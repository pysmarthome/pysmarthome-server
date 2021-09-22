from setuptools import setup, find_packages

setup(
    name='pysmarthome-server',
    description='A simple yet powerful python http server to integrate smart devices',
    version='0.3.0',
    author='Filipe Alves',
    author_email='filipe.alvesdefernando@gmail.com',
    install_requires=[
        'ariadne',
        'asyncio',
        'flask',
        'pysmarthome>=3.1.0',
        's3db',
    ],
    packages=find_packages(),
    scripts=['pysmarthome-server.wsgi'],
    url='https://github.com/filipealvesdef/pysmarthome-server',
    zip_safe=False,
)
