import ctypes
import datetime
import json
import sys
from collections import OrderedDict

import six

if sys.version_info[0:2] >= (3, 7):
    long = int


class TypeCheckMixin(object):
    def __isType(self, variable, typesToCheck):
        for typeToCheck in typesToCheck:
            if type(variable) is typeToCheck or isinstance(variable, typeToCheck):
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
        return self.__isType(variable, [six.string_types])

    def isList(self, variable):
        return self.__isType(variable, [list, tuple])

    def isDict(self, variable):
        return self.__isType(variable, [dict])

    def isType(self, variable, variableType):
        STRING_TYPES_MAP = {
            'bool': TypeCheckMixin.isBool,
            'int8': TypeCheckMixin.isInt8,
            'uint8': TypeCheckMixin.isUint8,
            'int16': TypeCheckMixin.isInt16,
            'uint16': TypeCheckMixin.isUint16,
            'int32': TypeCheckMixin.isInt32,
            'uint32': TypeCheckMixin.isUint32,
            'int64': TypeCheckMixin.isInt64,
            'uint64': TypeCheckMixin.isUint64,
            'float32': TypeCheckMixin.isFloat32,
            'float64': TypeCheckMixin.isFloat64,
            'timestamp': TypeCheckMixin.isTimestamp,
            'datetime': TypeCheckMixin.isTimestamp,
            'str': TypeCheckMixin.isString,
            'text': TypeCheckMixin.isString,
            'unicode': TypeCheckMixin.isString,
            'bytes': TypeCheckMixin.isBinary,
            'bytearray': TypeCheckMixin.isBinary,
            'list': TypeCheckMixin.isList,
            'tuple': TypeCheckMixin.isList,
            'dict': TypeCheckMixin.isDict,
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

    def getDict(self):
        return {}

    def getValue(self, variableType):
        STRING_TYPES_MAP = {
            'bool': TypeDeriveValueMixin.getBool,
            'int8': TypeDeriveValueMixin.getInt8,
            'uint8': TypeDeriveValueMixin.getUint8,
            'int16': TypeDeriveValueMixin.getInt16,
            'uint16': TypeDeriveValueMixin.getUint16,
            'int32': TypeDeriveValueMixin.getInt32,
            'uint32': TypeDeriveValueMixin.getUint32,
            'int64': TypeDeriveValueMixin.getInt64,
            'uint64': TypeDeriveValueMixin.getUint64,
            'float32': TypeDeriveValueMixin.getFloat32,
            'float64': TypeDeriveValueMixin.getFloat64,
            'timestamp': TypeDeriveValueMixin.getTimestamp,
            'datetime': TypeDeriveValueMixin.getTimestamp,
            'str': TypeDeriveValueMixin.getString,
            'unicode': TypeDeriveValueMixin.getString,
            'bytes': TypeDeriveValueMixin.getBinary,
            'bytearray': TypeDeriveValueMixin.getBinary,
            'list': TypeDeriveValueMixin.getList,
            'tuple': TypeDeriveValueMixin.getList,
            'dict': TypeDeriveValueMixin.getDict,
        }
        if variableType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableType]
            return functionToCall(self)
        return False


class EntropyUtils(object):

    def getSign(self, value):
        if value >= 0:
            return 0
        return 1

    def getPowerOfTwo(self, power=1):
        if power == long(power) and power >= 0:
            return (long) (1 << power)
        raise ArithmeticError("Only support +ve Integral Powers of Two.")

    def getMaximumUnsigned(self, power=1):
        return self.getPowerOfTwo(power) - 1

    def getComplementaryMaskUnsigned(self, power=1, powerBits = 64):
        assert(powerBits >= power)
        return self.getMaximumUnsigned(powerBits) - self.getMaximumUnsigned(power)


