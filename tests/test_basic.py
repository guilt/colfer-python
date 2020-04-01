
import datetime
import json
import unittest

from colf import Colfer, EntropyUtils, RawFloatConvertUtils


class ExampleMixin(object):

    def getExampleObject(self):
        x = Colfer()
        x.declareAttribute('a', 'uint32')
        x.a = 2
        x.a = 3

        x.b = False
        x.b = True

        x.declareAttribute('c', 'int16')
        x.c = -10

        x.declareAttribute('d', 'int64')
        x.d = 1000000000000

        x.e = (2, 3, 4)

        x.f = b'123'
        x.f = bytearray('123', encoding='utf8')

        x.g = u'123'

        x.h = datetime.datetime.now()

        x.i = [2, 3, 4]

        x.declareAttribute('j', 'float64')
        x.j = 3.14151617

        x.declareAttribute('k', 'float32')
        x.k = 3.1415

        x.l = 'Hello World'

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
        testObject['a'] = 4
        self.assertEqual(testObject.a, 4)

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
        self.assertEqual(0b1111111111111110000000000000000000000000000000000000000000000000, bin(self.getComplementaryMaskUnsigned(49)))

class TestRawFloatConvertUtils(unittest.TestCase, RawFloatConvertUtils):
    # Test Reference:
    # https://www.h-schmidt.net/FloatConverter/IEEE754.html
    # https://en.wikipedia.org/wiki/Double-precision_floating-point_format
    def testKnownValues(self):
        self.assertEqual(self.getFloatAsBytes(0),             bytes([0b00000000, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getFloatAsBytes(0.5),           bytes([0b00111111, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getFloatAsBytes(-0.5),          bytes([0b10111111, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getFloatAsBytes(9.8),           bytes([0b01000001, 0b00011100, 0b11001100, 0b11001101]))

        self.assertEqual(self.getDoubleAsBytes(0),            bytes([0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getDoubleAsBytes(-2),           bytes([0b11000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]))
        self.assertEqual(self.getDoubleAsBytes(0.01171875),   bytes([0b00111111, 0b10001000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000]))
