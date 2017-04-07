try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup, find_packages

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name              = 'TCS34725',
      version           = '1.0.0',
      author            = 'Urs Utzinger',
      author_email      = 'utzinger@email.arizona.edu',
      description       = 'Library for accessing the TCS34725 color sensor',
      license           = 'MIT',
      classifiers       = classifiers,
      url               = 'https://github.com/uutzinger/Python_TCS34725/',
      dependency_links  = ['https://github.com/adafruit/Adafruit_Python_GPIO/tarball/master#egg=Adafruit-GPIO-0.6.5'],
      install_requires  = ['Adafruit-GPIO>=0.6.5'],
      packages          = find_packages())
