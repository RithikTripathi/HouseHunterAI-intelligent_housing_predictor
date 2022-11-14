from cgi import test
from housing.logger import logging
from housing.exception import Housing_Exception
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import os,sys
import pandas as pd
import json
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab




class DataValidation:
    def __init__(self, data_validation_config : DataValidationConfig,
                        data_ingestion_artifact : DataIngestionArtifact):
        try:
            logging.info(f"{'='*20} Data Validation Log Started. {'='*20} \n\n")
            self.data_validiation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def get_train_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def is_train_test_file_exists(self) -> bool:
        try:
            logging.info("========= Checking if Training and Test Files are Available =========")
            is_train_file_exists = False
            is_test_file_exists = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            logging.info(f"Checking if train file exists: {train_file_path}.")
            if os.path.exists(train_file_path):
                is_train_file_exists = True
                logging.info(f"Train file exists: {train_file_path}.")
            else:
                logging.info(f"Train file does not exists: {train_file_path}.")
                raise Exception("Train file does not exists")

            logging.info(f"Checking if test file exists: {test_file_path}.")
            if os.path.exists(test_file_path):
                is_test_file_exists = True
                logging.info(f"Test file exists: {test_file_path}.")
            else:
                logging.info(f"Test file does not exists: {test_file_path}.")
                raise Exception("Test file does not exists")

            is_available =  is_train_file_exists and is_test_file_exists
            
            logging.info(f" === is Train and Test File Exists? ->  === {is_available}")

            return is_available

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def validiate_dataset_schema(self) -> bool :
        # we can make a function to check if the dataset meets the requirements as stated by client or have specific fields/ values or not 
        pass
    
    def get_and_save_data_drift_report(self):
        try:
            train_df, test_df = self.get_train_test_df()
            
            profile = Profile(sections=[DataDriftProfileSection()] )
            profile.calculate(train_df, test_df)
            # profile.json() # this returns a json object
            report = json.loads(profile.json()) # this converts that json into dictionary format/ list

            report_file_path = self.data_validiation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            with open(report_file_path, "w") as report_file:
                json.dump(report, report_file, indent=6)

            return report

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_train_test_df()
            dashboard.calculate(train_df, test_df)

            report_page_file_path = self.data_validiation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir, exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise Housing_Exception(e,sys) from e



    def  is_data_drift_detected(self) -> bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            # report now saved in the artifact folder. This function could be further imporved to compare datasets for model efficiency.
            return True
        except Exception as e:
            raise Housing_Exception(e,sys) from e


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            self.is_data_drift_detected()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path= self.data_validiation_config.schema_file_path,
                report_file_path= self.data_validiation_config.report_file_path,
                report_page_file_path=self.data_validiation_config.report_page_file_path,
                is_validated=True,
                message= "Data Validation Performed Successfully."
            )
            logging.info(f"Data Validation Artifact : {data_validation_artifact}")

            return data_validation_artifact
        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def __del__(self):
        logging.info(f"{'='*20} Data Validation Log Completed. {'='*20} \n\n")