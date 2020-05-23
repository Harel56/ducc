from setuptools import setup, find_packages
setup(name='ducc', vertion='0.1.0', author='Harel Etgar', description='project for course advanced system design', packages=find_packages(), install_requires=['sphinx', 'click', 'flask', 'Pillow', 'matplotlib', 'pika', 'pymongo'], tests_require=['pytest'])
