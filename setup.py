from setuptools import setup

setup(
    name='pysafe',
    version='0.1.1',
    description='Google Safe Browsing API python wrapper',
    url='https://github.com/Te-k/pysafebrowsing',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='security',
    install_requires=['requests', 'configparser'],
    license='MIT',
    packages=['pysafebrowsing'],
    entry_points= {
        'console_scripts': [ 'safebrowsing=pysafebrowsing.cli:main' ]
    }
)
