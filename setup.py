import os
import io

from setuptools import setup, find_packages, Command
from os import path

root = 'celseq2'
name = 'celseq2'
version = '0.0.1'

here = path.abspath(path.dirname(__file__))
description = ('A Python Package for Processing '
               'CEL-Seq2 RNA-Seq Data.')

install_requires = [
    #'genometools>=0.2.7, <1',
    #'pysam>=0.11.1',
    #'jinja2>=2.9.5, <3',
    #'pyyaml>=3.12, <4'
]

# do not require installation if built by ReadTheDocs
# (we mock these modules in docs/source/conf.py)
if 'READTHEDOCS' not in os.environ or \
        os.environ['READTHEDOCS'] != 'True':
    install_requires.extend([
        #'six>=1.10.0, <2',
        #'scipy>=0.14, <1',
        #'plotly>=1.9.6, <3',
    ])
else:
    install_requires.extend([
        #'pandas>=0.13, <1',
    ])

# get long description from file
long_description = ''
with io.open(path.join(here, 'README.md'), encoding='UTF-8') as fh:
    long_description = fh.read()


class CleanCommand(Command):
    """Removes files generated by setuptools.

    """
    # see https://github.com/trigger/trigger/blob/develop/setup.py
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        error_msg = 'You must run this command in the package root!'
        if not os.getcwd() == here:
            raise OSError(error_msg)
        else:
            os.system('rm -rf ./dist ./build ./*.egg-info ')

setup(
    name=name,

    version=version,

    description=description,
    long_description=long_description,

    # homepage
    url='https://gitlab.com/Puriney/celseq2',

    author='Yun Yan',
    author_email='yy1533@nyu.edu',

    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        'License :: Other/Proprietary License',

        'Programming Language :: Python :: 3.5',
    ],

    keywords='single-cell gene expression pipeline processing',

    # packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    packages=find_packages(exclude=['docs', 'tests*']),
    # packages=find_packages(root),

    # libraries = [],

    install_requires=install_requires,

    # tests_require=[],

    extras_require={
        'docs': [
            'sphinx',
            'sphinx-rtd-theme',
            'sphinx-argparse',
            'mock',
        ],
        'tests': [
            'pytest>=3, <4',
            'pytest-cov>=2.2.1, <3',
        ],
    },

    # data
    # package_data={'genometools': ['data/RdBu_r_colormap.tsv']},
    package_data={
        # 'singlecell': [
        #     'data/templates/*/*',
        # ]
    },
    # data outside the package
    # data_files=[('my_data', ['data/data_file'])],

    entry_points={
        'console_scripts': [

            ('bc_demultiplex = '
             'celseq2.demultiplex:main'),
        ],
    },

    cmdclass={
        'clean': CleanCommand,
    },

)
