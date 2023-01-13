class ValidationError(Exception):
    '''
    Validator field validation exception.

    Required arguments while raising this kind of exception:
    field_name          - type: str - name of field that exception is raised for
    exception_message   - type: str - exception message
    '''

    _field = None
    _message = None

    def __init__(self, field_name = None, exception_message = None):
        # raising exception for field validation, if any argument is missing => raise simple exception
        if field_name is None or exception_message is None:
            raise Exception("ValidationError raised improperly - missing field_name or exception_message")

        self._field = field_name
        self._message = exception_message

class ValidatorFieldError(Exception):
    '''
    Validator field exception (meant to be thrown only when validator field is created improperly).

    Required arguments while raising this kind of exception:
    field_name          - type: str - name of field that exception is raised for
    exception_message   - type: str - exception message
    '''

    _field = None
    _message = None

    def __init__(self, field_name = None, exception_message = None):
        # raising exception for field validation, if any argument is missing => raise simple exception
        if field_name is None or exception_message is None:
            raise Exception("ValidatorFieldError raised improperly - missing field_name or exception_message")
        
        self._field = field_name
        self._message = exception_message
