#!/usr/bin/env python3

import datetime
import sys
from collections import OrderedDict

import six

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
        return self.__isType(variable, [datetime.datetime])

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


class TypeDeriveValueMixin(object):

    def getBool(self):
        return False

    def getInt8(self):
        return 0

    def getUint8(self):
        return 0

    def getInt16(self):
        return 0

    def getUint16(self):
        return 0

    def getInt32(self):
        return 0

    def getUint32(self):
        return 0

    def getInt64(self):
        return 0

    def getUint64(self):
        return 0

    def getFloat32(self):
        return 0.0

    def getFloat64(self):
        return 0.0

    def getTimestamp(self):
        return datetime.datetime.utcfromtimestamp(0)

    def getBinary(self):
        return b''

    def getString(self):
        return ''

    def getList(self):
        return []

    def getValue(self, variableType):
        STRING_TYPES_MAP = {
            'bool': TypeDeriveValueMixin.getBool,
            'Bool': TypeDeriveValueMixin.getBool,

            'boolean': TypeDeriveValueMixin.getBool,
            'Boolean': TypeDeriveValueMixin.getBool,

            'byte': TypeDeriveValueMixin.getUint8,
            'Byte': TypeDeriveValueMixin.getUint8,

            'int8': TypeDeriveValueMixin.getInt8,
            'Int8': TypeDeriveValueMixin.getInt8,

            'uint8': TypeDeriveValueMixin.getUint8,
            'Uint8': TypeDeriveValueMixin.getUint8,

            'int16': TypeDeriveValueMixin.getInt16,
            'Int16': TypeDeriveValueMixin.getInt16,

            'uint16': TypeDeriveValueMixin.getUint16,
            'Uint16': TypeDeriveValueMixin.getUint16,

            'int32': TypeDeriveValueMixin.getInt32,
            'Int32': TypeDeriveValueMixin.getInt32,

            'uint32': TypeDeriveValueMixin.getUint32,
            'Uint32': TypeDeriveValueMixin.getUint32,

            'int64': TypeDeriveValueMixin.getInt64,
            'Int64': TypeDeriveValueMixin.getInt64,

            'uint64': TypeDeriveValueMixin.getUint64,
            'Uint64': TypeDeriveValueMixin.getUint64,

            'float32': TypeDeriveValueMixin.getFloat32,
            'Float32': TypeDeriveValueMixin.getFloat32,

            'float64': TypeDeriveValueMixin.getFloat64,
            'Float64': TypeDeriveValueMixin.getFloat64,

            'timestamp': TypeDeriveValueMixin.getTimestamp,
            'Timestamp': TypeDeriveValueMixin.getTimestamp,
            'TimeStamp': TypeDeriveValueMixin.getTimestamp,

            'datetime': TypeDeriveValueMixin.getTimestamp,
            'Datetime': TypeDeriveValueMixin.getTimestamp,
            'DateTime': TypeDeriveValueMixin.getTimestamp,

            'str': TypeDeriveValueMixin.getString,
            'Str': TypeDeriveValueMixin.getString,

            'string': TypeDeriveValueMixin.getString,
            'String': TypeDeriveValueMixin.getString,

            'text': TypeDeriveValueMixin.getString,
            'Text': TypeDeriveValueMixin.getString,

            'unicode': TypeDeriveValueMixin.getString,
            'Unicode': TypeDeriveValueMixin.getString,

            'binary': TypeDeriveValueMixin.getBinary,
            'Binary': TypeDeriveValueMixin.getBinary,

            'bytes': TypeDeriveValueMixin.getBinary,
            'Bytes': TypeDeriveValueMixin.getBinary,

            'bytearray': TypeDeriveValueMixin.getBinary,
            'Bytearray': TypeDeriveValueMixin.getBinary,
            'ByteArray': TypeDeriveValueMixin.getBinary,

            'list': TypeDeriveValueMixin.getList,
            'List': TypeDeriveValueMixin.getList,

            'tuple': TypeDeriveValueMixin.getList,
            'Tuple': TypeDeriveValueMixin.getList,
        }
        if variableType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableType]
            return functionToCall(self)
        return False


