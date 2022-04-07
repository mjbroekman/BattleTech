# setup.py file for pymek package
import setuptools

setuptools.setup(
    name="pymek",
    version="1.0.0",
    description="Tool for interrogating MekHQ campaign saves",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'})
