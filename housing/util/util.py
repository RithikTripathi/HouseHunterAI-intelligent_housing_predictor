# it is a kind of helper function
import yaml
from housing.exception import Housing_Exception
import os, sys, dill
import numpy as np
import pandas as pd
from housing.constant import *

def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise Housing_Exception(e,sys) from e



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

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path : str location of file to save
    array : np.array data to save
    """
    try : 
       dir_path = os.path.dirname(file_path)
       os.makedirs(dir_path, exist_ok= True)

       with open(file_path, 'wb') as file_obj:
        np.save(file_obj, array)

    except Exception as e:
        raise Housing_Exception(e,sys) from e

def load_numpy_array_data(file_path : str) -> np.array:
    """
    load numpy array data from file
    file_path : str location of file to load
    return : np.array data loaded
    """
    try : 
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise Housing_Exception(e,sys) from e

def save_object(file_path:str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise Housing_Exception(e,sys) from e


def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise Housing_Exception(e,sys) from e


# schema file has datatype of each column, so this function will read daat type from there and try to match/ convert as required
#A static method does not receive an implicit first argument. A static method is also a method that is bound to the class and not the 
# object of the class. This method can’t access or modify the class state. 
# It is present in a class because it makes sense for the method to be present in class.
# @staticmethod : this function would have been a static method if placed in the data transformation class itself
def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame :
    try:

        """
        schema file has datatype of each column, so this function will read daat type from there and try to match/ convert as required
        and then return the dataframe from csv
        """
        
        #reading schema file
        dataset_schema = read_yaml_file(schema_file_path)
        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataframe = pd.read_csv(file_path)

        error_message = ""

        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_message = f"{error_message} \nColumn : [{column}] is not available in the schema"

        if len(error_message) > 0:
            raise Exception(error_message)

        return dataframe

    except Exception as e:
        raise Housing_Exception(e,sys) from e