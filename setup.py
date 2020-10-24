from setuptools import setup, find_namespace_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = ["pyinspect", "click", "rich>=9.0.0"]

setup(
    name="donote",
    version="0.0.2",
    description="donote",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require={"dev": ["coverage-badge", "click"]},
    python_requires=">=3.6,",
    packages=find_namespace_packages(),
    include_package_data=True,
    url="https://github.com/FedeClaudi/knowledge_base",
    author="Federico Claudi",
    zip_safe=False,
    entry_points={"console_scripts": ["dono = donote.cli:cli_main"]},
)
