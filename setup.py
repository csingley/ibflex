"""
Release process:
    1.  Update ibflex.__version__.__version__
    2.  Change download_url below
    3.  Commit changes & push
    4.  `git tag` the release
    5.  `git push --tags`
    6.  Verify that new tag shows at https://github.com/csingley/ibflex/releases
    7.  `python setup.py sdist`
    8.  `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
    9.  Check https://test.pypi.org/project/ibflex
    10. `twine upload dist/*`
    11. `make clean`
    12. Change download_url back to master; commit & push
"""
import os.path
from setuptools import setup, find_packages

__here__ = os.path.dirname(os.path.realpath(__file__))

ABOUT = {}
with open(os.path.join(__here__, "ibflex", "__version__.py"), "r") as f:
    exec(f.read(), ABOUT)

with open(os.path.join(__here__, "README.rst"), "r") as f:
    README = f.read()

URL_BASE = "{}/tarball".format(ABOUT["__url__"])

setup(
    name=ABOUT["__title__"],
    version=ABOUT["__version__"],
    description=ABOUT["__description__"],
    long_description=README,
    long_description_content_type="text/x-rst",
    author=ABOUT["__author__"],
    author_email=ABOUT["__author_email__"],
    url=ABOUT["__url__"],
    packages=find_packages(),
    package_data={
        "ibflex": ["README.rst", "tests/*", "py.typed"],
    },
    python_requires=">=3.7",
    license=ABOUT["__license__"],
    # Note: change 'master' to the tag name when releasing a new verion
    #  download_url="{}/master".format(URL_BASE),
    download_url="{}/{}".format(URL_BASE, ABOUT["__version__"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["Interactive Brokers", "ibkr", "flex", "xml"],
    extras_require={
        "web": ["requests"],
    },
    entry_points={
        "console_scripts": [
            "flexget=ibflex.client:main [web]",
        ],
    },
)
