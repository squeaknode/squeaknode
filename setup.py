import os
import sys

import pkg_resources
import setuptools.command.build_py
import setuptools.command.test
from grpc_tools import protoc
from setuptools import Command
from setuptools import find_packages
from setuptools import setup

from squeaknode import __version__

PACKAGE_DIRECTORIES = {
    '': '.',
}


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        self.run_command('build_proto_modules')
        setuptools.command.build_py.build_py.run(self)


def build_package_protos(package_root, strict_mode=False):
    proto_files = []
    inclusion_root = os.path.abspath(package_root)
    for root, _, files in os.walk(inclusion_root):
        for filename in files:
            if filename.endswith('.proto'):
                proto_files.append(os.path.abspath(os.path.join(root,
                                                                filename)))

    well_known_protos_include = pkg_resources.resource_filename(
        'grpc_tools', '_proto')

    for proto_file in proto_files:
        command = [
            'grpc_tools.protoc',
            '--proto_path={}'.format(inclusion_root),
            '--proto_path={}'.format(well_known_protos_include),
            '--python_out={}'.format(inclusion_root),
            '--grpc_python_out={}'.format(inclusion_root),
            '--mypy_out={}'.format(inclusion_root),
        ] + [proto_file]
        if protoc.main(command) != 0:
            if strict_mode:
                raise Exception('error: {} failed'.format(command))
            else:
                sys.stderr.write('warning: {} failed'.format(command))


class BuildPackageProtos(Command):
    """Command to generate project *_pb2.py modules from proto files."""

    description = 'build grpc protobuf modules'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # import grpc_tools.command
        # grpc_tools.command.build_package_protos('.')
        build_package_protos('.')


setup(
    name="squeaknode",
    version=__version__,
    url="https://github.com/yzernik/squeaknode",
    description="Server for squeak protocol.",
    packages=find_packages(),
    # package_dir=PACKAGE_DIRECTORIES,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'squeaklib==0.5.1',
        'importlib_resources',
        'argparse',
        'googleapis-common-protos',
        'grpcio',
        'grpcio-tools',
        'mypy-protobuf',
        'psycopg2',
        'requests',
        'SQLAlchemy',
        'Flask',
        'protobuf',
        'flask-login',
        'Flask-WTF',
        'flask-cors',
        'alembic',
    ],
    extras_require={"test": ["pytest", "coverage"]},
    entry_points={
        'console_scripts': [
            'runsqueaknode = squeaknode.main:main',
        ],
    },
    cmdclass={
        'build_proto_modules': BuildPackageProtos,
        'build_py': BuildPyCommand,
    },
)
