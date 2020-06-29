import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graphene-django-pagination",
    version="0.0.1",
    author="Instruct Developers",
    author_email="contato@instruct.com.br",
    description="This package adds offset-based pagination to Graphene-Django without using Graphene Relay.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/instruct-br/graphene-django-pagination",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'django>=2.2.6',
        "graphene-django>=2.6.0"
    ]
)
