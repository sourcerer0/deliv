import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deliv",
    version="1.1.0-b.2",
    author="Lo Han",
    author_email="lohan.uchsa@protonmail.com",
    description="Delivery service scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sourcerer0/deliv",
    packages=setuptools.find_packages(),
    keywords="delivery scraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pycountry>=20.7.3',
        'beautifulsoup4>=4.9.3',
        'Delorean>=1.0.0',
        'geopy>=2.1.0',
        'pytz>=2021.1',
        'requests>=2.25.1',
        'urllib3>=1.26.3'
    ]
)