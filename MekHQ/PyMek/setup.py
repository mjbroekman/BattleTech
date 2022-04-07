# setup.py file for pymek package
import setuptools

setuptools.setup(
    name="pymek",
    version="1.0.0",
    description="Tool for interrogating MekHQ campaign saves",
    license="GPL-3.0 - https://opensource.org/licenses/GPL-3.0",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'})
