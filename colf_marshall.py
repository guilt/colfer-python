import datetime

from colf_base import TypeCheckMixin, RawFloatConvertUtils, UTFUtils, ColferConstants


class ColferMarshallerMixin(TypeCheckMixin, RawFloatConvertUtils, UTFUtils, ColferConstants):

    def marshallHeader(self, byteOutput, offset):
        byteOutput[offset] = 0x7f; offset += 1
        return offset

    def marshallVarInt(self, value, byteOutput, offset, limit=-1):
        if limit > 0:
            while value > 0x7f and limit:
                byteOutput[offset] = (value & 0x7f) | 0x80; offset += 1
                value >>= 7; limit -= 1
        else:
            while value > 0x7f:
                byteOutput[offset] = (value & 0x7f) | 0x80; offset += 1
                value >>= 7
        byteOutput[offset] = value & 0xff; offset += 1
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
                # Flat - do not use | 0x80. See y
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
            offset = self.marshallVarInt(value, byteOutput, offset)

        return self.marshallHeader(byteOutput, offset)

    def marshallListInt32(self, name, value, index, byteOutput, offset):
        valueLength = len(value)

        if valueLength != 0:
            assert (valueLength < ColferConstants.COLFER_LIST_MAX)

            byteOutput[offset] = index; offset += 1

            # Compressed Path
            offset = self.marshallVarInt(valueLength, byteOutput, offset)

            for valueElement in value:
                # Move last bit to the end
                valueElementEncoded = ((valueElement << 1) & 0xffffffff) ^ ((valueElement >> 31) & 0x00000001)
                # Compressed Path
                offset = self.marshallVarInt(valueElementEncoded, byteOutput, offset)

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
                offset = self.marshallVarInt(value, byteOutput, offset)

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
            offset = self.marshallVarInt(value, byteOutput, offset, 8)

        return self.marshallHeader(byteOutput, offset)

    def marshallListInt64(self, name, value, index, byteOutput, offset):
        valueLength = len(value)

        if valueLength != 0:
            assert (valueLength < ColferConstants.COLFER_LIST_MAX)

            byteOutput[offset] = index; offset += 1

            # Compressed Path
            offset = self.marshallVarInt(valueLength, byteOutput, offset)

            for valueElement in value:
                # Move last bit to the end
                valueElementEncoded = ((valueElement << 1) & 0xffffffffffffffff) ^ ((valueElement >> 63) & 0x0000000000000001)
                # Compressed Path
                offset = self.marshallVarInt(valueElementEncoded, byteOutput, offset, 8)
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
                offset = self.marshallVarInt(value, byteOutput, offset)

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
            offset = self.marshallVarInt(valueLength, byteOutput, offset)

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
            offset = self.marshallVarInt(valueLength, byteOutput, offset)

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
            offset = self.marshallVarInt(valueLength, byteOutput, offset)

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
            offset = self.marshallVarInt(valueLength, byteOutput, offset)

            # Flat
            for valueAsBytes in value:
                valueLength = len(valueAsBytes)
                assert (valueLength <= ColferConstants.COLFER_MAX_SIZE)

                # Compressed Path
                offset = self.marshallVarInt(valueLength, byteOutput, offset)

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

            offset = self.marshallVarInt(valueLength, byteOutput, offset)

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
            offset = self.marshallVarInt(valueLength, byteOutput, offset)

            #Flat
            for valueAsString in value:
                valueLength = len(valueAsString)
                assert (valueLength <= ColferConstants.COLFER_MAX_SIZE)

                valueAsBytes, valueLength = self.encodeUTFBytes(valueAsString)
                assert (valueLength <= self.COLFER_MAX_SIZE)

                # Compressed Path
                offset = self.marshallVarInt(valueLength, byteOutput, offset)

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