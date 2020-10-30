import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acorns",
    version="0.0.4",
    author="Deshana Desai, Etai Shuchatowitz, Zhongshi Jiang, Teseo Schneider,Daniele Panozzo",
    author_email="dkd266@nyu.edu",
    description="An Automatic Generator for Gradients and Hessians ofC99 functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deshanadesai/acorns",
    packages=setuptools.find_packages(include=("acorns", "acorns.*")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_dir={"": "."},
    install_requires = [
            'pycparser',
            'numpy',
            'argparse'],
    entry_points={
        'console_scripts': [
            'acorns_autodiff = acorns.forward_diff:main'
            ]
    }

    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],
)
