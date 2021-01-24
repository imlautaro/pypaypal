"""
PyPayPal
------
An easy way to use the PayPal API with Python
"""

from setuptools import setup

setup(
    name='PyPayPal',
    version='1.0',
    url='https://github.com/imlautaro/pypaypal',
    license='MIT',
    author='Lautaro Pereyra',
    author_email='dev.lautaropereyra@gmail.com',
    description='An easy way to use the PayPal API with Python',
    py_modules=['pypaypal'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    python_requires=">= 3.6",
    install_requires=['requests']
)
