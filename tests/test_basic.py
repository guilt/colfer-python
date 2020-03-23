
import datetime
import json
import unittest

from colf import Colfer


class ExampleMixin(object):

    def getExampleObject(self):
        x = Colfer()
        x.declareAttribute('a', 'int32')
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

        x.k = 'Hello World'

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
