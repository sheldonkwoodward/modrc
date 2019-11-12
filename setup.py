# sheldon woodward
# 4/15/18

"""Setup file."""


from os.path import abspath, dirname, join
from setuptools import setup

from modrc import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(name='modrc',
      version=__version__,
      description='A bare-bones command line program.',
      long_description=long_description,
      packages=['modrc', 'modrc/commands'],
      install_requires=['click', 'clint', 'distro'],
      entry_points={
          'console_scripts': [
              'modrc = modrc.__main__:main'
          ]
      },
      license='MIT',
      keywords='cli')
