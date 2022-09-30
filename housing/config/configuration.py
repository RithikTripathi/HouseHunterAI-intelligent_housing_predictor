from housing.util.util import read_yaml_file
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelEvaluationConfig, ModelTrainerConfig, ModelPusherConfig, TrainingPipelineConfig
from housing.constant import *
from housing.exception import Housing_Exception
from housing.logger import logging
import os, sys


# this class has nothing to do with any creation/ deletion
# this only gives configuration information
class Configuration : 

    # these return is already specified as NamedTuple

    def __init__(self, 
                config_file_path:str = CONFIG_FILE_PATH,
                current_time_stamp:str = CURRENT_TIME_STAMP
                ) -> None:
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_data_ingestion_config(self) -> DataIngestionConfig: 
        try:
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]
            artifact_dir = self.training_pipeline_config.artifact_dir

           
            # the folder should be inside artifact folder in housing, it should be names according to the timeline in which it was created
            data_ingestion_artifact_dir = os.path.join(
                artifact_dir, DATA_INGESTION_ARTIFACT_DIR, self.time_stamp
            )
            tgz_download_dir = os.path.join(
                data_ingestion_artifact_dir, data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )
            raw_data_dir = os.path.join(
                data_ingestion_artifact_dir, data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )
            # train and test files will be inside ingested data folder in artifact folder
            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir, data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )
            ingested_train_dir = os.path.join(
                ingested_data_dir, data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            ingested_test_dir =  os.path.join(
                ingested_data_dir, data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )

            data_ingestion_config = DataIngestionConfig(
                                    dataset_download_url = dataset_download_url, 
                                    tgz_download_dir = tgz_download_dir, 
                                    raw_data_dir = raw_data_dir, 
                                    ingested_train_dir = ingested_train_dir, 
                                    ingested_test_dir = ingested_test_dir
                                    )

            logging.info(f"Data Ingestion Config : {data_ingestion_config}")
            return data_ingestion_config


        except Exception as e:
            raise Housing_Exception(e, sys) from e

    def get_data_validiation_config(self) ->DataValidationConfig:
        pass

    def get_data_transformation_config(self) -> DataTransformationConfig:
        pass

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass

    
    # sample output : TrainingPipelineConfig(artifact_dir='c:\\Users\\rkt7k\\Desktop\\iNeuron Data Science\\Projects iNeuron\\MLPROJ\\housing\\artifact')
    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            # reading configuration information
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
                            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
                            )

            trianing_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipeline config : {trianing_pipeline_config}")
            return trianing_pipeline_config

        except Exception as e:
            raise Housing_Exception(e,sys) from e
