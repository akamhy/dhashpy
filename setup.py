import os.path
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

about = {}
with open(os.path.join(os.path.dirname(__file__), "dhashpy", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name=about["__title__"],
    packages=["dhashpy"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=about["__license__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    download_url="https://github.com/akamhy/dhashpy/archive/%s.tar.gz"
    % about["__version__"],
    keywords=[
        "DHash",
        "image hashing",
        "Perceptual hashing",
        "compare images",
    ],
    install_requires=["Pillow"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    project_urls={
        "Source": "https://github.com/akamhy/dhashpy",
        "Documentation": "https://dhashpy.readthedocs.io/en/latest/",
        "Tracker": "https://github.com/akamhy/dhashpy/issues",
    },
)