class RawFloatConvertUtils(object):

    def getFloatAsBytes(self, value):
        cFloatValue = ctypes.c_float(value)
        cMemValue = (ctypes.c_byte * 4)()
        ctypes.memmove(cMemValue, ctypes.byref(cFloatValue), 4)
        if sys.byteorder == "little":
            return bytearray(cMemValue)[::-1]
        return bytearray(cMemValue)

    def getBytesAsFloat(self, value):
        if sys.byteorder == "little":
            flippedValue = value[::-1]
        else:
            flippedValue = value
        cMemValue = (ctypes.c_byte * 4)()
        cMemValue[0] = flippedValue[0]
        cMemValue[1] = flippedValue[1]
        cMemValue[2] = flippedValue[2]
        cMemValue[3] = flippedValue[3]
        cFloatValue = ctypes.c_float(0)
        ctypes.memmove(ctypes.byref(cFloatValue), cMemValue, 4)
        return cFloatValue.value

    def getDoubleAsBytes(self, value):
        cDoubleValue = ctypes.c_double(value)
        cMemValue = (ctypes.c_byte * 8)()

        ctypes.memmove(cMemValue, ctypes.byref(cDoubleValue), 8)
        if sys.byteorder == "little":
            return bytearray(cMemValue)[::-1]
        return bytearray(cMemValue)

    def getBytesAsDouble(self, value):
        if sys.byteorder == "little":
            flippedValue = value[::-1]
        else:
            flippedValue = value
        cMemValue = (ctypes.c_byte * 8)()
        cMemValue[0] = flippedValue[0]
        cMemValue[1] = flippedValue[1]
        cMemValue[2] = flippedValue[2]
        cMemValue[3] = flippedValue[3]
        cMemValue[4] = flippedValue[4]
        cMemValue[5] = flippedValue[5]
        cMemValue[6] = flippedValue[6]
        cMemValue[7] = flippedValue[7]
        cDoubleValue = ctypes.c_double(0)
        ctypes.memmove(ctypes.byref(cDoubleValue), cMemValue, 8)
        return cDoubleValue.value


class UTFUtils(EntropyUtils):

    def encodeUTFBytes(self, stringValue):
        stringAsBytes = stringValue.encode('utf-8')
        return stringAsBytes, len(stringAsBytes)


class JsonMixin(TypeCheckMixin):

    def toJson(self):
        return json.dumps(self, default=str)

    def fromJson(self, jsonStr):
        loadedValue = json.loads(jsonStr)
        if self.isDict(loadedValue):
            for key, value in loadedValue.items():
                self.__setattr__(key, value)


class DictMixIn(dict, JsonMixin):

    def __init__(self, *args, **kwargs):
        super(dict, self).__init__(*args, **kwargs)
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

    def validateKnownAttribute(self, name, variableType, value, variableSubType = None):
        return value

    def setKnownAttribute(self, name, variableType, value, variableSubType = None):
        value = self.validateKnownAttribute(name, variableType, value, variableSubType)
        self.__dict__['__variables'][name] = [variableType, value, variableSubType]

    def __setattr__(self, name, value):
        if not name in self.__dict__['__variables']:
            variableType = str(type(value).__name__)
            if self.isList(value) and value:
                variableSubType = str(type(value[0]).__name__)
            else:
                variableSubType = None
        else:
            variableType = self.__dict__['__variables'][name][0]
            variableSubType = self.__dict__['__variables'][name][2]
        value = self.validateKnownAttribute(name, variableType, value, variableSubType)
        self.__dict__['__variables'][name] = [variableType, value, variableSubType]

    def setAttribute(self, name, value):
        return self.__setattr__(name, value)

    def toJson(self):
        return json.dumps(dict(self.items()), default=str)


class ColferConstants(object):
    COLFER_MAX_INDEX = 127
    COLFER_MAX_SIZE = 16 * 1024 * 1024
    COLFER_LIST_MAX = 64 * 1024


