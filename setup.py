from setuptools import find_packages, setup

with open('README.rst', 'r') as f:
    long_description = f.read()

with open('VERSION', 'r') as f:
    version = f.read()

setup(
    name='pysports-stats',
    version=version,
    author='Brandon Veber',
    author_email='veber.brandon@gmail.com',
    description='A free sports API written for python',
    long_description=long_description,
    license='MIT',
    url='https://github.com/bveber/pysports-stats',
    packages=find_packages(),
    python_requires='>=3.7',
    keywords='stats sports api sports machine learning',
    install_requires=[
        "numpy >= 1.19.5",
        "pandas >= 0.24.1",
        "pyquery >= 1.4.0",
        "requests >= 2.18.4"
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
