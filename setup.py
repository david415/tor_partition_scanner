from setuptools import setup, find_packages

__version__ = '0.0.1'
__author__ = 'David Stainton'
__contact__ = 'dstainton415@gmail.com'
__url__ = ''
__license__ = 'GPL3'
__copyright__ = '2017'

setup(name='orscanner', # TODO: pick a better name
      version=__version__,
      description='Tor Bandwidth Scanner',
      long_description=__doc__,
      keywords=['python', 'twisted', 'txtorcon', 'tor', 'metrics'],
      install_requires=open('requirements.txt').readlines(),

      # TODO: complete the classifiers
      #classifiers = ['Framework :: Twisted', 'Programming Language :: Python']
      classifiers=[],
      author=__author__,
      author_email=__contact__,
      url=__url__,
      license=__license__,
      packages=find_packages(),
      # data_files = [('path', ['filename'])]
      data_files=[],
      scripts=['bin/detect_partitions.py'],
     )
