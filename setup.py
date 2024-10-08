from setuptools import find_packages, setup

setup(
    name='bwt',
    version='0.1.0',
    packages=find_packages(where='backend'),
    package_dir={'bwt': 'backend/bwt', 'bwt_front': 'interface'},
    install_requires=[
        'fastapi',
        'matplotlib',
        'moviepy',
        'pandas',
        'openai',
        'openai-whisper',
        'python-multipart',
        'requests',
        'spacy',
        'st-annotated-text',
        'streamlit',
        'tqdm',
        'whisper_timestamped',
        'uvicorn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
