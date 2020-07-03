import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="squeakserver",
    version="1.0.0",
    url="https://github.com/yzernik/squeakserver",
    description="Server for squeak protocol.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={"test": ["pytest", "coverage"]},
    entry_points={
        'console_scripts': [
            'runsqueakserver = squeakserver.server.main:main',
        ],
    },
)
