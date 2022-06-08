from multiprocessing.dummy import Array


class CodeSmell(object): 
    def __init__(self, data):
        self.type = data['type']
        self.module = data['module']
        self.obj = data['obj']
        self.line = data['line']
        self.column = data['column']
        self.endLine = data['endLine']
        self.path = data['path']
        self.symbol = data['symbol']
        self.message = data['message']
        self.message_id = data['message-id']

    def __repr__(self) -> str:
        return f'{self.type} in {self.module} on line {self.line} at {self.column} with reason: {self.message}'

    def __str__(self) -> str:
        return f'{self.type} in {self.module} on line {self.line} at {self.column} with reason: {self.message}'

    @staticmethod
    def convert_dict(json_content) -> Array:
        ret = []
        for code_smell in json_content:
            ret.append(CodeSmell(code_smell))
        return ret