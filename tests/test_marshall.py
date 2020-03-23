import json
import unittest

from tests.test_basic import ExampleMixin


class TestMarshall(unittest.TestCase, ExampleMixin):

    def testStr(self):
        marshallableObject = self.getExampleObject()
        print(marshallableObject)

    def testJson(self):
        marshallableObject = self.getExampleObject()
        print(json.dumps(marshallableObject, default=str))

    def testMarshall(self):
        byteOutput = bytearray(200)
        marshallableObject = self.getExampleObject()
        marshallableObject.marshall(byteOutput)

    def testUnMarshall(self):
        byteInput = bytearray(200)
        unmarshalledObject, _ = self.getExampleObject().unmarshall(byteInput)
        print(json.dumps(unmarshalledObject, default=str))
