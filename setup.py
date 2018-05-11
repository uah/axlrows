from distutils.core import setup
from setuptools import find_packages
setup(
    name='axlrows',
    version='0.0.6',
    install_requires=[
        "Pygments==2.2.0",
        "appdirs==1.4.3",
        "docopt==0.6.2",
        "jedi==0.10.2",
        "packaging==16.8",
        "prompt-toolkit==1.0.14",
        "ptpython==0.39",
        "pyaxl==1.1",
        "pyparsing==2.2.0",
        "six==1.10.0",
        "suds-jurko==0.6",
        "wcwidth==0.1.7"
    ],
    zip_safe=False,
    packages=[
        'axlrows'
    ]
)

