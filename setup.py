from setuptools import setup, find_packages

setup(
    name='turbonomic_sustanability_export',
    version='0.1.0',
    packages=find_packages(include=['sqllite.*', 'tool.*', 'turbonomic.*']),
    install_requires=[
        'requests',
        'urllib3',
        'retry',
        'pandas',
        'configparser',
        'flask',
        'flask-openapi3',
        'jsonpickle',
    ]
)
