from setuptools import setup

setup(
    name='MongoLibrary',
    version='1.1.0',
    description='Biblioteca para utilização do MongoDB com Robot Framework',
    license='MIT',
    packages=['MongoLibrary'],
    author='Rafael Carneiro de Moraes',
    author_email='rafael.moraes@primecontrol.com.br',
    keywords=['robotframework', 'robot', 'framework', 'mongodb'],
    url='https://gitlab.com/rpa-automation/libraries/mongolibrary',
    include_package_data=True,
    install_requires=[
        'pymongo'
    ]
)