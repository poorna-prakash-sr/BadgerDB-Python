from setuptools import setup, find_packages

setup(
    name="badgerdb-python",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
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
