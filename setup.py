import setuptools

VERSION = '0.0.1'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="widgets-theme-tkinter-joaoguilhermedev", # Replace with your own username
    version=VERSION,
    author="Joao Guilherme Dev",
    author_email="joaoguilhermedev@gmail.com",
    description="Edited tkinter widgets to simplify the creation and assembly of a graphical interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=requirements
)


if __name__ == "__main__":
    pass