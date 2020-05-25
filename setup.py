from setuptools import setup, find_packages
setup(name='ducc', vertion='1.0.0', author='Harel Etgar', description='Final project for course advanced system design', packages=find_packages(), install_requires=['sphinx', 'click', 'flask', 'Pillow', 'matplotlib', 'pika', 'pymongo', 'protobuf'], tests_require=['pytest'])
