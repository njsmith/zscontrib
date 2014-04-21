from setuptools import setup, find_packages

DESC = "Extra ZSS-related stuff that doesn't belong in the zss repository"

LONG_DESC = (DESC + "\n"
             "Currently includes some hacks for downloading and converting\n"
             "the Google Books v2 ngrams to ZSS format. It would be nice to\n"
             "include similar scripts here as well.")

setup(
    name="zss",
    version="0.0.0-dev",
    description=DESC,
    long_description=LONG_DESC,
    long_description=LONG_DESC,
    author="Nathaniel J. Smith",
    author_email="njs@pobox.com",
    url="https://github.com/njsmith/zsscontrib",
    classifiers =
      [ "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        ],
    packages=find_packages(),
    install_requires=["zss"],
)
