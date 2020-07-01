#!/usr/bin/env python3

from setuptools import setup

setup(
    name='ms210x-tools',
    version="0.0.1",
    description="Tools for MacroSilicon MS210x USB video capture devices",

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'hexdump',
        'ioctl_opt',
    ],
    license='MIT',
    packages=['devices', 'linux'],
    py_modules=['ms210x-tool'],
    python_requires='>=3',
)
