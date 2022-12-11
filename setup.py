from setuptools import setup

setup(
    name="qfly",
    description="Qualisys Drone SDK",
    version=0.2,
    url="https://github.com/qualisys/qualisys_drone_sdk",
    license="MIT",
    install_requires=['qtm', 'cflib', 'pynput'],
    packages=["qfly"],
    author="Mehmet Aydin Baytas c/o Qualisys AB",
    author_email="support@qualisys.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
)