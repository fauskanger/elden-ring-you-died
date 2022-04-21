from setuptools import setup, find_packages, find_namespace_packages
from pathlib import Path
from collections import defaultdict


def gen_model_file_tuples():
    model_files = list(Path('models').rglob('*'))
    model_files = [p for p in model_files if p.is_file()]
    # print(f'Files {model_files}')
    # print(f'  >>>>  There are {len(model_files)} files.')

    entries = defaultdict(list)
    for f in model_files:
        entries[f.relative_to(Path()).parent].append(str(f))

    return [(str(k), v) for (k, v) in entries.items()]


model_data_files_entries = gen_model_file_tuples()

# print('> > > > file entries:\n')
# print(model_data_files_entries, end='\n\n')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='youdied',
    version='0.2.2',
    url='https://github.com/fauskanger/elden-ring-you-died/tree/main/youdied',
    license='MIT',
    author='Thomas F',
    author_email='',
    description='Captures screen and detect "you died"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    data_files=model_data_files_entries,  # Optional
    # package_data={
    #     'youdied': ['*'],
    # },
    # include_package_data=True,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Scientific/Engineering :: Image Recognition"
    ],
    entry_points={
        'console_scripts': ['youdied=youdied:main']
    },
    install_requires=[
        'numpy',
        'pandas',
        'tensorflow>=2',
        'pillow>=9',
        'comtypes>=1.1.7',  # dependency of D3DShot
    ]
)
