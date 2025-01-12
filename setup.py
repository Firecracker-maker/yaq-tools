import setuptools

# Package meta-data.
NAME = "yaqtools"
DESCRIPTION = "A comprehensive suits of data tools"
URL = "https://github.com/Firecracker-maker/yaq-tools"
AUTHOR = "firecraker"


def _get_requirements(filename: str) -> list:
    """
    Parse package requirements form a pip requirementts.txt file
    Parameters
    ----------
    filename: filename to parse the information from

    Returns
    -------

    """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("./version.txt", "r") as ver:
    version = ver.read().strip()


# What packages are optional?
EXTRAS = {
    "format": ["black==23.10.1", "isort==5.12.0"],
    "lint": ["pylint==2.16.2"],
    "test": [
        "pytest==7.4.3",
        "pytest-mock==3.12.0",
        "coverage==7.3.2",
        "requests-mock==1.10.0",
    ],
    "release": ["nox==2022.11.21", "build==1.2.1", "twine==5.0.0"],
}

EXTRAS["all"] = list(set([v for deps in EXTRAS.values() for v in deps]))
version_attribute = f"__version__ = '{version}'"

# Where the magic happens:
setuptools.setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    url=URL,
    version=version,
    base_package_name="yaqtools",
    packages=setuptools.find_packages(exclude=["*tests"]),
    install_requires=_get_requirements("requirements.txt"),
    extras_require=EXTRAS,
    python_requires=">=3.11",
    include_package_data=True,
)
