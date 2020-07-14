import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pentagraph-Cobalt", # Replace with your own username
    version="0.0.1",
    author="Cobalt",
    author_email="chaosthe0rie@pm.me",
    description="Graph representation and tools for programming with pentagame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Penta-Game/pentagraph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)