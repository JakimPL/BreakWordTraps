from setuptools import find_packages, setup

setup(
    name='bwt',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'moviepy',
        'openai',
        'whisper',
        'whisper_timestamped',
        'fastapi',
        'uvicorn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