class ColferMarshallerMixin(object):

    def marshallBool(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallInt8(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallUint8(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallInt16(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallUint16(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallInt32(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallUint32(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallInt64(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallUint64(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallFloat32(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallFloat64(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallTimestamp(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallBinary(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallString(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallList(self, name, variableValue, byteOutput, offset):
        return offset

    def marshallType(self, name, variableType, variableValue, byteOutput, offset):
        STRING_TYPES_MAP = {
            'bool': ColferMarshallerMixin.marshallBool,
            'Bool': ColferMarshallerMixin.marshallBool,

            'boolean': ColferMarshallerMixin.marshallBool,
            'Boolean': ColferMarshallerMixin.marshallBool,

            'byte': ColferMarshallerMixin.marshallUint8,
            'Byte': ColferMarshallerMixin.marshallUint8,

            'int8': ColferMarshallerMixin.marshallInt8,
            'Int8': ColferMarshallerMixin.marshallInt8,

            'uint8': ColferMarshallerMixin.marshallUint8,
            'Uint8': ColferMarshallerMixin.marshallUint8,

            'int16': ColferMarshallerMixin.marshallInt16,
            'Int16': ColferMarshallerMixin.marshallInt16,

            'uint16': ColferMarshallerMixin.marshallUint16,
            'Uint16': ColferMarshallerMixin.marshallUint16,

            'int32': ColferMarshallerMixin.marshallInt32,
            'Int32': ColferMarshallerMixin.marshallInt32,

            'uint32': ColferMarshallerMixin.marshallUint32,
            'Uint32': ColferMarshallerMixin.marshallUint32,

            'int64': ColferMarshallerMixin.marshallInt64,
            'Int64': ColferMarshallerMixin.marshallInt64,

            'uint64': ColferMarshallerMixin.marshallUint64,
            'Uint64': ColferMarshallerMixin.marshallUint64,

            'float32': ColferMarshallerMixin.marshallFloat32,
            'Float32': ColferMarshallerMixin.marshallFloat32,

            'float64': ColferMarshallerMixin.marshallFloat64,
            'Float64': ColferMarshallerMixin.marshallFloat64,

            'timestamp': ColferMarshallerMixin.marshallTimestamp,
            'Timestamp': ColferMarshallerMixin.marshallTimestamp,
            'TimeStamp': ColferMarshallerMixin.marshallTimestamp,

            'datetime': ColferMarshallerMixin.marshallTimestamp,
            'Datetime': ColferMarshallerMixin.marshallTimestamp,
            'DateTime': ColferMarshallerMixin.marshallTimestamp,

            'str': ColferMarshallerMixin.marshallString,
            'Str': ColferMarshallerMixin.marshallString,

            'string': ColferMarshallerMixin.marshallString,
            'String': ColferMarshallerMixin.marshallString,

            'text': ColferMarshallerMixin.marshallString,
            'Text': ColferMarshallerMixin.marshallString,

            'unicode': ColferMarshallerMixin.marshallString,
            'Unicode': ColferMarshallerMixin.marshallString,

            'binary': ColferMarshallerMixin.marshallBinary,
            'Binary': ColferMarshallerMixin.marshallBinary,

            'bytes': ColferMarshallerMixin.marshallBinary,
            'Bytes': ColferMarshallerMixin.marshallBinary,

            'bytearray': ColferMarshallerMixin.marshallBinary,
            'Bytearray': ColferMarshallerMixin.marshallBinary,
            'ByteArray': ColferMarshallerMixin.marshallBinary,

            'list': ColferMarshallerMixin.marshallList,
            'List': ColferMarshallerMixin.marshallList,

            'tuple': ColferMarshallerMixin.marshallList,
            'Tuple': ColferMarshallerMixin.marshallList,
        }
        if variableType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableType]
            # print('Marshalling: {}:{}={} @{} Invoke: {}'.format(name, variableType, variableValue, offset,
            #                                                    functionToCall))
            return functionToCall(self, name, variableValue, byteOutput, offset)
        return offset

    def marshall(self, byteOutput, offset=0):
        assert (byteOutput != None)
        assert (self.isBinary(byteOutput, True))
        assert (offset >= 0)
        for name in dir(self):
            variableType, value = self.getAttributeWithType(name)
            offset = self.marshallType(name, variableType, value, byteOutput, offset)
        return offset

    def getAttributeWithType(self, name):
        value = self.__getattr__(name)
        valueType = str(type(value).__name__)
        return valueType, value


class ColferUnmarshallerMixin(object):

    def unmarshallBool(self, name, byteInput, offset):
        return None, offset

    def unmarshallInt8(self, name, byteInput, offset):
        return None, offset

    def unmarshallUint8(self, name, byteInput, offset):
        return None, offset

    def unmarshallInt16(self, name, byteInput, offset):
        return None, offset

    def unmarshallUint16(self, name, byteInput, offset):
        return None, offset

    def unmarshallInt32(self, name, byteInput, offset):
        return None, offset

    def unmarshallUint32(self, name, byteInput, offset):
        return None, offset

    def unmarshallInt64(self, name, byteInput, offset):
        return None, offset

    def unmarshallUint64(self, name, byteInput, offset):
        return None, offset

    def unmarshallFloat32(self, name, byteInput, offset):
        return None, offset

    def unmarshallFloat64(self, name, byteInput, offset):
        return None, offset

    def unmarshallTimestamp(self, name, byteInput, offset):
        return None, offset

    def unmarshallBinary(self, name, byteInput, offset):
        return None, offset

    def unmarshallString(self, name, byteInput, offset):
        return None, offset

    def unmarshallList(self, name, byteInput, offset):
        return None, offset

    def unmarshallType(self, name, variableType, byteInput, offset):
        STRING_TYPES_MAP = {
            'bool': ColferUnmarshallerMixin.unmarshallBool,
            'Bool': ColferUnmarshallerMixin.unmarshallBool,

            'boolean': ColferUnmarshallerMixin.unmarshallBool,
            'Boolean': ColferUnmarshallerMixin.unmarshallBool,

            'byte': ColferUnmarshallerMixin.unmarshallUint8,
            'Byte': ColferUnmarshallerMixin.unmarshallUint8,

            'int8': ColferUnmarshallerMixin.unmarshallInt8,
            'Int8': ColferUnmarshallerMixin.unmarshallInt8,

            'uint8': ColferUnmarshallerMixin.unmarshallUint8,
            'Uint8': ColferUnmarshallerMixin.unmarshallUint8,

            'int16': ColferUnmarshallerMixin.unmarshallInt16,
            'Int16': ColferUnmarshallerMixin.unmarshallInt16,

            'uint16': ColferUnmarshallerMixin.unmarshallUint16,
            'Uint16': ColferUnmarshallerMixin.unmarshallUint16,

            'int32': ColferUnmarshallerMixin.unmarshallInt32,
            'Int32': ColferUnmarshallerMixin.unmarshallInt32,

            'uint32': ColferUnmarshallerMixin.unmarshallUint32,
            'Uint32': ColferUnmarshallerMixin.unmarshallUint32,

            'int64': ColferUnmarshallerMixin.unmarshallInt64,
            'Int64': ColferUnmarshallerMixin.unmarshallInt64,

            'uint64': ColferUnmarshallerMixin.unmarshallUint64,
            'Uint64': ColferUnmarshallerMixin.unmarshallUint64,

            'float32': ColferUnmarshallerMixin.unmarshallFloat32,
            'Float32': ColferUnmarshallerMixin.unmarshallFloat32,

            'float64': ColferUnmarshallerMixin.unmarshallFloat64,
            'Float64': ColferUnmarshallerMixin.unmarshallFloat64,

            'timestamp': ColferUnmarshallerMixin.unmarshallTimestamp,
            'Timestamp': ColferUnmarshallerMixin.unmarshallTimestamp,
            'TimeStamp': ColferUnmarshallerMixin.unmarshallTimestamp,

            'datetime': ColferUnmarshallerMixin.unmarshallTimestamp,
            'Datetime': ColferUnmarshallerMixin.unmarshallTimestamp,
            'DateTime': ColferUnmarshallerMixin.unmarshallTimestamp,

            'str': ColferUnmarshallerMixin.unmarshallString,
            'Str': ColferUnmarshallerMixin.unmarshallString,

            'string': ColferUnmarshallerMixin.unmarshallString,
            'String': ColferUnmarshallerMixin.unmarshallString,

            'text': ColferUnmarshallerMixin.unmarshallString,
            'Text': ColferUnmarshallerMixin.unmarshallString,

            'unicode': ColferUnmarshallerMixin.unmarshallString,
            'Unicode': ColferUnmarshallerMixin.unmarshallString,

            'binary': ColferUnmarshallerMixin.unmarshallBinary,
            'Binary': ColferUnmarshallerMixin.unmarshallBinary,

            'bytes': ColferUnmarshallerMixin.unmarshallBinary,
            'Bytes': ColferUnmarshallerMixin.unmarshallBinary,

            'bytearray': ColferUnmarshallerMixin.unmarshallBinary,
            'Bytearray': ColferUnmarshallerMixin.unmarshallBinary,
            'ByteArray': ColferUnmarshallerMixin.unmarshallBinary,

            'list': ColferUnmarshallerMixin.unmarshallList,
            'List': ColferUnmarshallerMixin.unmarshallList,

            'tuple': ColferUnmarshallerMixin.unmarshallList,
            'Tuple': ColferUnmarshallerMixin.unmarshallList,
        }
        if variableType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableType]
            # print('Unmarshalling: {}:{} @{} Invoke: {}'.format(name, variableType, offset, functionToCall))
            return functionToCall(self, name, byteInput, offset)
        return None, offset

    def unmarshall(self, byteInput, offset=0):
        assert (byteInput != None)
        assert (self.isBinary(byteInput))
        assert (offset >= 0)
        for name in dir(self):
            variableType, _ = self.getAttributeWithType(name)
            newValue, offset = self.unmarshallType(name, variableType, byteInput, offset)
            self.setKnownAttribute(name, variableType, newValue)
        return self, offset

    def getAttributeWithType(self, name):
        value = self.__getattr__(name)
        valueType = str(type(value).__name__)
        return valueType, value

    def setKnownAttribute(self, name, variableType, value):
        self.__dict__['__variables'][name] = [variableType, value]


class DictMixIn(dict):

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

    def setKnownAttribute(self, name, variableType, value):
        self.__dict__['__variables'][name] = [variableType, value]

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)

    def __delitem__(self, name):
        del self.__dict__['__variables'][name]

    def __getattr__(self, name):
        if not name in self.__dict__['__variables']:
            raise AttributeError('Attribute {} does not exist.'.format(name))
        return self.__dict__['__variables'][name][1]

    def getAttribute(self, name):
        return self.__getattr__(name)

    def getAttributeWithType(self, name):
        return self.__dict__['__variables'][name]

    def __setattr__(self, name, value):
        if not name in self.__dict__['__variables']:
            variableType = str(type(value).__name__)
        else:
            variableType = self.__dict__['__variables'][name][0]
        self.setKnownAttribute(name, variableType, value)

    def setAttribute(self, name, value):
        return self.__setattr__(name, value)


class Colfer(DictMixIn, TypeCheckMixin, TypeDeriveValueMixin, ColferMarshallerMixin, ColferUnmarshallerMixin):

    def __delitem__(self, name):
        raise NotImplementedError('Del {} is unimplementable.'.format(name))

    def setKnownAttribute(self, name, variableType, value):
        if value is not None:
            if not self.isType(value, variableType):
                raise AttributeError(
                    'Attribute {} is of type {}. Cannot be assigned to {}'.format(name, variableType, value))
        else:
            value = self.getValue(variableType)
        super().setKnownAttribute(name, variableType, value)

    def declareAttribute(self, name, variableType, value=None):
        if name is None or variableType is None or type(variableType) is not str:
            raise AttributeError('Must declare a valid attribute and type')
        if name in self.__dict__['__variables']:
            raise AttributeError('Cannot declare attribute {} again'.format(name))
        if value is not None:
            if not self.isType(value, variableType):
                raise AttributeError(
                    'Attribute {} is of type {}. Cannot be assigned to {}'.format(name, variableType, value))
        else:
            value = self.getValue(variableType)
        self.__dict__['__variables'][name] = [variableType, value]
