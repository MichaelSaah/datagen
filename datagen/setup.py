import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datagen",
    version="0.0.1",
    author="Michael Saah",
    author_email="mike.saah@gmail.com",
    description="A data generation utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelSaah/datagen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    )
