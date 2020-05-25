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

class TestMarshall(unittest.TestCase, ExampleMixin):

    def testMarshall(self):
        byteOutput = bytearray(200)
        marshallableObject = self.getExampleObject()
        length = marshallableObject.marshall(byteOutput)
        print('Marshalled: {}'.format(byteOutput[:length]))

    def testUnMarshall(self):
        byteInput = bytearray(200)
        unmarshalledObject, _ = self.getExampleObject().unmarshall(byteInput)
        print('Unmarshalled: {}'.format(unmarshalledObject))
