# -*- coding: utf-8 -*-
import datetime
import json
import unittest

from colf import Colfer, EntropyUtils, RawFloatConvertUtils, UTFUtils


class ExampleMixin(object):

    def getExampleObject(self):
        x = Colfer()

        x.a = False
        x.a = True

        x.declareAttribute('b', 'uint8')
        x.b = 2
        x.b = 3

        x.declareAttribute('c', 'uint16')
        x.c = 230
        x.c = 20000

        x.declareAttribute('d', 'uint32')
        x.d = 10
        x.declareAttribute('dS', 'int32')
        x.dS = -2

        x.declareAttribute('e', 'uint64')
        x.e = 1000000000000
        x.declareAttribute('eS', 'int64')
        x.eS = -1000000000000

        x.declareAttribute('f', 'list', variableSubType='uint64')
        x.f = (2, 3, 4)
        x.f = [2, 3, 4]

        x.g = b'123'
        x.g = bytearray('123', encoding='utf8')

        x.h = u'Foo'

        x.i = datetime.datetime.now()

        x.declareAttribute('j', 'float32')
        x.j = 3.1415

        x.declareAttribute('k', 'float64')
        x.j = 3.141516171819

        x.l = 'Hello World'
        x.l = u'これはテストです'

        return x


class TestBasicTypes(unittest.TestCase, ExampleMixin):

    def testTypes(self):
        self.getExampleObject()

    def testDir(self):
        print(dir(self.getExampleObject()))

    def testIteration(self):
        for attr, attrValue in self.getExampleObject().items():
            print('{} = {}'.format(attr, attrValue))

    def testDictionaryLikeObject(self):
        testObject = self.getExampleObject()
        testObject['a'] = False
        self.assertEqual(testObject.a, False)

        with self.assertRaises(NotImplementedError) as _:
            del testObject['a']

    def testStr(self):
        marshallableObject = self.getExampleObject()
        print(marshallableObject)

    def testJson(self):
        marshallableObject = self.getExampleObject()
        print(json.dumps(marshallableObject, default=str))


class TestEntropyUtils(unittest.TestCase, EntropyUtils):

    def testPowers(self):
        self.assertEqual(self.getPowerOfTwo(0), 1)
        self.assertEqual(self.getPowerOfTwo(), 2)
        self.assertEqual(self.getPowerOfTwo(2), 4)
        self.assertEqual(self.getPowerOfTwo(200), 2**200)
        with self.assertRaises(ArithmeticError):
            self.getPowerOfTwo(2.5)
        with self.assertRaises(ArithmeticError):
            self.getPowerOfTwo(-1)

    def testMaximum(self):
        self.assertEqual(self.getMaximumUnsigned(0), 0)
        self.assertEqual(self.getMaximumUnsigned(), 1)
        self.assertEqual(self.getMaximumUnsigned(2), 3)
        self.assertEqual(self.getMaximumUnsigned(8), 255)
        self.assertEqual(self.getMaximumUnsigned(16), 65535)
        with self.assertRaises(ArithmeticError):
            self.getMaximumUnsigned(2.5)
        with self.assertRaises(ArithmeticError):
            self.getMaximumUnsigned(-1)

    def testEntropy(self):
        self.assertEqual(self.getComplementaryMaskUnsigned(8, 16), 0xff00)
        self.assertEqual(0b11111111111000000000000000000000, self.getComplementaryMaskUnsigned(21, 32))
        self.assertEqual(0b1111111111111110000000000000000000000000000000000000000000000000, self.getComplementaryMaskUnsigned(49))


class TestRawFloatConvertUtils(unittest.TestCase, RawFloatConvertUtils):
    # Test Reference:
    # https://www.h-schmidt.net/FloatConverter/IEEE754.html
    # https://en.wikipedia.org/wiki/Double-precision_floating-point_format

    def testKnownValuesAsBytes(self):
        self.assertEqual(self.getFloatAsBytes(0),             bytes([0b00000000, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getFloatAsBytes(0.5),           bytes([0b00111111, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getFloatAsBytes(-0.5),          bytes([0b10111111, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getFloatAsBytes(9.8),           bytes([0b01000001, 0b00011100, 0b11001100, 0b11001101]))

        self.assertEqual(self.getDoubleAsBytes(0),            bytes([0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getDoubleAsBytes(-2),           bytes([0b11000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getDoubleAsBytes(0.01171875),   bytes([0b00111111, 0b10001000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]))

    def testKnownValuesAsFloats(self):
        self.assertEqual(0,              self.getBytesAsFloat(bytes([0b00000000, 0b00000000, 0b00000000, 0b00000000])))
        self.assertEqual(0.5,            self.getBytesAsFloat(bytes([0b00111111, 0b00000000, 0b00000000, 0b00000000])))
        self.assertEqual(-0.5,           self.getBytesAsFloat(bytes([0b10111111, 0b00000000, 0b00000000, 0b00000000])))
        self.assertAlmostEqual(9.8,      self.getBytesAsFloat(bytes([0b01000001, 0b00011100, 0b11001100, 0b11001101])), places=6)

        self.assertEqual(0,             self.getBytesAsDouble(bytes([0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000])))
        self.assertEqual(-2,            self.getBytesAsDouble(bytes([0b11000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000])))
        self.assertEqual(0.01171875,    self.getBytesAsDouble(bytes([0b00111111, 0b10001000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000])))


class TestUTFUtils(UTFUtils, unittest.TestCase):

    def testUTFEncode(self):
        testVectors = [
            u"A",
            u"¢",
            u"ह",
            u"€",
            u"한",
            u"𐍈",
            u"☃"
        ]
        for testVector in testVectors:
            valueAsBytes, valueLength = self.encodeUTFBytes(testVector)
            decodedTestVector = valueAsBytes[:valueLength].decode('utf-8')
            self.assertEqual(decodedTestVector, testVector)