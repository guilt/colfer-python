#!/usr/bin/env python3

from collections import OrderedDict
import six
import sys

if sys.version_info[0:2] >= (3, 8):
    long = int

class TypeCheckMixin(object):
    def __isType(self, variable, typesToCheck):
        for typeToCheck in typesToCheck:
            if type(variable) is typeToCheck:
                return True
        return False

    def __checkRange(self, variable, minInclusive, maxInclusive):
        return variable >= minInclusive and variable <= maxInclusive

    def __isInt(self, variable):
        return self.__isType(variable, [int])

    def __isShort(self, variable):
        return self.isInt16(variable)

    def __isLong(self, variable):
        return self.__isType(variable, [long])

    def __isFloat(self, variable):
        # TODO: Figure out Float128, Big Number Types in Python
        return self.__isType(variable, [float])

    def isBool(self, variable):
        return self.__isType(variable, [bool])

    def isInt8(self, variable):
        return self.__isInt(variable) and self.__checkRange(variable, -128, 127)

    def isUint8(self, variable):
        return self.__isInt(variable) and self.__checkRange(variable, 0, 255)

    def isInt16(self, variable):
        # Two's complement allows -32768
        return self.__isInt(variable) and self.__checkRange(variable, -32768, 32767)

    def isUint16(self, variable):
        return self.__isInt(variable) and self.__checkRange(variable, 0, 65535)

    def isInt32(self, variable):
        return self.__isInt(variable) and self.__checkRange(variable, -2147483648, 2147483647)

    def isUint32(self, variable):
        return self.__isInt(variable) and self.__checkRange(variable, 0, 4294967295)

    def isInt64(self, variable):
        return (self.__isLong(variable) or self.__isInt(variable)) \
               and self.__checkRange(variable, -9223372036854775808, 9223372036854775807)

    def isUint64(self, variable):
        return (self.__isLong(variable) or self.__isInt(variable)) \
               and self.__checkRange(variable, 0, 18446744073709551615)

    def isFloat32(self, variable):
        return self.__isFloat(variable) \
               and self.__checkRange(variable, -3.402823e+38, 3.402823e+38)

    def isFloat64(self, variable):
        return self.__isFloat(variable) \
               and self.__checkRange(variable, -1.7976931348623158e+308, 1.7976931348623158e+308)

    def isTimestamp(self, variable):
        from datetime import datetime
        return self.__isType(variable, datetime)

    def isBinary(self, variable, outputCapable=False):
        if outputCapable:
            return self.__isType(variable, [bytearray])
        return self.__isType(variable, [bytes, bytearray])

    def isString(self, variable):
        return self.__isType(variable, six.string_types)

    def isList(self, variable):
        return self.__isType(variable, [list, tuple])

    def isType(self, variable, variableType):
        STRING_TYPES_MAP = {
            'bool': TypeCheckMixin.isBool,
            'Bool': TypeCheckMixin.isBool,

            'boolean': TypeCheckMixin.isBool,
            'Boolean': TypeCheckMixin.isBool,

            'byte': TypeCheckMixin.isUint8,
            'Byte': TypeCheckMixin.isUint8,

            'int8': TypeCheckMixin.isInt8,
            'Int8': TypeCheckMixin.isInt8,

            'uint8': TypeCheckMixin.isUint8,
            'Uint8': TypeCheckMixin.isUint8,

            'int16': TypeCheckMixin.isInt16,
            'Int16': TypeCheckMixin.isInt16,

            'uint16': TypeCheckMixin.isUint16,
            'Uint16': TypeCheckMixin.isUint16,

            'int32': TypeCheckMixin.isInt32,
            'Int32': TypeCheckMixin.isInt32,

            'uint32': TypeCheckMixin.isUint32,
            'Uint32': TypeCheckMixin.isUint32,

            'int64': TypeCheckMixin.isInt64,
            'Int64': TypeCheckMixin.isInt64,

            'uint64': TypeCheckMixin.isUint64,
            'Uint64': TypeCheckMixin.isUint64,

            'float32': TypeCheckMixin.isFloat32,
            'Float32': TypeCheckMixin.isFloat32,

            'float64': TypeCheckMixin.isFloat64,
            'Float64': TypeCheckMixin.isFloat64,

            'timestamp': TypeCheckMixin.isTimestamp,
            'Timestamp': TypeCheckMixin.isTimestamp,
            'TimeStamp': TypeCheckMixin.isTimestamp,

            'datetime': TypeCheckMixin.isTimestamp,
            'Datetime': TypeCheckMixin.isTimestamp,
            'DateTime': TypeCheckMixin.isTimestamp,

            'str': TypeCheckMixin.isString,
            'Str': TypeCheckMixin.isString,

            'string': TypeCheckMixin.isString,
            'String': TypeCheckMixin.isString,

            'text': TypeCheckMixin.isString,
            'Text': TypeCheckMixin.isString,

            'unicode': TypeCheckMixin.isString,
            'Unicode': TypeCheckMixin.isString,

            'binary': TypeCheckMixin.isBinary,
            'Binary': TypeCheckMixin.isBinary,

            'bytes': TypeCheckMixin.isBinary,
            'Bytes': TypeCheckMixin.isBinary,

            'bytearray': TypeCheckMixin.isBinary,
            'Bytearray': TypeCheckMixin.isBinary,
            'ByteArray': TypeCheckMixin.isBinary,

            'list': TypeCheckMixin.isList,
            'List': TypeCheckMixin.isList,

            'tuple': TypeCheckMixin.isList,
            'Tuple': TypeCheckMixin.isList,
        }
        if variableType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableType]
            return functionToCall(self, variable)
        return False

