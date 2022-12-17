import sys
import uuid, os, sys
import pandas as pd
from tkinter import E
from collections import namedtuple
from datetime import datetime
from housing.config.configuration import Configuration
from housing.logger import logging, get_log_file_name
from housing.exception import Housing_Exception
from threading import Thread
from typing import List
from multiprocessing import Process   

from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from housing.entity.artifact_entity import ModelTrainerArtifact, ModelEvaluationArtifact , ModelPusherArtifact
from housing.entity.config_entity import DataIngestionConfig, ModelEvaluationConfig
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import  DataValidation
from housing.component.data_transformation import DataTransformation
from housing.component.model_trainer import ModelTrainer
from housing.component.model_evaluation import ModelEvaluation
from housing.component.model_pusher import ModelPusher
from housing.constant import EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME


Experiment = namedtuple("Experiment", ["experiment_id", "initialization_timestamp", "artifact_time_stamp",
                                        "running_status", "start_time", "stop_time", "execution_time", "message",
                                        "experiment_file_path", "accuracy", "is_model_accepted"])

# Exp_id : random exp id is generated
# the moment an object of pipeline is generated , we create a initialization pipeline.
# artifact time stamp : timestamp when the artifact was created: sow e can know which experiment generated which specific artifact and its related info.
# experiment file path : a csv file inside experiment directory to store the tabular data on UI
# running status : if running status is true then we will simply ignore any more pipeline running requests

class Pipeline(Thread):

    # as in experiment namedTuple we have 11 params, we are initializing None to everyone of them
    experiment: Experiment = Experiment(*([None] *11 ))
    experiment_file_path = None

    def __init__(self, config: Configuration)  -> None:
        try:
            os.makedirs(config.training_pipeline_config.artifact_dir, exist_ok= True)
            Pipeline.experiment_file_path = os.path.join(
                config.training_pipeline_config.artifact_dir,
                EXPERIMENT_DIR_NAME,
                EXPERIMENT_FILE_NAME
            )
            super().__init__(daemon=False, name="pipeline")

            self.config = config

       

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_data_ingestion(self) -> DataIngestionConfig:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config = self.config.get_data_validiation_config(),
                                            data_ingestion_artifact = data_ingestion_artifact)

            return data_validation.initiate_data_validation()

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact,
                                        data_validation_artifact : DataValidationArtifact) -> DataTransformationArtifact :
        try:
            data_transformation = DataTransformation(
                                        data_transformation_config= self.config.get_data_transformation_config(),
                                        data_ingestion_artifact= data_ingestion_artifact,
                                        data_validation_artifact= data_validation_artifact  )
            
            return data_transformation.initiate_data_transformation()

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_model_trainer(self, data_transformation_artifact : DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(
                                model_trainer_config= self.config.get_model_trainer_config(),
                                data_transformation_artifact= data_transformation_artifact
                                )

            return model_trainer.initiate_model_trainer()

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_model_evaluation(self, data_ingestion_artifact : DataIngestionArtifact, 
                                     data_validation_artifact :DataValidationArtifact,
                                     model_trainer_artifact: ModelTrainerArtifact
                                ) -> ModelEvaluationArtifact:
        try:
            model_eval = ModelEvaluation(
                model_evaluation_config= self.config.get_model_evaluation_config(),
                data_ingestion_artifact= data_ingestion_artifact,
                data_validation_artifact= data_validation_artifact,
                model_trainer_artifact= model_trainer_artifact
            )

            return model_eval.initiate_model_evaluation()

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def start_model_pusher(self, model_eval_artifact: ModelEvaluationArtifact):
        try:
            model_pusher = ModelPusher(
                model_pusher_config= self.config.get_model_pusher_config(),
                model_evaluation_artifact= model_eval_artifact
            )

            return model_pusher.initiate_model_pusher()

        except Exception as e:
            raise Housing_Exception(e,sys) from e


    def run_pipeline(self):
        try:
            if Pipeline.experiment.running_status:
                logging.info("Pipeline is already running !!! ")
                return Pipeline.experiment

            logging.info("*********==================  Pipeline Started. ==================*********")

            experiment_id = str(uuid.uuid4())

            Pipeline.experiment = Experiment(experiment_id= experiment_id,
                                            initialization_timestamp= self.config.time_stamp,
                                            artifact_time_stamp= self.config.time_stamp,
                                            running_status= True,
                                            start_time= datetime.now(),
                                            stop_time= None,
                                            execution_time= None,
                                            experiment_file_path= Pipeline.experiment_file_path,
                                            is_model_accepted= None,
                                            message= "Pipeline Started...",
                                            accuracy= None
            )
            logging.info(f"Pipeline experiment : {Pipeline.experiment}")

            self.save_experiment()

            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            data_transformation_artifact = self.start_data_transformation(
                                                    data_ingestion_artifact= data_ingestion_artifact,
                                                    data_validation_artifact= data_validation_artifact)

            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact= data_transformation_artifact)

            model_evaluation_artifact = self.start_model_evaluation(
                                                    data_ingestion_artifact= data_ingestion_artifact,
                                                    data_validation_artifact= data_validation_artifact,
                                                    model_trainer_artifact= model_trainer_artifact
            )

            if model_evaluation_artifact.is_model_accepted:
                model_pusher_artifact = self.start_model_pusher(model_eval_artifact= model_evaluation_artifact)
                logging.info(f'Model pusher artifact: {model_pusher_artifact}')
            else:
                logging.info("Trained model rejected.")
            
            logging.info("*********==================  Pipeline Completed. ==================*********")

            stop_time = datetime.now()
            Pipeline.experiment = Experiment(experiment_id= Pipeline.experiment.experiment_id,
                                            initialization_timestamp= self.config.time_stamp,
                                            artifact_time_stamp= self.config.time_stamp,
                                            running_status= False,
                                            start_time= Pipeline.experiment.start_time,
                                            stop_time= stop_time,
                                            execution_time= stop_time - Pipeline.experiment.start_time,
                                            message= "Pipeline Completed.",
                                            experiment_file_path= Pipeline.experiment_file_path,
                                            is_model_accepted= model_evaluation_artifact.is_model_accepted,
                                            accuracy= model_trainer_artifact.model_accuracy
            )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")
            self.save_experiment()

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def save_experiment(self):
        try:
            if Pipeline.experiment.experiment_id is not None:
                experiment = Pipeline.experiment
                experiment_dict = experiment._asdict()
                experiment_dict: dict = {key : [value] for key , value in experiment_dict.items()}

                experiment_dict.update({
                    "created_time_stamp" : [datetime.now()],
                    "experiment_file_path" : [os.path.basename[Pipeline.experiment.experiment_file_path]]
                })

                experiment_report = pd.DataFrame(experiment_dict)

                os.makedirs(os.path.dirname(Pipeline.experiment_file_path), exist_ok= True)

                if os.path.exists(Pipeline.experiment_file_path):
                    experiment_report.to_csv(Pipeline.experiment_file_path, index= False, header= False, mode= "a")
                else:
                    experiment_report.to_csv(Pipeline.experiment_file_path, index= False, header= True, mode= "w")
            else:
                print("First Start Experiment")

        except Exception as e:
            raise Housing_Exception(e,sys) from e


    @classmethod
    def get_experiment_status(cls, limit:5) -> pd.DataFrame:
        try:
            pass

        except Exception as e:
            raise Housing_Exception(e,sys) from e




# in experiment history, only last 5 records will be displayed
# use of class level attribute : it is same for every object. 
# if training pipeline is already running : i will not start another pipeline and inform that pipeline already running