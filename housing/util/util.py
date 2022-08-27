# it is a kind of helper function
import yaml
from housing.exception import Housing_Exception
import os, sys

# making a function to read yaml file

def read_yaml_file(file_path : str) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionart.
    file_path : str
    """
    try : 
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Housing_Exception(e,sys) from e