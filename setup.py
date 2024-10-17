from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='aws_sso_tool',
    version='0.1.12',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto3>=1.18.0',
        'click>=7.0',
    ],
    entry_points={
        'console_scripts': [
            'aws-sso-tool=aws_sso_tool.cli:main',
        ],
    },
    author="Moshe Eliya",
    author_email="mosiko1234@gmail.com",
    description="CLI tool to simplify AWS SSO login and operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mosiko1234/aws_sso_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)
