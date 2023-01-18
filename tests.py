from unittest import TestCase
import unittest

from validators.validators import IntegerFieldValidator, StringFieldValidator
from validators.exceptions import ValidatorFieldError
from validators.validators import TicTacToeRequestValidator

# VALIDATOR FIELDS TESTS


class IntegerFieldValidatorTest(TestCase):
    '''
    Validator integer field tests class.
    '''

    # VALIDATOR FIELD DEFINITION TESTS

    def test_proper_validator_field_definition(self):
        '''
        Tests IntegerFieldValidator proper initialization.
        '''

        validator_field_error_thrown = False
        try:
            IntegerFieldValidator(field_name="test_int", required=False, nullable=False)
        except ValidatorFieldError:
            validator_field_error_thrown = True

        self.assertFalse(validator_field_error_thrown)

    def test_invalid_validator_field_definition_required_attributes_invalid_types_values(self):
        '''
        Tests IntegerFieldValidator initialization in case when any required parameter type is invalid.
        '''

        validator_field_error_thrown_number = 0
        # all keyword arguments invalid types
        try:
            IntegerFieldValidator(field_name=[], required={}, nullable="str")
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        # invalid 'field_name' type
        try:
            IntegerFieldValidator(field_name={}, required=True, nullable=True)
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        # invalid 'required' type
        try:
            IntegerFieldValidator(field_name="test_int", required={}, nullable=True)
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        # invalid 'nullable' type
        try:
            IntegerFieldValidator(field_name="test_int", required=False, nullable={})
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        self.assertEqual(4, validator_field_error_thrown_number)

    def test_invalid_validator_field_definition_required_attributes_none_values(self):
        '''
        Tests IntegerFieldValidator initialization in case when any required parameter is equal to 'None'.
        '''

        validator_field_error_thrown_number = 0
        # all required fields values equal 'None'
        try:
            IntegerFieldValidator(field_name=None, required=None, nullable=None)
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        # 'field_name' param value = None
        try:
            IntegerFieldValidator(field_name=None, required=False, nullable=True)
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        # 'required' param value = None
        try:
            IntegerFieldValidator(field_name="test_int", required=None, nullable=True)
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        # 'nullable' param value = None
        try:
            IntegerFieldValidator(field_name="test_int", required=True, nullable=None)
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        self.assertEqual(4, validator_field_error_thrown_number)

    def test_invalid_validator_field_definition_required_attibutes_not_passed(self):
        '''
        Tests IntegerFieldValidator initialization in case when any required parameter is not passed.
        '''

        validator_field_error_thrown_number = 0
        # none constructor parameters passed
        try:
            IntegerFieldValidator()
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        # lack of 'field_name' attribute
        try:
            IntegerFieldValidator(required=False, nullable=False)
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        # lack of 'required' attribute
        try:
            IntegerFieldValidator(field_name="test_int", nullable=False)
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        # lack of 'nullable' attribute
        try:
            IntegerFieldValidator(field_name="test_int", required=False)
        except ValidatorFieldError:
            validator_field_error_thrown_number += 1

        self.assertEqual(4, validator_field_error_thrown_number)

    def test_validator_field_definition_min_value_invalid_type(self):
        '''
        Tests IntegerFieldValidator validation when field min value limit type is invalid (other than int)
        -> exception 'ValidatorFieldError' should be raised.
        '''

        validator_field_error_thrown = False
        try:
            IntegerFieldValidator(field_name="test_int", required=False, nullable=False, min_value="10")
        except ValidatorFieldError:
            validator_field_error_thrown = True

        self.assertTrue(validator_field_error_thrown)

    def test_validator_field_validation_max_value_invalid_type(self):
        '''
        Tests IntegerFieldValidator validation when field max value limit type is invalid (other than int)
        -> exception 'ValidatorFieldError' should be raised.
        '''

        validator_field_error_thrown = False
        try:
            IntegerFieldValidator(field_name="test_int", required=False, nullable=False, max_value="10")
        except ValidatorFieldError:
            validator_field_error_thrown = True

        self.assertTrue(validator_field_error_thrown)

    def test_validator_field_validation_min_and_max_proper_range(self):
        '''
        Tests IntegerFieldValidator definition when min value limit is lesser than max value limit.
        '''

        validator_field_error_thrown = False
        try:
            IntegerFieldValidator(field_name="test_int", required=False, nullable=False, min_value=-1,
                                  max_value=10)
        except ValidatorFieldError:
            validator_field_error_thrown = True

        self.assertFalse(validator_field_error_thrown)

    def test_validator_field_validation_min_and_max_range_validation(self):
        '''
        Tests IntegerFieldValidator definition when min value limit is greater than max value limit.
        '''

        validator_field_error_thrown = False
        try:
            IntegerFieldValidator(field_name="test_int", required=False, nullable=False, min_value=10,
                                  max_value=-10)
        except ValidatorFieldError:
            validator_field_error_thrown = True

        self.assertTrue(validator_field_error_thrown)

    # VALUE VALIDATION PROPER VALIDATION

    def test_proper_validator_field_validation_without_limits(self):
        '''
        Tests IntegerFieldValidator successful validation (without limits).
        '''

        validator_field_error_thrown = False
        try:
            validator = IntegerFieldValidator(field_name="test_int", required=False, nullable=False)
        except ValidatorFieldError:
            validator_field_error_thrown = True

        validator.set_value("10")

        valid = validator.is_valid()

        test_passed = (not validator_field_error_thrown and valid)
        self.assertTrue(test_passed)

    def test_proper_validator_field_validation_with_limits(self):
        '''
        Tests IntegerFieldValidator successful validation (without limits).
        '''

        validator = IntegerFieldValidator(field_name="test_int", required=False, nullable=False, min_value=-5,
                                          max_value=5)
        validator.set_value("5")

        valid = validator.is_valid()
        self.assertTrue(valid)

    # VALUE VALIDATION WITH MAX_VALUE LIMIT

    def test_proper_validator_field_validation_max_value_known(self):
        '''
        Tests IntegerFieldValidator validation when field max value limit is known.
        '''

        validator = IntegerFieldValidator(field_name="test_int", required=False, nullable=False, max_value=10)

        validator.set_value("100")
        greater_value_not_valid = not validator.is_valid()

        validator.set_value("-2")
        lesser_value_valid = validator.is_valid()

        self.assertTrue(greater_value_not_valid and lesser_value_valid)

    def test_validator_field_validation_max_value_none(self):
        '''
        Tests IntegerFieldValidator validation when field max value limit is None.
        '''

        validator = IntegerFieldValidator(field_name="test_int", required=False, nullable=False, max_value=None)
        validator.set_value("10")

        validator_valid = validator.is_valid()
        self.assertTrue(validator_valid)

    # VALUE VALIDATION WITH MIN_VALUE LIMIT

    def test_proper_validator_field_validation_min_value_known(self):
        '''
        Tests IntegerFieldValidator validation when field min value limit is known.
        '''
        validator = IntegerFieldValidator(field_name="test_int", required=False, nullable=False, min_value=-1)

        validator.set_value("10")
        greater_value_valid = validator.is_valid()

        validator.set_value("-2")
        lesser_value_invalid = not validator.is_valid()

        self.assertTrue(lesser_value_invalid and greater_value_valid)

    def test_validator_field_validation_min_value_none(self):
        '''
        Tests IntegerFieldValidator validation when field min value limit is None.
        '''

        validator = IntegerFieldValidator(field_name="test_int", required=False, nullable=False, min_value=None)
        validator.set_value("10")

        valid = validator.is_valid()
        self.assertTrue(valid)

    # VALUE VALIDATION TESTS (without limits)

    def test_validator_field_validation_invalid_value_type(self):
        '''
        Tests IntegerFieldValidator validation when passed validator field value is invalid (cannot cast to int).
        '''

        validator = IntegerFieldValidator(field_name="test_int", required=False, nullable=False)
        validator.set_value({})

        valid = validator.is_valid()
        self.assertFalse(valid)

    def test_validator_field_validation_unset_value(self):
        '''
        Tests IntegerFieldValidator validation when validator field value is unset.
        '''

        validator = IntegerFieldValidator(field_name="test_int", required=True, nullable=False)

        valid = validator.is_valid()
        self.assertFalse(valid)

    def test_validator_field_validation_none_value(self):
        '''
        Tests IntegerFieldValidator validation when validator field value is None.
        '''

        validator = IntegerFieldValidator(field_name="test_int", required=True, nullable=False)
        validator.set_value(None)

        valid = validator.is_valid()
        self.assertFalse(valid)

