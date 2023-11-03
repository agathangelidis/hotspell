from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name="hotspell",
    version="0.1.5.5",
    description="Detect heat waves from weather station data",
    author="Ilias Agathangelidis",
    packages=["hotspell"],
    package_data={"hotspell": ["datasets/*.pickle"]},
    install_requires=["numpy", "pandas"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    url="https://github.com/agathangelidis/hotspell",
)
