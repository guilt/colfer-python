# Python-Colfer

A strong typed version of *Colfer* serialization/deserialization for Python.

## Usage

First install with PyPi

```bash
pip install colf
```

Then use it to construct a Colfer Object and use it:

```python
from colf import Colfer

class TestType(Colfer):

    def __init__(self):
        super(Colfer, self).__init__()
        self.declareAttribute('radius', 'float64')
        self.declareAttribute('test', 'bool')
        self.declareAttribute('inner', 'object')

    def marshall(self, byteOutput, offset=0):
        offset = self.marshallFloat64(self.radius, 0, byteOutput, offset)
        offset = self.marshallBool(self.test, 1, byteOutput, offset)
        offset = self.marshallObject(self.inner, 2, byteOutput, offset)
        return offset

    def unmarshall(self, byteInput, offset=0):
        self.radius, offset = self.unmarshallFloat64(0, byteInput, offset)
        self.test, offset = self.unmarshallBool(1, byteInput, offset)
        self.inner, offset = self.unmarshallObject(2, byteInput, offset)
        return self, offset

# Write to Somewhere
exampleObject = TestType()
exampleObject.radius = 2.5
exampleObject.test = True
exampleObject.inner = TestType()
exampleObject.inner.radius = 3.0
byteOutput = bytearray(30)
length = exampleObject.marshall(byteOutput)
print(byteOutput[:length])

# Read from Somewhere
deserializedObject, _ = TestType().unmarshall(byteOutput[:length])
print(deserializedObject, deserializedObject.inner)
```

## Running Unit Tests

```bash
pip install tox
tox
```

## Call for Testing Volunteers

The code was tested on Python 2.7, 3.6, 3.7, 3.8.
 
This code has been tested on Little-Endian machines only. It
requires to be tested on other architectures such as PowerPC, or those
with unique floating point formats.

Also, there may be chances this code may not work on some Python
version due to nuances not previously uncovered.

Please volunteer to test it on as many exotic computers, OSes
and send in your patches (or) bug reports.
