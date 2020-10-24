from setuptools import setup, find_namespace_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = [
    "pyinspect",
    "click",
]

setup(
    name="knowledgebase",
    version="0.0.1tc",  
    description="Knowledge base",
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
    entry_points={
        "console_scripts": [
            "kb = base.cli:cli_main",
        ]
    },
)