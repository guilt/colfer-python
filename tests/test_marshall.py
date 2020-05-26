# -*- coding: utf-8 -*-
import datetime
import unittest

from colf import Colfer
from tests.test_basic import ExampleMixin


class TestMarshallPrimitives(unittest.TestCase, ExampleMixin):

    def runTestOnType(self, variableType, testVectors, variableSubType=None):
        marshallableObject = Colfer()
        marshallableObject.declareAttribute('v', variableType, variableSubType=variableSubType)

        for vector in testVectors:
            byteOutput = bytearray(80)
            marshallableObject['v'] = vector
            print('Marshalling: {}'.format(marshallableObject))
            length = marshallableObject.marshall(byteOutput)
            print('Marshalled: {}'.format(byteOutput[:length]))

            byteInput=byteOutput[:length]

            unmarshalledObject, _ = marshallableObject.unmarshall(byteInput)
            print('Unmarshalled: {}'.format(unmarshalledObject))
            self.assertEqual(vector, unmarshalledObject['v'])
            print('')

    def testBool(self):
        testVectors = [
            False,
            True
        ]
        self.runTestOnType('bool', testVectors)

    def testUint8(self):
        testVectors = [
            0,
            35,
            255
        ]
        self.runTestOnType('uint8', testVectors)

    def testUint16(self):
        testVectors = [
            0,
            35,
            255,
            258,
            65535
        ]
        self.runTestOnType('uint16', testVectors)

    def testInt32(self):
        testVectors = [
            0,
            35,
            129,
            270,
            768,
            -2147483648,
            2147483647,
        ]
        self.runTestOnType('int32', testVectors)

    def testUint32(self):
        testVectors = [
            0,
            35,
            129,
            270,
            768,
            15000,
            267891,
            2678912,
            4294967295,
        ]
        self.runTestOnType('uint32', testVectors)

    def testListInt32(self):
        testVectors = [
            [],
            [1],
            [129],
            [270],
            [768],
            [-2147483648],
            [2147483647],
            [1,129,270,768],
            [0,-2147483648,2147483647]
        ]
        self.runTestOnType('list', testVectors, 'int32')

    def testInt64(self):
        testVectors = [
            0,
            35,
            129,
            270,
            768,
            -2147483648,
            2147483647,
            -922337203685478,
            922337203685477,
            9223372036854775807,
            -9223372036854775808,
        ]
        self.runTestOnType('int64', testVectors)

    def testListInt64(self):
        testVectors = [
            [],
            [1],
            [129],
            [270],
            [768],
            [-2147483648],
            [2147483647],
            [1,129,270,768,-2147483648,2147483647,-922337203685478,922337203685477],
            [0,-9223372036854775808,9223372036854775807]
        ]
        self.runTestOnType('list', testVectors, 'int64')

    def testUint64(self):
        testVectors = [
            0,
            35,
            129,
            270,
            768,
            4294967295,
            922337203685477,
            9223372036854775,
            92233720368547758,
            9223372036854775807,
            18446744073709551615,
        ]
        self.runTestOnType('uint64', testVectors)

    def testFloat32(self):
        testVectors = [
            0.0,
            0.5,
            -0.5,
            9.800000190734863,
            -2.0,
            0.01171875,
        ]
        self.runTestOnType('float32', testVectors)

    def testListFloat32(self):
        testVectors = [
            [],
            [0.0],
            [0.5],
            [-0.5],
            [0.0, 0.5, -0.5, 9.800000190734863, -2.0, 0.01171875]
        ]
        self.runTestOnType('list', testVectors,'float32')

    def testFloat64(self):
        testVectors = [
            0.0,
            0.5,
            -0.5,
            9.800000190734863,
            -2.0,
            0.01171875,
        ]
        self.runTestOnType('float64', testVectors)

    def testListFloat64(self):
        testVectors = [
            [],
            [0.0],
            [0.5],
            [-0.5],
            [0.0, 0.5, -0.5, 9.800000190734863, -2.0, 0.01171875]
        ]
        self.runTestOnType('list', testVectors,'float64')

    def testTimestamp(self):
        testVectors = [
            datetime.datetime.utcfromtimestamp(0),
            datetime.datetime.utcfromtimestamp(150000),
            datetime.datetime.now(),
            datetime.datetime.utcfromtimestamp(10000000000)
        ]
        self.runTestOnType('datetime', testVectors)

    def testBinary(self):
        testVectors = [
            b'',
            b'abc',
            b'zoozoo',
        ]
        self.runTestOnType('bytes', testVectors)

    def testListBinary(self):
        testVectors = [
            [],
            [b''],
            [b'', b'0'],
            [b'xyz', b'zoozoo'],
        ]
        self.runTestOnType('list', testVectors, 'bytes')

    def testString(self):
        testVectors = [
            '',
            '0',
            '0000',
            u"한",
            u"😘🤩"
        ]
        self.runTestOnType('str', testVectors)

    def testListString(self):
        testVectors = [
            [],
            [''],
            ['0',u"한"],
            ['0000','100'],
            [u"한",u"😘🤩"]
        ]
        self.runTestOnType('list', testVectors, 'str')


class TestMarshall(unittest.TestCase, ExampleMixin):

    def testMarshallAndUnMarshall(self):
        byteOutput = bytearray(200)
        marshallableObject = self.getExampleObject()
        print('Original: {}'.format(marshallableObject))
        length = marshallableObject.marshall(byteOutput)
        print('Marshalled: {}'.format(byteOutput[:length]))
        unmarshalledObject, _ = self.getExampleObject().unmarshall(byteOutput[:length])
        print('Unmarshalled: {}'.format(unmarshalledObject))
