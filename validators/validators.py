from validators.exceptions import ValidationError, ValidatorFieldError

# VALIDATOR FIELD CLASSES


class BaseFieldValidator():
    '''
    Base validator required fields (declared while defining validator):

    field_name  - type: str     - validator field name (same as attribute while defining validator,
                                  it's used when raising validation error if necessary).
    required    - type: bool    - boolean value whether specific validator field is required or not.
    nullable    - type: bool    - boolean value whether specific validator field value can be null or not.
    '''
    # Base validator required fields (declared while defining validator)

    _required = None
    _name = None
    _nullable = None

    def __init__(self, field_name=None, required=None, nullable=None):
        '''
        Base validator field initializer.

        args:
            field_name  - type: str     - Validator field name
            required    - type: bool    - Information if field is required or not
            nullable    - type: bool    - Information if field can be None or not
        '''

        # field_name param validation
        if field_name is None:
            raise ValidatorFieldError("none_field", "Missing required field name value.")
        if type(field_name) != str:
            raise ValidatorFieldError("none_field", "Provided field name type is not str.")

        # required param validation
        if required is None:
            raise ValidatorFieldError(field_name, "Missing required information if field \
'{validator_field_name}' is required.".format(validator_field_name=field_name))
        if type(required) != bool:
            raise ValidatorFieldError(field_name, "Provided 'required' parameter type is not bool.")

        # nullable param validation
        if nullable is None:
            raise ValidatorFieldError(field_name, "Missing required information if field \
'{validator_field_name}' can be null.".format(validator_field_name=field_name))
        if type(nullable) != bool:
            raise ValidatorFieldError(field_name, "Provided 'nullable' parameter type is not bool.")

        self._required = required
        self._name = field_name
        self._nullable = nullable

    def validate(self):
        '''
        Validates specific validator field (checks if provided was required values - if not, then ValidationError is thrown).
        '''

        field_value = getattr(self, "_value", None)
        required = getattr(self, "_required", None)
        nullable = getattr(self, "_nullable", None)

        # check if field can be None, if not and value is None => raise ValidationError
        if not nullable:
            if field_value is None:
                raise ValidationError(self._name, "Field '{field_name}' cannot be null.".format(field_name=self._name))

        # if field is required and value for this field is not provided => raise ValidationError
        if required:
            if field_value is None:
                raise ValidationError(self._name, "Required parameter '{field_name}' is missing".format(field_name=self._name))

    def is_valid(self):
        '''
        Runs inner validation and if it throws exception, False is returned, otherwise True.

        returns:
            bool - information if validator data are correct or not.
        '''

        try:
            self.validate()
        except ValidationError:
            return False
        return True


