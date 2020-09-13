import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Zen Publish",  # Replace with your own username
    version="0.0.1",
    author="Dr. P. B. Patel",
    author_email="contact.zenreportz@gmail.com",
    description="Package for Zen Reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: APACHE2 License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click', 'pyyaml', 'click', 'requests'
    ],
    python_requires='>=3',
    entry_points='''
        [console_scripts]
        zen=main:zen
    ''',
)
