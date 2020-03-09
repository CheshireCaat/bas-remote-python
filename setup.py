from setuptools import setup, find_packages

import bas_remote

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='bas-remote-python',
    description='Python library, which allows you to automate Google Chrome browser.',
    url='https://github.com/CheshireCaat/bas-remote-python',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author_email='cheshirecat902@gmail.com',
    project_urls={
        "Documentation": "https://github.com/CheshireCaat/bas-remote-python/wiki",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    version=bas_remote.__version__,
    license=bas_remote.__license__,
    author=bas_remote.__author__,
    packages=find_packages(),
    keywords=[
        'visual-programming-language',
        'browserautomationstudio',
        'bas-remote-control',
        'bas-remote-client',
        'bot-framework',
        'bas-remote',
        'bas-client',
        'automation',
        'chromium',
        'imacros',
        'windows',
        'desktop',
        'browser',
        'grabber',
        'poster',
        'macros',
        'bas',
        'ide',
        'cef',
        'bot'
    ],
    install_requires=requirements,
    python_requires=">=3.7",
    test_suite='tests',
)
