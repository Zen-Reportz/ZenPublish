import setuptools

def read_text(file_name: str):
    return open(file_name).read()

setuptools.setup(
    name="zen-publish",  # Replace with your own username
    version="0.0.10",
    author="Dr. P. B. Patel",
    author_email="contact.zenreportz@gmail.com",
    description="Package for Zen Reports",
    long_description= read_text("README.md"),
    long_description_content_type="text/markdown",
    url="",
    py_modules = ["zen_publish"],
    # packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click', 'pyyaml', 'requests'
    ],
    python_requires='>=3',
    dependency_links=['https://github.com/Zen-Reportz/ZenPublish/tree/master/python-package'],
    license='Apache License',
    entry_points={
        "console_scripts": [
            "zen=zen_publish:cli"
        ]
    },
)