class StringFieldValidatorTest(TestCase):
    '''
    String field validator tests class
    '''

    # PROPER VALIDATOR DEFINITION TESTS


    def test_validator_field_proper_definition_without_optional_params(self):
        validator_error_thrown = False
        try:
            StringFieldValidator(field_name="test", required=True, nullable=False)
        except ValidatorFieldError:
            validator_error_thrown = True

        self.assertFalse(validator_error_thrown)

    def test_validator_field_proper_definition_with_min_length_param(self):
        validator_error_thrown = False
        try:
            StringFieldValidator(field_name="test", required=True, nullable=False, min_length=1)
        except ValidatorFieldError:
            validator_error_thrown = True

        self.assertFalse(validator_error_thrown)

    def test_validator_field_proper_definition_with_max_length_param(self):
        validator_error_thrown = False
        try:
            StringFieldValidator(field_name="test", required=True, nullable=False, max_length=1)
        except ValidatorFieldError:
            validator_error_thrown = True

        self.assertFalse(validator_error_thrown)

    def test_validator_field_proper_definition_with_empty_param(self):
        validator_error_thrown = False
        try:
            StringFieldValidator(field_name="test", required=True, nullable=False, empty=False)
        except ValidatorFieldError:
            validator_error_thrown = True

        self.assertFalse(validator_error_thrown)

    # IMPROPER VALIDATOR DEFINITION TESTS

    def test_validator_field_improper_definition_required_arguments_invalid_values_types(self):
        validator_error_thrown_number = 0

        try:
            StringFieldValidator(field_name=10, required=True, nullable=False)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        try:
            StringFieldValidator(field_name="Test", required={}, nullable=False)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        try:
            StringFieldValidator(field_name="Test", required=True, nullable="")
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        self.assertEqual(3, validator_error_thrown_number)

    def test_validator_field_improper_definition_required_arguments_none_values_passed(self):
        validator_error_thrown_number = 0

        try:
            StringFieldValidator(field_name=None, required=True, nullable=False)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        try:
            StringFieldValidator(field_name="Test", required=None, nullable=False)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        try:
            StringFieldValidator(field_name="Test", required=True, nullable=None)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        try:
            StringFieldValidator(field_name=None, required=None, nullable=None)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        self.assertEqual(4, validator_error_thrown_number)

    def test_validator_field_improper_definition_required_arguments_not_passed(self):
        validator_error_thrown_number = 0

        try:
            StringFieldValidator(required=True, nullable=False)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        try:
            StringFieldValidator(field_name="Test", nullable=False)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        try:
            StringFieldValidator(field_name="Test", required=True)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        try:
            StringFieldValidator()
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        self.assertEqual(4, validator_error_thrown_number)

    # IMPROPER VALIDATOR DEFINITION (OPTIONAL PARAMS) TESTS

    def test_validator_field_improper_definition_optional_arguments_none_values_passed(self):
        validator_error_thrown_number = 0

        # 'min_length' none value passed
        try:
            StringFieldValidator(field_name="Test", required=True, nullable=False, min_length=None)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        # 'max_length' none value passed
        try:
            StringFieldValidator(field_name="Test", required=True, nullable=False, max_length=None)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        # 'empty' param none value passed
        try:
            StringFieldValidator(field_name="Test", required=True, nullable=False, empty=None)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        self.assertEqual(0, validator_error_thrown_number)

    def test_validator_field_improper_definition_optional_arguments_invalid_types(self):
        validator_error_thrown_number = 0

        # 'min_length' param invalid type passed
        try:
            StringFieldValidator(field_name="Test", required=True, nullable=False, min_length={})
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        # 'max_length' param invalid type passed
        try:
            StringFieldValidator(field_name="Test", required=True, nullable=False, max_length="qwerty")
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        # 'empty' param invalid type passed
        try:
            StringFieldValidator(field_name="Test", required=True, nullable=False, empty=123)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        self.assertEqual(3, validator_error_thrown_number)

    def test_validator_field_improper_definition_min_max_length_invalid_range(self):
        validator_error_thrown = False
        try:
            StringFieldValidator(field_name="Test", required=True, nullable=False, min_length=5, max_length=2)
        except ValidatorFieldError:
            validator_error_thrown = True

        self.assertTrue(validator_error_thrown)

    def test_validator_field_improper_definition_min_max_length_disallowed_values(self):
        validator_error_thrown_number = 0

        # 'min_length' param negative value
        try:
            StringFieldValidator(field_name="Test", required=True, nullable=False, min_length=-1, max_length=2)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        # 'max_length' param negative value
        try:
            StringFieldValidator(field_name="Test", required=True, nullable=False, min_length=1, max_length=-2)
        except ValidatorFieldError:
            validator_error_thrown_number += 1

        self.assertEqual(2, validator_error_thrown_number)

    # FIELD VALIDATION TESTS

    def test_validator_field_proper_validation(self):
        '''
        Tests StringFieldValidator proper validation case (without optional parameters).
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False)
        validator.set_value("011101101")

        valid = validator.is_valid()
        self.assertTrue(valid)

    def test_validator_field_improper_validation_invalid_type(self):
        '''
        Tests StringFieldValidator improper validation case (when passed value type is other than 'str').
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False)
        validator.set_value({})

        validator_error_thrown_number = 0
        valid = validator.is_valid()
        if not valid:
            validator_error_thrown_number += 1

        validator.set_value(1)
        valid = validator.is_valid()
        if not valid:
            validator_error_thrown_number += 1

        validator.set_value(True)
        valid = validator.is_valid()
        if not valid:
            validator_error_thrown_number += 1

        self.assertEqual(3, validator_error_thrown_number)

    def test_validator_field_improper_validation_value_unset(self):
        '''
        Tests StringFieldValidator when validator field value is unset.
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False)

        valid = validator.is_valid()
        self.assertFalse(valid)

    def test_validator_field_improper_validation_value_is_none(self):
        '''
        Tests StringFieldValidator when validator field value is None.
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False)
        validator.set_value(None)

        valid = validator.is_valid()
        self.assertFalse(valid)

    def test_validator_field_proper_validation_with_optional_params(self):
        '''
        Tests StringFieldValidator proper validation case (but with present optional params passed while
        initializing validator field).
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False, min_length=5,
                                         max_length=10)
        validator.set_value("011101101")

        valid = validator.is_valid()
        self.assertTrue(valid)

    def test_validator_field_improper_validation_with_optional_params_too_long_value(self):
        '''
        Tests StringFieldValidator improper validation case (but with present optional params passed while
        initializing validator field) and too long validator field value.
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False, min_length=5,
                                         max_length=10)
        validator.set_value("011101101011101101")

        valid = validator.is_valid()
        self.assertFalse(valid)

    def test_validator_field_improper_validation_with_optional_params_too_short_value(self):
        '''
        Tests StringFieldValidator improper validation case (but with present optional params passed
        while initializing validator field) and too short validator field value.
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False, min_length=5,
                                         max_length=10)
        validator.set_value("0111")

        valid = validator.is_valid()
        self.assertFalse(valid)

    def test_validator_field_improper_validation_with_optional_params_value_none(self):
        '''
        Tests validator improper validation case when optional params are passed and field value is None.
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False, min_length=5,
                                         max_length=10)
        validator.set_value(None)

        valid = validator.is_valid()
        self.assertFalse(valid)

    def test_validator_field_improper_validation_with_optional_params_value_unset(self):
        '''
        Tests validator improper validation case when optional params are passed and field value is unset.
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False, min_length=5,
                                         max_length=10)

        valid = validator.is_valid()
        self.assertFalse(valid)

    def test_validator_field_proper_validation_empty_allowed(self):
        '''
        Tests validator improper validation case when optional params are passed and field value is allowed
        to be empty.
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False, empty=True)
        validator.set_value("")

        valid = validator.is_valid()
        self.assertTrue(valid)

    def test_validator_field_improper_validation_empty_disallowed(self):
        '''
        Tests validator improper validation case when optional params are passed and field value is not
        allowed to be empty.
        '''

        validator = StringFieldValidator(field_name="Test", required=True, nullable=False, empty=False)
        validator.set_value("")

        valid = validator.is_valid()
        self.assertFalse(valid)


