import os
import io

from setuptools import setup, find_packages, Command
from os import path

root = 'celseq2'
name = 'celseq2'

exec(open("celseq2/version.py").read())

here = path.abspath(path.dirname(__file__))
description = ('A Python Package for Processing '
               'CEL-Seq2 RNA-Seq Data.')

install_requires = [
    'snakemake==4.0.0',
    'pyyaml>=3.12, <4',
    'HTSeq>=0.8',
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

    version=__version__,

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
    package_data={
        'celseq2': [
            'template/*',  # config.yaml, etc
            'workflow/*'  # snakemake workflow
        ]
    },
    # data outside the package
    # data_files=[('my_data', ['data/data_file'])],

    entry_points={
        'console_scripts': [

            ('bc_demultiplex = '
             'celseq2.demultiplex:main'),
            ('cook-annotation = '
             'celseq2.prepare_annotation_model:main'),
            ('count-umi = '
             'celseq2.count_umi:main'),
            ('new-configuration-file = '
             'celseq2.cook_config:main_new_config_file'),
            ('export-workflow = '
             'celseq2.cook_config:main_export_snakemake_workflow'),
            ('celseq2 = '
             'celseq2.celseq2:main'),
        ],
    },

    cmdclass={
        'clean': CleanCommand,
    },

)
