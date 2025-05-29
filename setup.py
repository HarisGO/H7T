from setuptools import setup, find_packages

setup(
    name="h7t",
    version="1.0.0",
    description="Modular Terminal Hacker Toolkit by H-7 (HarisGO)",
    author="H-7",
    author_email="your-email@example.com",
    url="https://github.com/yourusername/h7t",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "pillow",
        "requests",
        "beautifulsoup4"
    ],
    entry_points={
        "console_scripts": [
            "h7t=h7t.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)