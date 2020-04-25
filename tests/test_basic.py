# -*- coding: utf-8 -*-
import datetime
import unittest

from colf import Colfer
from colf_base import EntropyUtils, RawFloatConvertUtils, UTFUtils


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

        x.g = bytearray(b'123')  # Python 2 Coalesces b'123' to str
        x.g = bytearray('123', encoding='utf8')

        x.h = u'Foo'

        x.i = datetime.datetime.now()

        x.declareAttribute('j', 'float32')
        x.j = 3.1415

        x.declareAttribute('k', 'float64')
        x.k = 3.141516171819

        x.l = 'Hello World'
        x.l = u'これはテストです'

        x.declareAttribute('m', 'list', variableSubType='str')
        x.m = ('Hello', 'World')

        x.declareAttribute('n', 'list', variableSubType='bool')
        x.n = (True, False)

        x.declareAttribute('o', 'list', variableSubType='bytes')
        x.o = (bytearray(b'Foo'), bytearray(b'Bar'))

        return x


class TestBasicTypes(unittest.TestCase, ExampleMixin):

    def testTypes(self):
        self.getExampleObject()

    def testDir(self):
        print(dir(self.getExampleObject()))

    def testIteration(self):
        for attr, attrValue in self.getExampleObject().items():
            print(attr, ' = ', attrValue)

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
        print('JSON: {}'.format(marshallableObject.toJson()))

    def testLoadJson(self):
        marshallableObject = self.getExampleObject()
        jsonToLoad = '{"j":2.71828}'
        marshallableObject.fromJson(jsonToLoad)
        self.assertAlmostEqual(marshallableObject.j, 2.71828, places=6)


class TestEntropyUtils(unittest.TestCase, EntropyUtils):

    def testSign(self):
        self.assertEqual(self.getSign(-1), 1)
        self.assertEqual(self.getSign(0), 0)
        self.assertEqual(self.getSign(1), 0)

    def testPowers(self):
        self.assertEqual(self.getPowerOfTwo(0), 1)
        self.assertEqual(self.getPowerOfTwo(), 2)
        self.assertEqual(self.getPowerOfTwo(2), 4)
        self.assertEqual(self.getPowerOfTwo(200), 2 ** 200)
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
        self.assertEqual(0b1111111111111110000000000000000000000000000000000000000000000000,
                         self.getComplementaryMaskUnsigned(49))


class TestRawFloatConvertUtils(unittest.TestCase, RawFloatConvertUtils):
    # Test Reference:
    # https://www.h-schmidt.net/FloatConverter/IEEE754.html
    # https://en.wikipedia.org/wiki/Double-precision_floating-point_format

    def assertBytesEqual(self, lhs, rhs):
        self.assertEqual(len(rhs), len(rhs), 'Lengths of Bytes are not equal')
        for offset in range(len(lhs)):
            self.assertTrue(int(lhs[offset]) == int(rhs[offset]),
                            'Bytes at position: {} are not the same'.format(offset))

    def testKnownValuesAsBytes(self):
        self.assertBytesEqual(self.getFloatAsBytes(0), [0b00000000, 0b00000000, 0b00000000, 0b00000000])
        self.assertBytesEqual(self.getFloatAsBytes(0.5), [0b00111111, 0b00000000, 0b00000000, 0b00000000])
        self.assertBytesEqual(self.getFloatAsBytes(-0.5), [0b10111111, 0b00000000, 0b00000000, 0b00000000])
        self.assertBytesEqual(self.getFloatAsBytes(9.8), [0b01000001, 0b00011100, 0b11001100, 0b11001101])

        self.assertBytesEqual(self.getDoubleAsBytes(0),
                              [0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
                               0b00000000])
        self.assertBytesEqual(self.getDoubleAsBytes(-2),
                              [0b11000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
                               0b00000000])
        self.assertBytesEqual(self.getDoubleAsBytes(0.01171875),
                              [0b00111111, 0b10001000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
                               0b00000000])

    def testKnownValuesAsFloats(self):
        self.assertEqual(0, self.getBytesAsFloat(bytearray([0b00000000, 0b00000000, 0b00000000, 0b00000000])))
        self.assertEqual(0.5, self.getBytesAsFloat(bytearray([0b00111111, 0b00000000, 0b00000000, 0b00000000])))
        self.assertEqual(-0.5, self.getBytesAsFloat(bytearray([0b10111111, 0b00000000, 0b00000000, 0b00000000])))
        self.assertAlmostEqual(9.8, self.getBytesAsFloat(bytearray([0b01000001, 0b00011100, 0b11001100, 0b11001101])),
                               places=6)

        self.assertEqual(0, self.getBytesAsDouble(bytearray(
            [0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000])))
        self.assertEqual(-2, self.getBytesAsDouble(bytearray(
            [0b11000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000])))
        self.assertEqual(0.01171875, self.getBytesAsDouble(bytearray(
            [0b00111111, 0b10001000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000])))


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
