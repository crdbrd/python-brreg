import re

from setuptools import find_packages, setup


with open('brreg/__init__.py') as fh:
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))


with open('README.rst') as fh:
    long_description = fh.read()


setup(
    name='brreg',
    version=metadata['version'],
    description='API client for Brønnøysundregistrene',
    long_description=long_description,
    url='https://brreg.readthedocs.io/',
    author='Otovo AS',
    author_email='andrroy+brreg@otovo.com',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='brreg enhetsregisteret',
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3.6',
    install_requires=['attrs >= 17.4', 'requests'],
    extras_require={
        'dev': [
            'black',
            'check-manifest',
            'flake8',
            'flake8-bugbear',
            'flake8-comprehensions',
            'flake8-import-order',
            'flake8-quotes',
            'flake8-tidy-imports',
            'pep8-naming',
            'mypy',
            'pydocstyle',
            'pytest',
            'pytest-xdist',
            'responses',
            'sphinx',
            'sphinx_rtd_theme',
            'tox',
        ]
    },
)
