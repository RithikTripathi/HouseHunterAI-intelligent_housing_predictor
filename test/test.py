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



# # Data Validiation Checking ----------------

# from housing.logger import logging
# from housing.pipeline.pipeline import Pipeline


# def main():
#     try:
#         pipeline = Pipeline()
#         pipeline.run_pipeline()
#     except Exception as e:
#         logging.error(f"{e}")
#         print(e)
    

# if __name__ == "__main__":
#     main()


# Data Validiation Config Checking ----------------

# from housing.logger import logging
# from housing.pipeline.pipeline import Pipeline
# from housing.config.configuration import Configuration


# def main():
#     try:
#         data_transformation_config = Configuration().get_data_transformation_config()
#         print(data_transformation_config)
#     except Exception as e:
#         logging.error(f"{e}")
#         print(e)
    

# if __name__ == "__main__":
#     main()



from housing.util.util import read_yaml_file
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelEvaluationConfig, ModelTrainerConfig, ModelPusherConfig, TrainingPipelineConfig
from housing.constant import *
from housing.exception import Housing_Exception
from housing.logger import logging
import os, sys
from housing.config.configuration import Configuration 


from housing.logger import logging
from housing.pipeline.pipeline import Pipeline

def main():
    try:
        config_file_path= CONFIG_FILE_PATH
        current_time_stamp = CURRENT_TIME_STAMP

        config_info = read_yaml_file(file_path=config_file_path)
        training_pipeline_config = config_info[TRAINING_PIPELINE_CONFIG_KEY]
        artifact_dir = os.path.join(ROOT_DIR,
                        training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                        training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
                        )

        trianing_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)


        # experiment_file_path = os.path.join(
        #         config.training_pipeline_config.artifact_dir,
        #         EXPERIMENT_DIR_NAME,
        #         EXPERIMENT_FILE_NAME
        #     )

  

        print(Configuration.training_pipeline_config.artifact_dir)

        # print( experiment_file_path)
    except Exception as e:
        logging.error(f"{e}")
        print(e)
    

if __name__ == "__main__":
    main()
