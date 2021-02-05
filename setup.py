import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="packetStatus-sourcerer0",
    version="0.1",
    author="Lo Han",
    author_email="lohan.uchsa@protonmail.com",
    description="Delivery service scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sourcerer0/packetStatus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)