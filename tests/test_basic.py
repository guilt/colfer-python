import unittest

from colf import Colfer


class ExampleMixin(object):

    def getExampleObject(self):
        x = Colfer()
        x.a = 2
        x.a = 3

        x.b = False
        x.b = True

        x.declareAttribute('c', 'short')
        x.c = -10

        x.declareAttribute('d', 'int64')
        x.d = 1000000000000

        x.e = (2, 3, 4)

        x.f = b'123'
        x.f = bytearray('123', encoding='utf8')

        x.g = u'123'

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
