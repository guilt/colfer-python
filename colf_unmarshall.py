from colf_base import TypeCheckMixin, RawFloatConvertUtils, UTFUtils, ColferConstants


class ColferUnmarshallerMixin(TypeCheckMixin, RawFloatConvertUtils, UTFUtils, ColferConstants):

    def unmarshallHeader(self, value, byteInput, offset):
        offset += 1
        return value, offset

    def unmarshallVarInt(self, byteInput, offset):
        value = 0
        bitShift = 0

        valueAsByte = byteInput[offset]; offset += 1
        while valueAsByte > 0x7f:
            value |= (valueAsByte & 0x7f) << bitShift;
            valueAsByte = byteInput[offset]; offset += 1
            bitShift += 7

        value |= (valueAsByte & 0x7f) << bitShift

        return value, offset

    def unmarshallBool(self, name, index, byteInput, offset):
        if (byteInput[offset] & 0x7f) != index:
            return None, offset

        indexIsSigned = True if byteInput[offset] & 0x80 else False

        offset += 1
        value = True

        return self.unmarshallHeader(value, byteInput, offset)

    def unmarshallUint8(self, name, index, byteInput, offset):
        if (byteInput[offset] & 0x7f) != index:
            return None, offset

        indexIsSigned = True if byteInput[offset] & 0x80 else False

        offset += 1
        value = byteInput[offset]; offset += 1

        return self.unmarshallHeader(value, byteInput, offset)

    def unmarshallUint16(self, name, index, byteInput, offset):
        if (byteInput[offset] & 0x7f) != index:
            return None, offset

        indexIsSigned = True if byteInput[offset] & 0x80 else False

        offset += 1

        if indexIsSigned:
            # Flat - do not use | 0x80. See https://github.com/pascaldekloe/colfer/issues/61
            value = byteInput[offset]; offset += 1
            value = (value << 8) | byteInput(offset); offset += 1
        else:
            # Compressed
            value = byteInput[offset]; offset += 1

        if byteInput[offset] != index:
            return 0, offset

        return self.unmarshallHeader(value, byteInput, offset)

    def unmarshallInt32(self, name, index, byteInput, offset):
        if (byteInput[offset] & 0x7f) != index:
            return None, offset

        indexIsSigned = True if byteInput[offset] & 0x80 else False

        offset += 1

        # Compressed Path
        value, offset = self.unmarshallVarInt(byteInput, offset)
        value = -value if indexIsSigned else value

        return self.unmarshallHeader(value, byteInput, offset)

    def unmarshallListInt32(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallUint32(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallInt64(self, name, index, byteInput, offset):
        if (byteInput[offset] & 0x7f) != index:
            return None, offset

        indexIsSigned = True if byteInput[offset] & 0x80 else False

        offset += 1

        # Compressed Path
        value, offset = self.unmarshallVarInt(byteInput, offset)
        value = -value if indexIsSigned else value

        return self.unmarshallHeader(value, byteInput, offset)

    def unmarshallListInt64(self, name, value, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallUint64(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallFloat32(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallListFloat32(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallFloat64(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallListFloat64(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallTimestamp(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallBinary(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallListBinary(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallString(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallListString(self, name, index, byteInput, offset):
        raise NotImplementedError("Unimplemented Type.")

        return None, offset

    def unmarshallList(self, name, index, byteInput, offset, variableSubType=None):
        STRING_TYPES_MAP = {
            'int32': ColferUnmarshallerMixin.unmarshallListInt32,
            'int64': ColferUnmarshallerMixin.unmarshallListInt64,
            'float32': ColferUnmarshallerMixin.unmarshallListFloat32,
            'float64': ColferUnmarshallerMixin.unmarshallListFloat64,
            'bytes': ColferUnmarshallerMixin.unmarshallListBinary,
            'bytearray': ColferUnmarshallerMixin.unmarshallListBinary,
            'str': ColferUnmarshallerMixin.unmarshallListString,
            'unicode': ColferUnmarshallerMixin.unmarshallListString,
        }

        if variableSubType in STRING_TYPES_MAP:
            functionToCall = STRING_TYPES_MAP[variableSubType]
            return functionToCall(self, name, index, byteInput, offset)

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