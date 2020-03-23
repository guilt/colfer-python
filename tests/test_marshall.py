import json
import unittest

from tests.test_basic import ExampleMixin


class TestMarshall(unittest.TestCase, ExampleMixin):

    def testJson(self):
        marshallableObject = self.getExampleObject()
        print(marshallableObject)
        print(json.dumps(marshallableObject, default=str))

    def testMarshall(self):
        byteOutput = bytearray(200)
        marshallableObject = self.getExampleObject()
        marshallableObject.marshall(byteOutput)

    def testUnMarshall(self):
        byteInput = bytearray(200)
        unmarshalledObject, _ = self.getExampleObject().unMarshall(byteInput)
