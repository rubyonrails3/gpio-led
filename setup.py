from setuptools import setup

setup(
    name="lights",
    version="0.0.1",
    packages=["control"],
    install_requires=[
        "autobahn",
        "suntime",
        "gpiod"
    ],
    console_scripts=[
        'start = control:start'
    ]
)
