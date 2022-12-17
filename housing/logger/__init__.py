import logging
import os
from datetime import datetime
import pandas as pd
from housing.constant import get_current_time_stamp
LOG_DIR = "logs"

def get_log_file_name():
    return f"log_{get_current_time_stamp()}.log"

LOG_FILE_NAME = get_log_file_name()

os.makedirs(LOG_DIR, exist_ok= True)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename= LOG_FILE_PATH,
    filemode= "w",
    format = '[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s',
    level= logging.INFO
    )

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns
    
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]


# # Directory to save logging reports
# Log_Dir = "Housing_Logs"
# # Variable to store current time with date 
# Current_time_stamp = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
# # Logging File Name with Date and Time
# Log_File_Name = f"log_{Current_time_stamp}.log"

# # Creating the directory
# # exist_ok makes sure that new filder will only be created if it does not exist
# os.makedirs(Log_Dir, exist_ok=True)

# Log_File_Path = os.path.join(Log_Dir, Log_File_Name)
# logging.basicConfig(
#     filename=Log_File_Path,
#     filemode="w",
#     format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
#     level= logging.INFO
#     )
