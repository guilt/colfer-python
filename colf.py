#!/usr/bin/env python3

from collections import OrderedDict
import six
import sys

if sys.version_info[0:2] >= (3, 8):
    long = int

class Colfer(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__setitem__('__dummy', None)
        self.__dict__['__variables'] = OrderedDict()

    def __isType(self, variable, typesToCheck):
        for typeToCheck in typesToCheck:
            if type(variable) is typeToCheck:
                return True
        return False

    def __checkRange(self, variable, minInclusive, maxInclusive):
        return variable >= minInclusive and variable <= maxInclusive

    def isBool(self, variable):
        return self.__isType(variable, [bool])

    def isInt(self, variable):
        return self.__isType(variable, [int])

    def isShort(self, variable):
        return self.isInt16(variable)

    def isLong(self, variable):
        return self.__isType(variable, [long])

    def isInt8(self, variable):
        return self.isInt(variable) and self.__checkRange(variable, -128, 127)

    def isUint8(self, variable):
        return self.isInt(variable) and self.__checkRange(variable, 0, 255)

    def isInt16(self, variable):
        # Two's complement allows -32768
        return self.isInt(variable) and self.__checkRange(variable, -32768, 32767)

    def isUint16(self, variable):
        return self.isInt(variable) and self.__checkRange(variable, 0, 65535)

    def isInt32(self, variable):
        return self.isInt(variable) and self.__checkRange(variable, -2147483648, 2147483647)

    def isUint32(self, variable):
        return self.isInt(variable) and self.__checkRange(variable, 0, 4294967295)

    def isInt64(self, variable):
        return (self.isLong(variable) or self.isInt(variable)) \
               and self.__checkRange(variable, -9223372036854775808, 9223372036854775807)

    def isUint64(self, variable):
        return (self.isLong(variable) or self.isInt(variable)) \
               and self.__checkRange(variable, 0, 18446744073709551615)

    def isFloat(self, variable):
        return self.__isType(variable, [float])

    def isDouble(self, variable):
        # TODO: Figure out Float128, Big Number Types in Python
        return self.isFloat64(variable)

    def isFloat32(self, variable):
        return self.isFloat(variable) \
               and self.__checkRange(variable, -3.402823e+38, 3.402823e+38)

    def isFloat64(self, variable):
        return self.isFloat(variable) \
               and self.__checkRange(variable, -1.7976931348623158e+308, 1.7976931348623158e+308)

    def isTimestamp(self, variable):
        from datetime import datetime
        return self.isDouble(variable) or self.isLong(variable) or self.__isType(variable, datetime)

    def isBinary(self, variable):
        return self.__isType(variable, [bytes, bytearray])

    def isBinaryOutput(self, variable):
        return self.__isType(variable, [bytearray])

    def isString(self, variable):
        return self.__isType(variable, six.string_types)

    def isList(self, variable):
        return self.__isType(variable, [list, tuple])

    def isType(self, variable, variableType):
        STRING_TYPES_MAP = {
            'bool': Colfer.isBool,
            'Bool': Colfer.isBool,

            'boolean': Colfer.isBool,
            'Boolean': Colfer.isBool,

            'byte': Colfer.isUint8,
            'Byte': Colfer.isUint8,

            'int8': Colfer.isInt8,
            'Int8': Colfer.isInt8,

            'uint8': Colfer.isUint8,
            'Uint8': Colfer.isUint8,

            'int16': Colfer.isInt16,
            'Int16': Colfer.isInt16,

            'uint16': Colfer.isUint16,
            'Uint16': Colfer.isUint16,

            'int32': Colfer.isInt32,
            'Int32': Colfer.isInt32,

            'uint32': Colfer.isUint32,
            'Uint32': Colfer.isUint32,

            'int64': Colfer.isInt64,
            'Int64': Colfer.isInt64,

            'uint64': Colfer.isUint64,
            'Uint64': Colfer.isUint64,

            'short': Colfer.isShort,
            'Short': Colfer.isShort,

            'int': Colfer.isInt,
            'Int': Colfer.isInt,

            'long': Colfer.isLong,
            'Long': Colfer.isLong,

            'float32': Colfer.isFloat,
            'Float32': Colfer.isFloat,

            'float': Colfer.isFloat,
            'Float': Colfer.isFloat,

            'float64': Colfer.isDouble,
            'Float64': Colfer.isDouble,

            'double': Colfer.isDouble,
            'Double': Colfer.isDouble,

            'timestamp': Colfer.isTimestamp,
            'Timestamp': Colfer.isTimestamp,
            'TimeStamp': Colfer.isTimestamp,

            'datetime': Colfer.isTimestamp,
            'Datetime': Colfer.isTimestamp,
            'DateTime': Colfer.isTimestamp,

            'str': Colfer.isString,
            'Str': Colfer.isString,

            'string': Colfer.isString,
            'String': Colfer.isString,

            'text': Colfer.isString,
            'Text': Colfer.isString,

            'unicode': Colfer.isString,
            'Unicode': Colfer.isString,

            'binary': Colfer.isBinary,
            'Binary': Colfer.isBinary,

            'bytes': Colfer.isBinary,
            'Bytes': Colfer.isBinary,

            'bytearray': Colfer.isBinary,
            'Bytearray': Colfer.isBinary,
            'ByteArray': Colfer.isBinary,

            'list': Colfer.isList,
            'List': Colfer.isList,

            'tuple': Colfer.isList,
            'Tuple': Colfer.isList,
        }
        if variableType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableType]
            return functionToCall(self, variable)
        return False

    def __dir__(self):
        return self.__dict__['__variables'].keys()

    def keys(self):
        return iter(name for name in self.__dict__['__variables'].keys())

    def values(self):
        return iter(value[1] for value in self.__dict__['__variables'].values())

    def items(self):
        return iter((name, value[1]) for name, value in self.__dict__['__variables'].items())

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __getattr__(self, name):
        if not name in self.__dict__['__variables']:
            raise AttributeError('Attribute {} does not exist.'.format(name))
        return self.__dict__['__variables'][name][1]

    def __setAttributeKnown(self, name, typeAsString, value):
        self.__dict__['__variables'][name] = [typeAsString, value]

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)

    def __setattr__(self, name, value):
        if not name in self.__dict__['__variables']:
            typeAsString = str(type(value).__name__)
        else:
            typeAsString = self.__dict__['__variables'][name][0]
        if not self.isType(value, typeAsString):
            raise AttributeError(
                'Attribute {} is of type {}. Cannot be assigned to {}'.format(name, typeAsString, value))
        self.__setAttributeKnown(name, typeAsString, value)

    def __delitem__(self, name):
        raise NotImplementedError('Del {} is unimplementable.'.format(name))

    def __str__(self):
        return dict(self.items()).__str__()

    def declareAttribute(self, name, variableType, value=None):
        if name is None or variableType is None or type(variableType) is not str:
            raise AttributeError('Must declare a valid attribute and type')
        if name in self.__dict__['__variables']:
            raise AttributeError('Cannot declare attribute {} again'.format(name))
        if value is not None:
            variableType = self.__dict__['__variables'][name][0]
            if not self.isType(value, variableType):
                raise AttributeError(
                    'Attribute {} is of type {}. Cannot be assigned to {}'.format(name, variableType, value))
        self.__dict__['__variables'][name] = [variableType, value]

    def __unmarshallType(self, name, variableType, byteInput, offset):
        print('Unmarshalling: {}:{} @{}'.format(name, variableType, offset))
        return None, offset

    def __marshallType(self, name, variableType, variableValue, byteOutput, offset):
        print('Marshalling: {}:{}={} @{}'.format(name, variableType, variableValue, offset))
        return offset

    def unMarshall(self, byteInput, offset=0):
        assert (byteInput != None)
        assert (self.isBinary(byteInput))
        assert (offset >= 0)
        for name in self.__dict__['__variables']:
            variableType, _ = self.__dict__['__variables'][name]
            newValue, offset = self.__unmarshallType(name, variableType, byteInput, offset)
            self.__dict__['__variables'][name] = [variableType, newValue]
        return self, offset

    def marshall(self, byteOutput, offset=0):
        assert (byteOutput != None)
        assert (self.isBinaryOutput(byteOutput))
        assert (offset >= 0)
        for name in self.__dict__['__variables']:
            variableType, value = self.__dict__['__variables'][name]
            offset = self.__marshallType(name, variableType, value, byteOutput, offset)
        return offset


def main():
    pass


if __name__ == '__main__':
    main()
