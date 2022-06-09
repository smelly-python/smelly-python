"""
The code smell modules provides the CodeSmell class
and the Location class, which is used by the CodeSmell.
"""
from multiprocessing.dummy import Array
from itertools import groupby


class Location:
    """
    The Location class contains the location information of a CodeSmell.
    This includes the module, object, line and column numbers of the code smell
    in the file that the path points to.
    """
    def __init__(self, data):
        self.module = data['module']
        self.python_object = data['obj']
        self.line = data['line']
        self.column = data['column']
        self.end_line = data['endLine']
        self.path = data['path']

    def __repr__(self) -> str:
        return f'in {self.module} on line {self.line} at {self.column}'

    def __str__(self):
        return f'in {self.module} on line {self.line} at {self.column}'


class CodeSmell:
    """
    The CodeSmell class contains all the fields of the JSON objects that pylint generates.
    """
    def __init__(self, data):
        self.type = data['type']
        self.location = Location(data)
        self.symbol = data['symbol']
        self.message = data['message']
        self.message_id = data['message-id']

    def __repr__(self) -> str:
        return f'{self.type} {repr(self.location)} with reason: {self.message}'

    def __str__(self) -> str:
        return f'{self.type} {self.location} with reason: {self.message}'

    def severity(self) -> int:
        """
        Gives the severity depending on the type of the code smell.
        Unknown types are automatically -1 severity.
        From high to low the severities are:
        - Error
        - Warning
        - Refactor
        - Convention
        :return: the severity of the code smell
        """
        types = ['convention', 'refactor', 'warning', 'error']
        return types.index(self.type) if self.type in types else -1

    @staticmethod
    def convert_dict(json_content) -> Array:
        """
        Converts
        :param json_content:
        :return:
        """
        ret = []
        for i in json_content:
            ret.append(CodeSmell(i))
        return ret

    @staticmethod
    def group_by_file(code_smells):
        """
        Takes a list of code smells and groups them by the file. 
        """
        def key_func(k):
            return k.location.path
        ret = []
        for key, value in groupby(code_smells, key_func):
            ret.append(list(value))
        return ret
