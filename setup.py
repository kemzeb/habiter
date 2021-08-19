import setuptools


def get_version(rel_path: str) -> str:
    with open(rel_path, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                version = line.split(delim)[1]
                return version
        raise RuntimeError('Unable to find version string')


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="habiter",
    version=get_version('habiter/__init__.py'),
    description="Quantifies and keeps tabs on unwanted habits.",
    author="Kemal Zebari",
    url="https://github.com/kemzeb/habiter",
    license="MIT",
    keywords=(
        "productivity",
        "cli"
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['habiter'],

    install_requires=(
        'appdirs',
        'click',
    ),

    entry_points={
        "console_scripts": [
            "habiter=habiter.internal.run:main"
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.8"
)