class ColferMarshallerMixin(TypeCheckMixin, RawFloatConvertUtils, UTFUtils, ColferConstants):

    def marshallHeader(self, byteOutput, offset):
        byteOutput[offset] = 0x7f; offset += 1
        return offset

    def marshallBool(self, name, value, index, byteOutput, offset):

        if value:
            byteOutput[offset] = index; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallUint8(self, name, value, index, byteOutput, offset):

        if value != 0:
            byteOutput[offset] = index; offset += 1
            byteOutput[offset] = value & 0xff; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallUint16(self, name, value, index, byteOutput, offset):
        if value != 0:

            if (value & self.getComplementaryMaskUnsigned(8, 16)) != 0:
                # Flat - do not use | 0x80. See https://github.com/pascaldekloe/colfer/issues/61
                byteOutput[offset] = index; offset += 1
                byteOutput[offset] = (value >> 8) & 0xff; offset += 1
                byteOutput[offset] = value & 0xff; offset += 1
            else:
                # Compressed
                byteOutput[offset] = (index | 0x80); offset += 1
                byteOutput[offset] = value & 0xff; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallInt32(self, name, value, index, byteOutput, offset):
        if value != 0:

            if value < 0:
                value = -value
                byteOutput[offset] = (index | 0x80); offset += 1
            else:
                byteOutput[offset] = index; offset += 1

            # Compressed Path
            while value > 0x7f:
                byteOutput[offset] = (value & 0x7f) | 0x80; offset += 1
                value >>= 7
            byteOutput[offset] = value & 0xff; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallListInt32(self, name, value, index, byteOutput, offset):
        valueLength = len(value)

        if valueLength != 0:
            assert (valueLength < ColferConstants.COLFER_LIST_MAX)

            byteOutput[offset] = index; offset += 1

            # Compressed Path
            while valueLength > 0x7f:
                byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                value >>= 7
            byteOutput[offset] = valueLength & 0xff; offset += 1

            for valueElement in value:
                # Move last bit to the end
                valueElementEncoded = ((valueElement << 1) & 0xffffffff) ^ ((valueElement >> 31) & 0x00000001)
                # Compressed Path
                while valueElementEncoded > 0x7f:
                    byteOutput[offset] = (valueElementEncoded & 0x7f) | 0x80; offset += 1
                    valueElementEncoded >>= 7
                byteOutput[offset] = valueElementEncoded & 0xff; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallUint32(self, name, value, index, byteOutput, offset):

        if value != 0:
            if (value & self.getComplementaryMaskUnsigned(21, 32)) != 0:
                # Flat
                byteOutput[offset] = index | 0x80; offset += 1
                byteOutput[offset] = (value >> 24) & 0xff; offset += 1
                byteOutput[offset] = (value >> 16) & 0xff; offset += 1
                byteOutput[offset] = (value >> 8) & 0xff; offset += 1
                byteOutput[offset] = value & 0xff; offset += 1
            else:
                # Compressed Path - do not use | 0x80
                byteOutput[offset] = index; offset += 1
                while value > 0x7f:
                    byteOutput[offset] = (value & 0x7f) | 0x80; offset += 1
                    value >>= 7
                byteOutput[offset] = value & 0xff; offset += 1

            offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallInt64(self, name, value, index, byteOutput, offset):
        if value != 0:

            if value < 0:
                value = -value
                byteOutput[offset] = (index | 0x80); offset += 1
            else:
                byteOutput[offset] = index; offset += 1

            # Compressed Path
            while value > 0x7f:
                byteOutput[offset] = (value & 0x7f) | 0x80; offset += 1
                value >>= 7
            byteOutput[offset] = value & 0xff; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallListInt64(self, name, value, index, byteOutput, offset):
        valueLength = len(value)

        if valueLength != 0:
            assert (valueLength < ColferConstants.COLFER_LIST_MAX)

            byteOutput[offset] = index; offset += 1

            # Compressed Path
            while valueLength > 0x7f:
                byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                value >>= 7
            byteOutput[offset] = valueLength & 0xff; offset += 1

            for valueElement in value:
                # Move last bit to the end
                valueElementEncoded = ((valueElement << 1) & 0xffffffffffffffff) ^ ((valueElement >> 63) & 0x0000000000000001)
                # Compressed Path
                writtenBytes = 0
                while valueElementEncoded > 0x7f and writtenBytes < 8:
                    byteOutput[offset] = (valueElementEncoded & 0x7f) | 0x80; offset += 1
                    valueElementEncoded >>= 7
                    writtenBytes += 1
                byteOutput[offset] = valueElementEncoded & 0xff; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallUint64(self, name, value, index, byteOutput, offset):
        if value != 0:
            if (value & self.getComplementaryMaskUnsigned(49)) != 0:
                # Flat
                byteOutput[offset] = index | 0x80; offset += 1
                byteOutput[offset] = (value >> 56) & 0xff; offset += 1
                byteOutput[offset] = (value >> 48) & 0xff; offset += 1
                byteOutput[offset] = (value >> 40) & 0xff; offset += 1
                byteOutput[offset] = (value >> 32) & 0xff; offset += 1
                byteOutput[offset] = (value >> 24) & 0xff; offset += 1
                byteOutput[offset] = (value >> 16) & 0xff; offset += 1
                byteOutput[offset] = (value >> 8) & 0xff; offset += 1
                byteOutput[offset] = value & 0xff; offset += 1
            else:
                # Compressed Path - do not use | 0x80
                byteOutput[offset] = index; offset += 1
                while value > 0x7f:
                    byteOutput[offset] = (value & 0x7f) | 0x80; offset += 1
                    value >>= 7
                byteOutput[offset] = value & 0xff; offset += 1

            offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallFloat32(self, name, value, index, byteOutput, offset):
        valueAsBytes = self.getFloatAsBytes(value)
        for valueAsByte in valueAsBytes:
            byteOutput[offset] = valueAsByte; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallListFloat32(self, name, value, index, byteOutput, offset):
        valueLength = len(value)

        if valueLength != 0:
            assert (valueLength < ColferConstants.COLFER_LIST_MAX)

            byteOutput[offset] = index; offset += 1

            # Compressed Path
            while valueLength > 0x7f:
                byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                value >>= 7
            byteOutput[offset] = valueLength & 0xff; offset += 1

            for valueElement in value:
                valueAsBytes = self.getFloatAsBytes(valueElement)
                for valueAsByte in valueAsBytes:
                    byteOutput[offset] = valueAsByte; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallFloat64(self, name, value, index, byteOutput, offset):
        valueAsBytes = self.getDoubleAsBytes(value)
        for valueAsByte in valueAsBytes:
            byteOutput[offset] = valueAsByte; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallListFloat64(self, name, value, index, byteOutput, offset):
        valueLength = len(value)

        if valueLength != 0:
            assert (valueLength < ColferConstants.COLFER_LIST_MAX)

            byteOutput[offset] = index; offset += 1

            # Compressed Path
            while valueLength > 0x7f:
                byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                value >>= 7
            byteOutput[offset] = valueLength & 0xff; offset += 1

            for valueElement in value:
                valueAsBytes = self.getDoubleAsBytes(valueElement)
                for valueAsByte in valueAsBytes:
                    byteOutput[offset] = valueAsByte; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallTimestamp(self, name, value, index, byteOutput, offset):
        timeDelta = value - datetime.datetime.utcfromtimestamp(0)
        nanoSeconds = timeDelta.microseconds * (10**3)
        seconds = timeDelta.seconds + (timeDelta.days * 24 * 3600)
        if nanoSeconds != 0 and seconds != 0:
            if (seconds & self.getComplementaryMaskUnsigned(32)) != 0:
                # Flat
                byteOutput[offset] += index | 0x80; offset += 1
                byteOutput[offset] += (seconds >> 56) & 0xff; offset += 1
                byteOutput[offset] += (seconds >> 48) & 0xff; offset += 1
                byteOutput[offset] += (seconds >> 40) & 0xff; offset += 1
                byteOutput[offset] += (seconds >> 32) & 0xff; offset += 1
                byteOutput[offset] += (seconds >> 24) & 0xff; offset += 1
                byteOutput[offset] += (seconds >> 16) & 0xff; offset += 1
                byteOutput[offset] += (seconds >> 8) & 0xff; offset += 1
                byteOutput[offset] += (seconds) & 0xff; offset += 1

                byteOutput[offset] += (nanoSeconds >> 24) & 0xff; offset += 1
                byteOutput[offset] += (nanoSeconds >> 16) & 0xff; offset += 1
                byteOutput[offset] += (nanoSeconds >> 8) & 0xff; offset += 1
                byteOutput[offset] += (nanoSeconds) & 0xff; offset += 1
            else:
                # Compressed Path
                byteOutput[offset] += index; offset += 1
                byteOutput[offset] += (seconds >> 24) & 0xff; offset += 1
                byteOutput[offset] += (seconds >> 16) & 0xff; offset += 1
                byteOutput[offset] += (seconds >> 8) & 0xff; offset += 1
                byteOutput[offset] += (seconds) & 0xff; offset += 1

                byteOutput[offset] += (nanoSeconds >> 24) & 0xff; offset += 1
                byteOutput[offset] += (nanoSeconds >> 16) & 0xff; offset += 1
                byteOutput[offset] += (nanoSeconds >> 8) & 0xff; offset += 1
                byteOutput[offset] += (nanoSeconds) & 0xff; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallBinary(self, name, value, index, byteOutput, offset):
        valueLength = len(value)
        if valueLength != 0:
            assert(valueLength <= ColferConstants.COLFER_MAX_SIZE)

            # Compressed Path
            byteOutput[offset] = index; offset += 1
            while valueLength > 0x7f:
                byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                valueLength >>= 7
            byteOutput[offset] = valueLength & 0xff; offset += 1

            # Flat
            for valueAsByte in value:
                byteOutput[offset] = valueAsByte; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallListBinary(self, name, value, index, byteOutput, offset):
        valueLength = len(value)
        if valueLength != 0:
            assert(valueLength <= ColferConstants.COLFER_LIST_MAX)

            # Compressed Path
            byteOutput[offset] = index; offset += 1
            while valueLength > 0x7f:
                byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                valueLength >>= 7
            byteOutput[offset] = valueLength & 0xff; offset += 1

            # Flat
            for valueAsBytes in value:
                valueLength = len(valueAsBytes)
                assert (valueLength <= ColferConstants.COLFER_MAX_SIZE)

                # Compressed Path
                byteOutput[offset] = index; offset += 1
                while valueLength > 0x7f:
                    byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                    valueLength >>= 7
                byteOutput[offset] = valueLength & 0xff; offset += 1

                # Flat
                for valueAsByte in valueAsBytes:
                    byteOutput[offset] = valueAsByte; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallString(self, name, value, index, byteOutput, offset):
        valueLength = len(value)
        if valueLength != 0:
            assert(valueLength <= ColferConstants.COLFER_MAX_SIZE)

            # Compressed Path
            byteOutput[offset] = index; offset += 1

            valueAsBytes, valueLength = self.encodeUTFBytes(value)
            assert(valueLength <= self.COLFER_MAX_SIZE)

            while valueLength > 0x7f:
                byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                valueLength >>= 7
            byteOutput[offset] = valueLength & 0xff; offset += 1

            # Flat
            index = 0
            while index < valueLength:
                valueAsByte = valueAsBytes[index]; index += 1
                byteOutput[offset] = valueAsByte; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallListString(self, name, value, index, byteOutput, offset):
        valueLength = len(value)

        if valueLength != 0:
            assert(valueLength <= ColferConstants.COLFER_LIST_MAX)

            byteOutput[offset] = index; offset += 1

            # Compressed Path
            while valueLength > 0x7f:
                byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                valueLength >>= 7
            byteOutput[offset] = valueLength & 0xff; offset += 1

            #Flat
            for valueAsString in value:
                valueLength = len(valueAsString)
                assert (valueLength <= ColferConstants.COLFER_MAX_SIZE)

                valueAsBytes, valueLength = self.encodeUTFBytes(valueAsString)
                assert (valueLength <= self.COLFER_MAX_SIZE)

                # Compressed Path
                while valueLength > 0x7f:
                    byteOutput[offset] = (valueLength & 0x7f) | 0x80; offset += 1
                    valueLength >>= 7
                byteOutput[offset] = valueLength & 0xff; offset += 1

                # Flat
                index = 0
                while index < valueLength:
                    valueAsByte = valueAsBytes[index]; index += 1
                    byteOutput[offset] = valueAsByte; offset += 1

        return self.marshallHeader(byteOutput, offset)

    def marshallList(self, name, value, index, byteOutput, offset, variableSubType=None):
        STRING_TYPES_MAP = {
            'int32': ColferMarshallerMixin.marshallListInt32,
            'int64': ColferMarshallerMixin.marshallListInt64,
            'float32': ColferMarshallerMixin.marshallListFloat32,
            'float64': ColferMarshallerMixin.marshallListFloat64,
            'bytes': ColferMarshallerMixin.marshallListBinary,
            'bytearray': ColferMarshallerMixin.marshallListBinary,
            'str': ColferMarshallerMixin.marshallListString,
            'unicode': ColferMarshallerMixin.marshallListString,
        }

        if variableSubType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableSubType]
            return functionToCall(self, name, value, index, byteOutput, offset)

        return offset

    def marshallType(self, name, variableType, variableSubType, value, index, byteOutput, offset):
        STRING_TYPES_MAP = {
            'bool': ColferMarshallerMixin.marshallBool,
            'uint8': ColferMarshallerMixin.marshallUint8,
            'uint16': ColferMarshallerMixin.marshallUint16,
            'int32': ColferMarshallerMixin.marshallInt32,
            'uint32': ColferMarshallerMixin.marshallUint32,
            'int64': ColferMarshallerMixin.marshallInt64,
            'uint64': ColferMarshallerMixin.marshallUint64,
            'float32': ColferMarshallerMixin.marshallFloat32,
            'float64': ColferMarshallerMixin.marshallFloat64,
            'timestamp': ColferMarshallerMixin.marshallTimestamp,
            'datetime': ColferMarshallerMixin.marshallTimestamp,
            'str': ColferMarshallerMixin.marshallString,
            'unicode': ColferMarshallerMixin.marshallString,
            'bytes': ColferMarshallerMixin.marshallBinary,
            'bytearray': ColferMarshallerMixin.marshallBinary,
            'list': ColferMarshallerMixin.marshallList,
            'tuple': ColferMarshallerMixin.marshallList,
        }
        if variableSubType:
            functionToCall = STRING_TYPES_MAP[variableType]
            return functionToCall(self, name, value, index, byteOutput, offset, variableSubType)
        if variableType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableType]
            return functionToCall(self, name, value, index, byteOutput, offset)
        return offset

    def marshall(self, byteOutput, offset=0):
        assert (byteOutput != None)
        assert (self.isBinary(byteOutput, True))
        assert (offset >= 0)
        index = 0
        for name in dir(self):
            variableType, value, variableSubType = self.getAttributeWithType(name)
            offset = self.marshallType(name, variableType, variableSubType, value, index, byteOutput, offset)
            index += 1
        return offset

    def getAttributeWithType(self, name):
        value = self.__getattr__(name)
        valueType = str(type(value).__name__)
        valueSubType = None
        return valueType, value. valueSubType


