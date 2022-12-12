from housing.logger import logging
from housing.exception import Housing_Exception
from housing.entity.config_entity import ModelEvaluationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact
from housing.constant import *
from housing.util.util import write_yaml_file, read_yaml_file, load_object,load_data
from housing.entity.model_factory import evaluate_regression_model
import numpy as np
import sys, os



class ModelEvaluation:

    def __init__(
            self, 
            model_evaluation_config: ModelEvaluationConfig,
            data_ingestion_artifact: DataIngestionArtifact,
            data_validation_artifact: DataValidationArtifact,
            model_trainer_artifact: ModelTrainerArtifact):

        try:
            logging.info(f"{'>>' * 30}Model Evaluation log started.{'<<' * 30} ")
            self.model_evaluation_config = model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    # # In order to obtain the best model : there could be multiple scenarious like : 
    #     - the pipeline is running for the first Time
    #     - the file is not available
    #     - file is present but there is no best_model info available
    # then we will return None as such there is no best / running model available

    def get_best_model(self):
        try:
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path

            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path = model_evaluation_file_path) # creating a empty file

                return model 

            model_eval_file_content = read_yaml_file(file_path= model_evaluation_file_path)

            # creating a empty dictionary if no file is present otherwise accept that file
            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            # checking if best_model details not present in file -> return None
            if BEST_MODEL_KEY not in model_eval_file_content:
                return model
            
            model = load_object(file_path= model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            
            return model

    
        except Exception as e:
            raise Housing_Exception(e,sys) from e


    # to update the model details in case we get a better model
    def update_eveluation_report(self, model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            eval_file_path = self.model_evaluation_config.model_evaluation_file_path
            model_eval_content = read_yaml_file(file_path= eval_file_path)
            # creating a empty dict if no content is present in file
            model_eval_content = dict() if model_eval_content is None else model_eval_content

            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]
            
            logging.info(f"Previous eval result: {model_eval_content}")


            #evasluated_model_path contains the path of newly trained model which performed better than current model
            eval_result = {
                BEST_MODEL_KEY : {
                    MODEL_PATH_KEY : model_evaluation_artifact.evaluated_model_path
                }
            }

            # creating a history of previou models with timestamp for record
            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp : previous_best_model}

                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY : model_history}
                    eval_result.update(history)

                else:
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)

            logging.info(f"Updated eval result:{model_eval_content}")

            write_yaml_file(file_path = eval_file_path, data = model_eval_content)

            

        except Exception as e:
            raise Housing_Exception(e,sys) from e


    # for comparision 
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            trained_model_object = load_object(file_path= trained_model_file_path)

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            train_dataframe = load_data(file_path= train_file_path, schema_file_path= schema_file_path)
            test_dataframe = load_data(file_path= test_file_path, schema_file_path= schema_file_path)

            schema_content = read_yaml_file(file_path= schema_file_path)

            target_column_name = schema_content[TARGET_COLUMN_KEY]

            # target column
            logging.info(f"Converting target column into numpy array.")
            train_target_arr = np.array(train_dataframe[target_column_name])
            test_target_arr = np.array(test_dataframe[target_column_name])
            logging.info(f"Conversion completed target column into numpy array.")

            # dropping target column from the dataframe
            logging.info(f"Dropping target column from the dataframe.")
            train_dataframe.drop(target_column_name, axis=1, inplace=True)
            test_dataframe.drop(target_column_name, axis=1, inplace=True)
            logging.info(f"Dropping target column from the dataframe completed.")

            model = self.get_best_model()

            # if no model is in production
            if model is None:
                logging.info("Not found any exisitng model. Hence accepting trained model. ")
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted= True, evaluated_model_path= trained_model_file_path)
                self.update_eveluation_report(model_evaluation_artifact)
                logging.info(f"Model Accepted. Model Evaluation artifact {model_evaluation_artifact} created")

                return model_evaluation_artifact

            # if there is already a model in production
            model_list = [model, trained_model_object] # creaitng a list with model : existing prod. model, trained_model_obj: recently trained model

            metric_info_artifact = evaluate_regression_model(
                    model_list= model_list,
                    X_train= train_dataframe,
                    y_train= train_target_arr,
                    X_test= test_dataframe,
                    y_test= test_target_arr,
                    base_accuracy= self.model_trainer_artifact.model_accuracy
            )
            logging.info(f"Model evaluation completed. model metric artifact: {metric_info_artifact}")
            # this will mark the completion of the comparision part : now proceeding towards actions

            # in cases like if we increase our base accuracy in future, then both (in prod. and trained) might fail to achieve it
            # in such situations, the metric_info_artifact will come None
            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(is_model_accepted= False, evaluated_model_path= trained_model_file_path)
                logging.info(response)
                return response

            # we are also capturing the index : so if 0 then model if 1 then trained model
            if metric_info_artifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted= True, evaluated_model_path= trained_model_file_path)
                self.update_eveluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")

            else:
                logging.info("Trained model did NOT performed better than existing model, hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted= False ,evaluated_model_path= trained_model_file_path)
                
            return model_evaluation_artifact

        except Exception as e:
            raise Housing_Exception(e,sys) from e


    def __del__(self):
        logging.info(f"{'=' * 20}Model Evaluation log completed.{'=' * 20} ")

    



