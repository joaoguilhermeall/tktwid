import setuptools

VERSION = '0.1.2'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="tktwid",
    version=VERSION,
    author="Joao Guilherme Dev",
    author_email="joaoguilhermedev@gmail.com",
    license="MIT Licence",
    url="https://github.com/joaoguilhermeall/tktwid",
    description="Edited tkinter widgets to simplify the creation and assembly of a graphical interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['./env', './tests', './dist', './build']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements
)
