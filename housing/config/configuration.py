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
        
        self.config_info = read_yaml_file(file_path=config_file_path)
        self.training_pipeline_config = self.get_training_pipeline_config()
        self.time_stamp = current_time_stamp

    def get_data_ingestion_config(self) -> DataIngestionConfig: 
        pass

    def get_data_validiation_config(self) ->DataValidationConfig:
        pass

    def get_data_transformation_config(self) -> DataTransformationConfig:
        pass

    def get_model_trailer_config(self) -> ModelTrainerConfig:
        pass

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass

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
