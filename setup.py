from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="susan-calvin-protocol",
    version="0.1.0",
    author="Nicola Marinello",
    author_email="nicola@ni-ma.it",
    description="Detect Creative Constraint Optimization (CCO) in AI-generated text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/susan-calvin-protocol",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "calvin=calvin.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
)
