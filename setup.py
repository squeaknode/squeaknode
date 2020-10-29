import io

import setuptools.command.build_py
# from grpc_tools.command import BuildPackageProtos
from setuptools import find_packages, setup
from setuptools import Command

PACKAGE_DIRECTORIES = {
    '': '.',
}

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        self.run_command('build_proto_modules')
        setuptools.command.build_py.build_py.run(self)


class BuildPackageProtos(Command):
    """Command to generate project *_pb2.py modules from proto files."""

    description = 'build grpc protobuf modules'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import grpc_tools.command
        grpc_tools.command.build_package_protos('.')

setup(
    name="squeaknode",
    version="1.0.0",
    url="https://github.com/yzernik/squeaknode",
    description="Server for squeak protocol.",
    long_description=readme,
    packages=find_packages(),
    #package_dir=PACKAGE_DIRECTORIES,
    include_package_data=True,
    zip_safe=False,
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
