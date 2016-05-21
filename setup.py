from setuptools import setup, Command
import sys
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name='python-vex',
    version='1.0.0',
    packages=['vex', 'vex.providers'],
    url='https://github.com/adalekin/vex',
    license='LICENSE',
    author='adalekin',
    author_email='adalekin@gmail.com',
    description='Python library to retreive video content and metadata',
    long_description=open('README.md').read(),
    install_requires=[
        "requests",
        "pafy",
        "youtube-dl",
        "html2text",
        "lxml",
        "python-dateutil",
        "Pillow",
        "pytz"
    ],
    cmdclass={'test': PyTest},
)
