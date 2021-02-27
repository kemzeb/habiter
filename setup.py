import os
import setuptools

from habiter.upkeep.updater import HABITER_VERSION

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
    keywords= (
        "productivity",
        "cli"
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    package_data = {
        "habiter.data": ["trace.txt"],
    },

    install_requires=(
        'appdirs'
    ),

    entry_points= {
        "console_scripts": [
            "habiter=habiter.run:main"
        ]
    },
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    python_requries =">=3.8"
)
