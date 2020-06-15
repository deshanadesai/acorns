import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autodiff-deshanadesai", # Replace with your own username
    version="0.0.1",
    author="Deshana Desai, Etai Shuchatowitz, Zhongshi Jiang, Teseo Schneider,Daniele Panozzo",
    author_email="dkd266@nyu.edu",
    description="An Automatic Generator for Gradients and Hessians ofC99 functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deshanadesai/acorns",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_dir="src",
)