class ColferUnmarshallerMixin(TypeCheckMixin, RawFloatConvertUtils, UTFUtils, ColferConstants):

    def unmarshallHeader(self, value, byteInput, offset):
        offset += 1
        return value, offset

    def unmarshallBool(self, name, index, byteInput, offset):

        if byteInput[offset] != index:
            return None, offset

        offset += 1
        value = True

        return self.unmarshallHeader(value, byteInput, offset)

    def unmarshallUint8(self, name, index, byteInput, offset):
        if byteInput[offset] != index:
            return 0, offset

        offset += 1
        value = byteInput[offset]; offset += 1

        # Unsigned-Ness
        if (value < 0):
            value = (256 + value)

        return self.unmarshallHeader(value, byteInput, offset)

    def unmarshallUint16(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallInt32(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallUint32(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallInt64(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallUint64(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallFloat32(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallFloat64(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallTimestamp(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallBinary(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallString(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallList(self, name, index, byteInput, offset, variableSubType=None):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallType(self, name, variableType, variableSubType, index, byteInput, offset):
        STRING_TYPES_MAP = {
            'bool': ColferUnmarshallerMixin.unmarshallBool,
            'uint8': ColferUnmarshallerMixin.unmarshallUint8,
            'uint16': ColferUnmarshallerMixin.unmarshallUint16,
            'int32': ColferUnmarshallerMixin.unmarshallInt32,
            'uint32': ColferUnmarshallerMixin.unmarshallUint32,
            'int64': ColferUnmarshallerMixin.unmarshallInt64,
            'uint64': ColferUnmarshallerMixin.unmarshallUint64,
            'float32': ColferUnmarshallerMixin.unmarshallFloat32,
            'float64': ColferUnmarshallerMixin.unmarshallFloat64,
            'datetime': ColferUnmarshallerMixin.unmarshallTimestamp,
            'str': ColferUnmarshallerMixin.unmarshallString,
            'unicode': ColferUnmarshallerMixin.unmarshallString,
            'bytes': ColferUnmarshallerMixin.unmarshallBinary,
            'bytearray': ColferUnmarshallerMixin.unmarshallBinary,
            'list': ColferUnmarshallerMixin.unmarshallList,
            'tuple': ColferUnmarshallerMixin.unmarshallList,
        }
        if variableSubType:
            functionToCall = STRING_TYPES_MAP[variableType]
            return functionToCall(self, name, index, byteInput, offset, variableSubType)
        if variableType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableType]
            return functionToCall(self, name, index, byteInput, offset)
        return None, offset

    def unmarshall(self, byteInput, offset=0):
        assert (byteInput != None)
        assert (self.isBinary(byteInput))
        assert (offset >= 0)
        index = 0
        for name in dir(self):
            variableType, _, variableSubType = self.getAttributeWithType(name)
            try:
                newValue, offset = self.unmarshallType(name, variableType, variableSubType, index, byteInput, offset)
                self.setKnownAttribute(name, variableType, newValue)
            except NotImplementedError:
                pass
            index += 1
        return self, offset

    def getAttributeWithType(self, name):
        value = self.__getattr__(name)
        valueType = str(type(value).__name__)
        return valueType, value

    def setKnownAttribute(self, name, variableType, value, variableSubType=None):
        self.__setattr__(name, value)


class Colfer(DictMixIn, TypeDeriveValueMixin, ColferMarshallerMixin, ColferUnmarshallerMixin):

    def __delitem__(self, name):
        raise NotImplementedError('Del {} is unimplementable.'.format(name))

    def validateKnownAttribute(self, name, variableType, value, variableSubType = None):
        if value is not None:
            if not self.isType(value, variableType):
                raise AttributeError('Attribute {} is of type {}. Cannot be assigned to {}'.format(name, variableType, value))
            if variableSubType and self.isList(value):
                for valueSub in value:
                    if not self.isType(valueSub, variableSubType):
                        raise AttributeError('Attribute {} is of type {}:{}. Cannot be assigned to {}'.format(name, variableType, variableSubType, valueSub))
        else:
            value = self.getValue(variableType)
        return value

    def declareAttribute(self, name, variableType, value=None, variableSubType=None):
        if name is None or variableType is None or type(variableType) is not str:
            raise AttributeError('Must declare a valid attribute and type')
        if name in dir(self):
            raise AttributeError('Cannot declare attribute {} again'.format(name))
        self.setKnownAttribute(name, variableType, value, variableSubType)
