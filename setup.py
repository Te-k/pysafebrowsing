from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("pysafebrowsing/about.py") as f:
    v = f.read()
    for l in v.split("\n"):
        if l.startswith("__version__"):
            __version__ = l.split('"')[-2]

setup(
    name="pysafebrowsing",
    version=__version__,
    description="Google Safe Browsing API python wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Te-k/pysafebrowsing",
    author="Tek",
    author_email="tek@randhome.io",
    keywords="security",
    install_requires=["requests", "configparser"],
    license="MIT",
    packages=["pysafebrowsing"],
    entry_points={"console_scripts": ["safebrowsing=pysafebrowsing.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