# VALIDATOR TESTS

class TicTacToeValidatorTest(TestCase):
    '''
    TicTacToeRequestValidator tests class.
    '''

    def __validate_validator(self, request_data: dict):
        '''
        Passes given request data to validator and finds if request is valid or not.\n
        params:
            request_data: dict
        returns:
            bool - information whether request is valid or not
        '''

        validator = TicTacToeRequestValidator(request_data)
        valid = validator.is_valid()
        return valid

    def test_proper_request_all_cases(self):
        '''
        Tests request validator in case when received data are correct.
        '''

        request_data = {
            'grid_size': 3,
            'moving_player': 2,
            'grid': "010201102"
        }
        valid_3x3 = self.__validate_validator(request_data)

        request_data = {
            'grid_size': 4,
            'moving_player': 1,
            'grid': "0120012010021002"
        }
        valid_4x4 = self.__validate_validator(request_data)

        request_data = {
            'grid_size': 5,
            'moving_player': 1,
            'grid': "1000210002100022000120001"
        }
        valid_5x5 = self.__validate_validator(request_data)

        self.assertTrue(valid_3x3 and valid_4x4 and valid_5x5)

    # validator validation looking for 'grid_size' field

    def test_invalid_request_negative_grid_size(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid_size was negative.
        '''

        request_data = {
            'grid_size': -1,
            'moving_player': 1,
            'grid': "010201102"
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_too_big_grid_size(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid_size was too big (100).
        '''

        request_data = {
            'grid_size': 100,
            'moving_player': 1,
            'grid': "010201102"
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_grid_size_null(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid_size was null.
        '''

        request_data = {
            'grid_size': None,
            'moving_player': 1,
            'grid': "010201102"
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_grid_size_not_integer(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid_size wasn't integer.
        '''

        request_data = {
            'grid_size': "qwerty",
            'moving_player': 1,
            'grid': "010201102"
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_lack_of_grid_size(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid_size was absent.
        '''

        request_data = {
            'moving_player': 1,
            'grid': "010201102"
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_grid_size_not_relevant_to_grid(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid_size was irrelewant to received grid.
        '''

        request_data = {
            'grid_size': 4,
            'moving_player': 1,
            'grid': "010201102"
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    # validator validation looking for 'moving_player' field

    def test_invalid_request_moving_player_out_of_allowed_range(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent moving_player identifier was out of allowed range.
        '''

        # testing when moving player is lesser than 1
        request_data = {
            'grid_size': 3,
            'moving_player': 0,
            'grid': "010201102"
        }
        valid_lesser = self.__validate_validator(request_data)

        # testing when moving player is greater than 2
        request_data = {
            'grid_size': 3,
            'moving_player': 3,
            'grid': "010201102"
        }
        valid_greater = self.__validate_validator(request_data)

        self.assertTrue(not valid_lesser and not valid_greater)

    def test_invalid_request_moving_player_null(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent moving_player identifier was null.
        '''

        request_data = {
            'grid_size': 3,
            'moving_player': None,
            'grid': "010201102"
        }
        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_moving_player_type_not_int(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent moving_player identifier type was not int.
        '''

        request_data = {
            'grid_size': 3,
            'moving_player': {},
            'grid': "010201102"
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_moving_player_type_not_passed(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent moving_player identifier type was not passed.
        '''

        request_data = {
            'grid_size': 3,
            'grid': "010201102"
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_moving_player_moved_more_times(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        player meant to make a move, actually moved more times than opponent.
        '''

        request_data = {
            'grid_size': 3,
            'grid': "120120010",
            'moving_player': 1
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    # validator validation looking for 'grid' field

    def test_invalid_request_grid_contains_forbidden_characters(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid contains forbidden characters.
        '''

        request_data = {
            'moving_player': 1,
            'grid_size': 3,
            'grid': "01x20a103"
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_grid_is_null(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid is null.
        '''

        request_data = {
            'moving_player': 1,
            'grid_size': 3,
            'grid': None
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_grid_is_empty(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid is empty.
        '''

        request_data = {
            'moving_player': 1,
            'grid_size': 3,
            'grid': ""
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_grid_not_passed(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid is not passed.
        '''

        request_data = {
            'moving_player': 1,
            'grid_size': 3,
        }

        valid = self.__validate_validator(request_data)
        self.assertFalse(valid)

    def test_invalid_request_impossible_grid_state(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid is impossible to reach in real game.
        '''

        request_data = {
            'moving_player': 1,
            'grid_size': 3,
            'grid': "111000222"
        }
        valid_3x3 = self.__validate_validator(request_data)

        request_data = {
            'moving_player': 1,
            'grid_size': 4,
            'grid': "111100002222"
        }
        valid_4x4 = self.__validate_validator(request_data)

        request_data = {
            'moving_player': 1,
            'grid_size': 5,
            'grid': "111110000022222"
        }
        valid_5x5 = self.__validate_validator(request_data)

        self.assertTrue(not valid_3x3 and not valid_4x4 and not valid_5x5)

    def test_invalid_request_irrelevant_grid_length_to_size(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid length is irrelevant to declared grid size.
        '''

        request_data = {
            'moving_player': 1,
            'grid_size': 3,
            'grid': "111100002222"
        }
        valid_3x3 = self.__validate_validator(request_data)

        request_data = {
            'moving_player': 1,
            'grid_size': 4,
            'grid': "112000000"
        }
        valid_4x4 = self.__validate_validator(request_data)

        request_data = {
            'moving_player': 1,
            'grid_size': 5,
            'grid': "110000022"
        }
        valid_5x5 = self.__validate_validator(request_data)

        self.assertTrue(not valid_3x3 and not valid_4x4 and not valid_5x5)

    def test_invalid_request_irrelevant_grid_length_to_any_grid_size(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid is irrelevant to any possible grid size.
        '''

        request_data = {
            'moving_player': 1,
            'grid_size': 3,
            'grid': "110022"
        }
        valid_3x3 = self.__validate_validator(request_data)

        request_data = {
            'moving_player': 1,
            'grid_size': 4,
            'grid': "11201212121212121212121221120121212121212121212122"
        }
        valid_4x4 = self.__validate_validator(request_data)

        request_data = {
            'moving_player': 1,
            'grid_size': 5,
            'grid': "112000000000000000000000000000000000000"
        }
        valid_5x5 = self.__validate_validator(request_data)

        self.assertTrue(not valid_3x3 and not valid_4x4 and not valid_5x5)

    def test_invalid_request_irrelevant_grid_random_length(self):
        '''
        Tests request validator in case when received data are incorrect - more specifically :
        sent grid length is irrelevant to any possible grid size.
        '''

        request_data = {
            'moving_player': 1,
            'grid_size': 3,
            'grid': "1100220000000000000000000000000000000000000000000000000000000000000000"
        }
        valid_3x3 = self.__validate_validator(request_data)

        request_data = {
            'moving_player': 1,
            'grid_size': 4,
            'grid': "11200000000000000000"
        }
        valid_4x4 = self.__validate_validator(request_data)

        request_data = {
            'moving_player': 1,
            'grid_size': 5,
            'grid': "112000000000000000000000000000000000000"
        }
        valid_5x5 = self.__validate_validator(request_data)

        self.assertTrue(not valid_3x3 and not valid_4x4 and not valid_5x5)

if __name__ == "__main__":
    unittest.main()
