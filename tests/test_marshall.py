import unittest

from colf import Colfer
from tests.test_basic import ExampleMixin


class TestMarshallPrimitives(unittest.TestCase, ExampleMixin):

    def runTestOnType(self, typeName, testVectors):
        marshallableObject = Colfer()
        marshallableObject.declareAttribute('v', typeName)

        for vector in testVectors:
            byteOutput = bytearray(30)
            marshallableObject['v'] = vector
            print('Marshalling: {}'.format(marshallableObject))
            length = marshallableObject.marshall(byteOutput)
            print('Marshalled: {}'.format(byteOutput[:length]))

            byteInput=byteOutput[:length]

            unmarshalledObject, _ = marshallableObject.unmarshall(byteInput)
            print('Unmarshalled: {}'.format(unmarshalledObject))
            self.assertEqual(vector, unmarshalledObject['v'])


    def testInt32(self):
        testVectors = [
            0,
            35,
            129,
            270,
            768
            -2147483648,
            2147483647,
        ]
        self.runTestOnType('int32', testVectors)


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
