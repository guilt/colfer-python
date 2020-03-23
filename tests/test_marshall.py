import unittest

from tests.test_basic import ExampleMixin


class TestMarshall(unittest.TestCase, ExampleMixin):

    def testMarshall(self):
        byteOutput = bytearray(200)
        marshallableObject = self.getExampleObject()
        marshallableObject.marshall(byteOutput)
        print('Marshalled: {}'.format(byteOutput))

    def testUnMarshall(self):
        byteInput = bytearray(200)
        unmarshalledObject, _ = self.getExampleObject().unmarshall(byteInput)
        print('Unmarshalled: {}'.format(unmarshalledObject))
