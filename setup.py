"""
colf: A strong typed version of Colfer serialization/deserialization for Python.
"""
from setuptools import setup, find_packages

VERSION = '0.5.1'

def get_requirements():
    with open('requirements.txt') as requirements:
        for req in requirements:
            req = req.strip()
            if req and not req.startswith('#'):
                yield req

def get_readme():
    with open('README.md') as readme:
        return readme.read()

setup(name='colf',
      version=VERSION,
      description="colf: Colfer serialization/deserialization for Python",
      long_description=get_readme(),
      long_description_content_type='text/markdown',
      classifiers=
      [
          'Topic :: Software Development :: Libraries',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      keywords='colf colfer serialization deserialization',
      author='Karthik Kumar Viswanathan',
      author_email='karthikkumar@gmail.com',
      url='http://github.com/guilt/Colfer-Python',
      license='cc0-1.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=['six'],
     )