class ColferMarshallerMixin(object):

    def marshall(self, byteOutput, offset=0):
        assert (byteOutput != None)
        assert (self.isBinary(byteOutput, True))
        assert (offset >= 0)
        for name in self.__dict__['__variables']:
            variableType, value = self.__dict__['__variables'][name]
            offset = self.marshallType(name, variableType, value, byteOutput, offset)
        return offset

    def marshallBool(self, name, variableValue, byteOutput, offset):
        if variableValue:
            byteOutput[offset] = 0
            offset += 1
        return offset

    def marshallType(self, name, variableType, variableValue, byteOutput, offset):
        print('Marshalling: {}:{}={} @{}'.format(name, variableType, variableValue, offset))
        if variableType == 'bool':
            offset = self.marshallBool(name, variableValue, byteOutput, offset)
        return offset

class ColferUnmarshallerMixin(object):

    def unMarshall(self, byteInput, offset=0):
        assert (byteInput != None)
        assert (self.isBinary(byteInput))
        assert (offset >= 0)
        for name in self.__dict__['__variables']:
            variableType, _ = self.__dict__['__variables'][name]
            newValue, offset = self.unmarshallType(name, variableType, byteInput, offset)
            self.__dict__['__variables'][name] = [variableType, newValue]
        return self, offset

    def unmarshallType(self, name, variableType, byteInput, offset):
        print('Unmarshalling: {}:{} @{}'.format(name, variableType, offset))
        return None, offset


class Colfer(dict, TypeCheckMixin, ColferMarshallerMixin, ColferUnmarshallerMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__setitem__('__dummy', None)
        self.__dict__['__variables'] = OrderedDict()

    def __dir__(self):
        return self.__dict__['__variables'].keys()

    def __str__(self):
        return dict(self.items()).__str__()

    def keys(self):
        return iter(name for name in self.__dict__['__variables'].keys())

    def values(self):
        return iter(value[1] for value in self.__dict__['__variables'].values())

    def items(self):
        return iter((name, value[1]) for name, value in self.__dict__['__variables'].items())

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)

    def __getattr__(self, name):
        if not name in self.__dict__['__variables']:
            raise AttributeError('Attribute {} does not exist.'.format(name))
        return self.__dict__['__variables'][name][1]

    def __delitem__(self, name):
        raise NotImplementedError('Del {} is unimplementable.'.format(name))

    def __setAttributeKnown(self, name, typeAsString, value):
        self.__dict__['__variables'][name] = [typeAsString, value]

    def __setattr__(self, name, value):
        if not name in self.__dict__['__variables']:
            typeAsString = str(type(value).__name__)
        else:
            typeAsString = self.__dict__['__variables'][name][0]
        if not self.isType(value, typeAsString):
            raise AttributeError(
                'Attribute {} is of type {}. Cannot be assigned to {}'.format(name, typeAsString, value))
        self.__setAttributeKnown(name, typeAsString, value)

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

def main():
    pass


if __name__ == '__main__':
    main()
