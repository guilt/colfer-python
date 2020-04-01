import unittest

from tests.test_basic import ExampleMixin


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
