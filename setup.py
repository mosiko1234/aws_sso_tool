from setuptools import setup, find_packages

setup(
    name='aws_sso_tool',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto3',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'aws-sso-tool=aws_sso_tool.cli:main',
        ],
    },
    author="Moshe Eliya",
    description="CLI tool to simplify AWS SSO login and operations",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mosiko1234/aws_sso_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
