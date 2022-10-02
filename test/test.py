# from housing.constant import *
# from housing.config.configuration import Configuration

# config = Configuration()

# print(config.config_info)
# print(DATA_INGESTION_CONFIG_KEY)
# print(config.config_info[DATA_INGESTION_CONFIG_KEY])

# data_ingestion_info = config.config_info[DATA_INGESTION_CONFIG_KEY]

# config.config_info[DATA_INGESTION_TGZ_DOWNLOAD_URL_KEY]

# config.config_info

# config.config_info[DATA_INGESTION_CONFIG_KEY][DATA_INGESTION_TGZ_DOWNLOAD_URL_KEY]

# config.get_training_pipeline_config().artifact_dir
# CURRENT_TIME_STAMP

# data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]

# config.get_data_ingestion_config()

# checking data ingestion --------------
# from housing.pipeline.pipeline import Pipeline
# from housing.exception import Housing_Exception
# from housing.logger import logging


# def main():
#     try:
#         pipeline = Pipeline()
#         pipeline.run_pipeline()
#     except Exception as e:
#         logging.error(f"{e}")
#         print(e)
    

# if __name__ == "__main__":
#     main()
# Data Ingestion Done ----------------

# checking if we are getting data validation config------------
# from housing.config.configuration import Configuration
# from housing.exception import Housing_Exception
# from housing.logger import logging

# def main():
#     try:
#         data_validation_config = Configuration().get_data_validiation_config()
#         print(data_validation_config)
#     except Exception as e:
#         logging.error(f"{e}")
#         print(e)
    

# if __name__ == "__main__":
#     main()

# Data validaiton configuration being received successfully ------------



