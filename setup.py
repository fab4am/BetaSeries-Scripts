from setuptools import setup, find_packages
import glob

setup(
    name='seripy',
    version="1.0",
    description="Series related Scripts",
    author="Jonathan Adami",
    author_email="contact@jadami.com",
    install_requires=[
        "sqlalchemy==0.6.1",
        "simplejson",
        "web.py",
        "python-daemon",
        "lxml",
        "piratebay",
    ],
    packages=find_packages(),
    include_package_data=True,
    data_files=[],
    entry_points = {},
    scripts=[],
)

