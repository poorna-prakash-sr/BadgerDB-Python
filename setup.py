from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    description = f.read()   

setup(
    name="badgerdb-python",
    author="Poorna Prakash SR",
    author_email="poornaprakashsr@gmail.com",
    description = "Python wrapper for BadgerDB",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    long_description=description,
    long_description_content_type='text/markdown',
    package_data={
        "badger": ["libbadger.so"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
