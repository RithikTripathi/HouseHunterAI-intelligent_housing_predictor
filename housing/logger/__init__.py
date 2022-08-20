import logging
import os
from datetime import datetime


# Directory to save logging reports
Log_Dir = "Housing_Logs"
# Variable to store current time with date 
Current_time_stamp = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
# Logging File Name with Date and Time
Log_File_Name = f"log_{Current_time_stamp}.log"

# Creating the directory
# exist_ok makes sure that new filder will only be created if it does not exist
os.makedirs(Log_Dir, exist_ok=True)

Log_File_Path = os.path.join(Log_Dir, Log_File_Name)
logging.basicConfig(
    filename=Log_File_Path,
    filemode="w",
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    level= logging.INFO
    )
