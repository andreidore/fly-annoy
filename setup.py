import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='flyannoy',
    version='0.1.0',
    author="Andrei Dore",
    author_email="andrei.dore@gmail.com",
    description="A simple Annoy server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andreidore/flyannoy",
    packages=["flyannoy"],
    install_requires=[
        'flask>=1.1.2',
        'annoy>=1.16.3',
        "boto3>=1.12.39",
        "awscli>=1.18.39",

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
)