class IntegerFieldValidator(BaseFieldValidator):
    '''
    Integer field validator class.

    Possible keyword arguments:
    field_name  - type: str     - validator field name (same as attribute while defining validator,
                                  it's used when raising validation error if necessary).
    required    - type: bool    - boolean value whether specific validator field is required or not.
    nullable    - type: bool    - information whether field value can be None or not.
    min_value   - type: int     - min field value that is acceptable.
    max_value   - type: int     - max field value that is acceptable.
    '''

    _value = None
    _min_value = None
    _max_value = None

    # dictionary for validator errors
    errors = None

    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        '''
        Initializes IntegerFieldValidator.

        args:
            min_value   - type: int     - integer minimal value
            max_value   - type: int     - integer maximal value

        throws:
            ValidatorFieldError    - this exception is thrown when something went wrong while creating validator field
        '''

        super().__init__(*args, **kwargs)

        # checking 'min_value' parameter type
        if min_value is not None:
            if type(min_value) != int:
                raise ValidatorFieldError(self._name, "Invalid parameter 'min_value' for field {field_name} \
- received value type was {received_type}, expected was {expected_type}.".format(
                    field_name=self._name,
                    received_type=str(type(min_value)),
                    expected_type=str(int)
                ))

        # checking 'max_value' parameter type
        if max_value is not None:
            if type(max_value) != int:
                raise ValidatorFieldError(self._name, "Invalid parameter 'max_value' for field {field_name} \
- received value type was {received_type}, expected was {expected_type}.".format(
                    field_name=self._name,
                    received_type=str(type(max_value)),
                    expected_type=str(int)
                ))

        # checking if range 'min_value'-'max_value' is valid
        if min_value is not None and max_value is not None:
            if min_value > max_value:
                raise ValidatorFieldError(self._name, "Invalid 'min_value' and 'max_value' parameters configuration \
- 'min_value' is lesser than 'max_value'.")

        self._min_value = min_value
        self._max_value = max_value

        self.errors = {}

    def get_value(self):
        return getattr("_value", None)

    def set_value(self, value):
        setattr(self, "_value", value)

    def __validate(self):
        '''
        Validates value of IntegerFieldValidator.

        throws:
            ValidationError - thrown when something wrong was detected in provided data
        '''

        super().validate()  # invoke base validation

        # type validation
        try:
            self._value = int(self._value)
        except ValueError:  # raise ValidationError if could not cast to integer
            raise ValidationError(self._name, "Provided value for field '{validator_field_name}' is not an integer.".format(validator_field_name=self._name))
        except TypeError:
            raise ValidationError(self._name, "Provided value for field '{validator_field_name}' is not an integer.".format(validator_field_name=self._name))

        # min value validation (if it exists)
        if self._min_value is not None:
            if self._value < self._min_value:
                raise ValidationError(self._name, "Provided integer value is lesser than minimal acceptable.")

        # max value validation (if it exists)
        if self._max_value is not None:
            if self._value > self._max_value:
                raise ValidationError(self._name, "Provided integer value is greater than maximal acceptable.")

    def is_valid(self):
        '''
        Runs validation of ValidatorField.

        returns:
            boolean info whether value of IntegerFieldValidator is correct or not
        '''

        try:
            self.__validate()
        except ValidationError as err:
            self.errors[err._field] = err._message
            return False
        return True


class StringFieldValidator(BaseFieldValidator):  # noqa: C901
    '''
    Validator string field class.

    Possible keyword arguments:
    field_name  - type: str     - validator field name (same as attribute while defining validator - it's used when raising validation error if necessary).
    required    - type: bool    - boolean value whether specific validator field is required or not.
    nullable    - type: bool    - information whether field value can be None or not.
    min_length  - type: int     - minimal string field length.
    max_length  - type: int     - maximal string field length.
    empty       - type: bool    - information whether field value length can be empty or not.
    '''

    _value = None
    _min_length = None
    _max_length = None
    _empty = None

    errors = None

    def __init__(self, min_length=None, max_length=None, empty=None, *args, **kwargs):
        '''
        Initializes StringFieldValidator.

        args:
            min_length  - type: int     - validator field value min length
            max_length  - type: int     - validator field value max length
            empty       - type: bool    - information if validator field can be empty

        throws:
            ValidatorFieldError - when could not create validator
        '''

        super().__init__(*args, **kwargs)

        # check 'min_length' parameter => if invalid, raise SerializerFieldError
        if min_length is not None:
            if type(min_length) == int:
                if min_length < 0:
                    raise ValidatorFieldError(self._name, "'min_length' parameter value must be non-negative value.")
                self._min_length = min_length
            else:
                raise ValidatorFieldError(self._name, "'min_length' parameter type must be 'int'. Passed value type was\
{passed_value_type}".format(passed_value_type=type(min_length)))

        # check 'max_length' parameter => if invalid, raise SerializerFieldError
        if max_length is not None:
            if type(max_length) == int:
                if max_length < 0:
                    raise ValidatorFieldError(self._name, "'max_length' parameter value must be non-negative value.")
                self._max_length = max_length
            else:
                raise ValidatorFieldError(self._name, "'max_length' parameter type must be 'int'. Passed value type was\
{passed_value_type}".format(passed_value_type=type(max_length)))

        # check 'empty' parameter => if invalid, raise SerializerFieldError
        if empty is not None:
            if type(empty) == bool:
                self._empty = empty
            else:
                raise ValidatorFieldError(self._name, "'empty' parameter type must be 'bool'. Passed value type was \
{passed_value_type}".format(passed_value_type=type(empty)))

        # check range 'min_length' - 'max_length'
        if min_length is not None and max_length is not None:
            if min_length > max_length:
                raise ValidatorFieldError(self._name, "'min_length' parameter value cannot be lesser than 'max_length'.")

        # check 'min_length', 'max_length' and 'empty' parameters configuration
        if min_length is not None and max_length is not None and empty is not None:
            if (min_length == 0 or max_length == 0) and not empty:
                raise ValidatorFieldError(
                    self._name,
                    "Neither 'min_length' nor 'max_length' can be 0, because field cannot be empty."
                )

        self.errors = {}

    def get_value(self):
        return getattr("_value", None)

    def set_value(self, value):
        setattr(self, "_value", value)

    def __validate(self):
        '''
        Validates string field validator value.

        throws:
            ValidationError - thrown when something wrong was detected in provided data
        '''
        super().validate()  # invoke base validation (required fields)

        # type validation
        if type(self._value) != str:
            raise ValidationError(self._name, "Type of provided value for field '{serializer_field_name}' is not str.".format(
                serializer_field_name=self._name
            ))

        # check if field can be empty
        if self._empty is not None:
            if not self._empty:
                if len(self._value) == 0:
                    raise ValidationError(self._name, "Field '{serializer_field_name}' cannot be empty.".format(
                        serializer_field_name=self._name
                    ))

        # compare grid value length with min_length
        if self._min_length is not None:
            if len(self._value) < self._min_length:
                raise ValidationError(self._name, "Provided value for field '{serializer_field_name}' is too short - \
it's length is equal to {value_length} but it should contain at least {min_length_value} characters.".format(
                    serializer_field_name=self._name,
                    value_length=len(self._value),
                    min_length_value=self._min_length
                ))

        # compare grid value length with max_length
        if self._max_length is not None:
            if len(self._value) > self._max_length:
                raise ValidationError(self._name, "Provided value for field '{serializer_field_name}' is too long - \
it's length is equal to {value_length} but it should contain max. {max_length_value} characters.".format(
                    serializer_field_name=self._name,
                    value_length=len(self._value),
                    max_length_value=self._max_length
                ))

    def is_valid(self):
        '''
        Runs validation of ValidatorField.

        returns:
            boolean info whether value of IntegerFieldValidator is correct or not
        '''

        try:
            self.__validate()
        except ValidationError as err:
            self.errors[err._field] = err._message
            return False
        return True

