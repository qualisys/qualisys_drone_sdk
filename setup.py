from setuptools import setup

version = "0.1a1"

setup(
    name="qfly",
    version=version,
    description="Qualisys Drone SDK",
    url="https://github.com/qualisys/qfly",
    download_url="https://github.com/qualisys/qfly/tarball/{}".format(
        version
    ),
    author="Mehmet Aydin Baytas",
    author_email="support@qualisys.com",
    install_requires=['qtm', 'cflib', 'pynput'],
    license="MIT",
    packages=["qfly"],
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
    zip_safe=True,
)