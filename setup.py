from setuptools import setup, find_packages

setup(
    name="aredis_client",
    version="0.3.0",
    description="Async redis Client is a simple and easy-to-use asynchronous Redis client for Python 3.6+",
    author="Alireza Heidari",
    author_email="alirezaheidari.cs@gmail.com",
    url="https://github.com/alirezaheidari-cs/aredis-client",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "redis",
        "python-decouple",
        "pydantic>=2",
    ],
    license='Apache License 2.0',
    keywords="redis async-redis aredis async-client",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    python_requires='>=3.6',
    project_urls={
        "Documentation": "https://github.com/alirezaheidari-cs/aredis-client#readme",
        "Source": "https://github.com/alirezaheidari-cs/aredis-client",
        "Tracker": "https://github.com/alirezaheidari-cs/aredis-client/issues",
    },
)
