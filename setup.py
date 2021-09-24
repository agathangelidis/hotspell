from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name="hotspell",
    version="0.0.9",
    description="Detect heat waves from weather station data",
    author="Ilias Agathangelidis",
    packages=["hotspell"],
    install_requires=["numpy", "pandas"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    url="https://github.com/agathangelidis/hotspell",
)
