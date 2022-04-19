from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='youdied',
    version='0.0.1',
    url='',
    license='MIT',
    author='Thomas F',
    author_email='',
    description='Captures screen and detect "you died"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Scientific/Engineering :: Image Recognition"
    ],
    entry_points={
        'console_scripts': ['youdied=cli:run_from_cli']
    },
    install_requires=[
        'numpy',
        'pandas',
        'tensorflow>=2',
        'pillow>=9',
        'D3DShot @ git+https://github.com/fauskanger/D3DShot#egg=D3DShot'
    ]
)