# VALIDATORS CLASSES


class TicTacToeRequestValidator():
    '''
    Tic-Tac-Toe request validator.
    '''

    moving_player = IntegerFieldValidator(field_name="moving_player", required=True, nullable=False, min_value=1, max_value=2)
    grid = StringFieldValidator(field_name="grid", required=True, nullable=False, empty=False, min_length=9, max_length=25)
    grid_size = IntegerFieldValidator(field_name="grid_size", required=True, nullable=False, min_value=3, max_value=5)

    def __init__(self, validator_data):
        '''
        Initiate TicTacToeRequestValidator.
        '''

        # fetching validator fields
        tmp = list(self.__dir__())
        validator_fields = []
        for t in tmp:
            a = str(type(getattr(self, t)))
            if "FieldValidator" in a:
                validator_fields.append(t)

        # set necessary 'data' and 'validated_data' structures in validator
        setattr(self, "data", validator_data)
        setattr(self, "validated_data", {})
        setattr(self, "errors", {})

        # process all validator fields
        for field_key in validator_fields:
            validator_field = getattr(self, field_key)  # fetch validator field
            field_value = validator_data.get(field_key, None)  # fetch value meant to be validator field value
            validator_field.set_value(field_value)  # set value for validator field
            # add field value to validated data dictionary (so it's not necessary to make it after validation
            # => validation will raise any exception)
            self.validated_data[field_key] = field_value

    def __get_grid_stats(self, grid_value, grid_size_value):
        '''
        Makes grid stats.

        args:
            grid_value - state of grid
            grid_size_value - size of grid

        returns:
            Lists of rows, columns, diagonal sums
        '''

        # check if received grid
        rows_sums = [0 for i in range(0, grid_size_value)]
        columns_sums = [0 for i in range(0, grid_size_value)]
        diagonal_sums = [0, 0]
        # processing all fields in grid
        for i in range(0, grid_size_value * grid_size_value):
            row = int(i / grid_size_value)
            column = int(i % grid_size_value)
            # 'X' player field
            if grid_value[i] == '1':
                rows_sums[row] += 1
                columns_sums[column] += 1
                if row == column:
                    diagonal_sums[0] += 1
                if row == grid_size_value - row - 1:
                    diagonal_sums[1] += 1
            # 'O' player field
            elif grid_value[i] == '2':
                rows_sums[row] -= 1
                columns_sums[column] -= 1
                if row == column:
                    diagonal_sums[0] -= 1
                if row == grid_size_value - row - 1:
                    diagonal_sums[1] -= 1

        return rows_sums, columns_sums, diagonal_sums

    def __validate(self):
        '''
        Validates TicTacToeRequestValidator.

        throws:
            ValidationError - when something in validator data is incorrect.
        '''

        # fetching validator fields
        tmp = list(self.__dir__())
        validator_fields = []
        for t in tmp:
            a = str(type(getattr(self, t)))
            if "FieldValidator" in a:
                validator_fields.append(t)

        # run 'validate()' method for each validator field
        for field in validator_fields:
            validator_field = getattr(self, field)
            valid = validator_field.is_valid()
            if not valid:
                raise ValidationError(validator_field._name, validator_field.errors[validator_field._name])

        # adding custom validation for specific fields
        grid_value = self.data["grid"]
        grid_size_value = self.data["grid_size"]

        # 'grid' FIELD VALUE VALIDATION

        # checking received grid state length with declared grid size
        if len(grid_value) != grid_size_value * grid_size_value:
            raise ValidationError("grid", "Received grid length is irrelevant to declared grid size. Received grid length is \
{grid_length} but should be equal to {expected_grid_length}".format(
                grid_length=len(grid_value),
                expected_grid_length=(grid_size_value * grid_size_value)
            ))

        # received grid value length validation
        if len(grid_value) != 9 and len(grid_value) != 16 and len(grid_value) != 25:
            raise ValidationError("grid", "Received grid state is invalid - it's length should be 9, 16 or 25. \
Length of received value was {received_grid_length}.".format(received_grid_length=len(grid_value)))

        # received grid value elements validation -> allowed values ['0', '1', '2']
        for i in range(0, len(grid_value)):
            if grid_value[i] not in ['0', '1', '2']:
                raise ValidationError("grid", "Invalid grid state identifier at index {invalid_index}.".format(
                    invalid_index=i
                ))

        # checking if received grid state is possible to happen (if one player did not make a move multiple times)
        x_fields, o_fields = 0, 0
        for i in range(0, len(grid_value)):
            if grid_value[i] == '1':
                x_fields += 1
            elif grid_value[i] == '2':
                o_fields += 1

        # check difference is more than one field
        if abs(x_fields - o_fields) > 1:
            raise ValidationError(
                "grid",
                "Received grid is invalid - in tic-tac-toe game there no scenario to make this state happen."
            )

        # check if one player made more moves than other one
        moving_player = self.data["moving_player"]
        if moving_player == 1 and x_fields > o_fields or moving_player == 2 and o_fields > x_fields:
            raise ValidationError(
                "moving_player",
                "Requested player made more moves than opponent - cannot process this request."
            )

        rows_sums, columns_sums, diagonal_sums = self.__get_grid_stats(grid_value, grid_size_value)

        # checking if player 'X' won in received grid
        if grid_size_value in rows_sums or grid_size_value in columns_sums or grid_size_value in diagonal_sums:
            raise ValidationError("grid", "Received grid is invalid - the game is ended and player 'X' won.")

        # checking if player 'O' won in received grid
        if -grid_size_value in rows_sums or -grid_size_value in columns_sums or -grid_size_value in diagonal_sums:
            raise ValidationError("grid", "Received grid is invalid - the game is ended and player 'O' won.")

    def is_valid(self):
        '''
        Decides whether received request is valid or not.

        returns:
            bool - information whether validator data are correct or not.
        '''

        try:
            self.__validate()
        except ValidationError as error:
            self.errors[error._field] = error._message
            return False
        return True
