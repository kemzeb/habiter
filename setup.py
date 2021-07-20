import os
import setuptools

from habiter.internal.utils.consts import HABITER_VERSION

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="habiter",
    version=HABITER_VERSION,
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
    packages=setuptools.find_packages(),

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
