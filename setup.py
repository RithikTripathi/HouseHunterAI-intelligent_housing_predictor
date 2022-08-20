from setuptools import setup, find_packages
from typing import List

# Declaring Variables for Setup function
Project_Name = "housinig-predictor"
Version = "0.0.1"
Author = "Rithik Tripathi"
Descriptuon = " Full Stack Data Scientist Machine Learning Housing Project"
Packages = ['housing']
REQUIREMENTS_FILE_NAME = "requirements.txt"

# here we are basically reading the requirements.txt file and returning a list of that
# -> specifies what is going to be returned : i.e will return a list having string values in it.
# -> this part could be ignored but its a good practice to increase readability of our code
def get_reuqirements_list()->List[str]:
    """
    This function is responsible to return list of requirements as strings mentioned in requirements.txt
    Return : list containing name of libraries mentioned in requirements.txt
    """
    with open(REQUIREMENTS_FILE_NAME) as requirement_file:
        return requirement_file.readlines()


# Setting up setup()
setup(
    name = Project_Name,
    version = Version,
    author = Author,
    description = Descriptuon,
    packages = find_packages(),
    install_requires = get_reuqirements_list() # name automatically changes from Requirement_file_name to install_requires
)

