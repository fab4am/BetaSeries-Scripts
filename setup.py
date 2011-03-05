from setuptools import setup, find_packages
import glob

setup(
    name='bs',
    version="1.0",
    description="Series related Scripts",
    author="Jonathan Adami",
    author_email="contact@jadami.com",
    install_requires=[
        "sqlalchemy==0.6.1",
        "simplejson",
        "Flask",
        "python-daemon",
        "lxml",
        "beautifulsoup",
    ],
    packages=find_packages(),
    include_package_data=True,
    data_files=[],
    entry_points = {},
    scripts=[],
)

