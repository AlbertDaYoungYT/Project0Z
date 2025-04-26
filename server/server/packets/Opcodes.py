class OpcodeMeta(type):
    _registry = {}

    def __new__(cls, name, bases, attrs):
        opcode = attrs.get('opcode')
        disabled = attrs.get('disabled', False)
        if opcode is not None:
            cls._registry[opcode] = {'class_name': name, 'disabled': disabled}
        return super().__new__(cls, name, bases, attrs)

class Opcodes:
    def __init__(self, value: int, disabled: bool = False):
        self.value = value
        self.disabled = disabled

def opcodes(value: int, disabled: bool = False):
    def decorator(cls):
        setattr(cls, 'opcode', value)
        setattr(cls, 'disabled', disabled)
        return cls
    return decorator