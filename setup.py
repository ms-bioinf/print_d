import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ms-bioinf", # Replace with your own username
    version="0.0.1",
    author="Michael Schroeder",
    author_email="ms@biotec.tu-dresden.de",
    description="Code to print matrices for the applied bioinformatics lecture.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
