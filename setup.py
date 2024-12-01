"""Set up the package."""
from pathlib import Path

from setuptools import find_packages, setup

with open(Path(__file__).absolute().parents[0] / "eve" / "VERSION") as _f:
    __version__ = _f.read().strip()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="eve",
    version=__version__,
    packages=find_packages(),
    description="Building applications with LLMs through composability",
    install_requires=["pydantic", "sqlalchemy", "numpy"],
    long_description=long_description,
    license="MIT",
    include_package_data=True,
    long_description_content_type="text/markdown",
)
