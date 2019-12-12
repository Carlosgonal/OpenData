import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

deps_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

setuptools.setup(
    name="opendata",
    version="0.0.1",
    author="Carlos González Álvarez",
    author_email="carlos.gonla@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Carlosgonal/SpainOpenData",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)