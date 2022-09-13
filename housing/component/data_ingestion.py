from housing.entity.config_entity import DataIngestionConfig
from housing.exception import Housing_Exception
from housing.logger import logging
import sys, os

class DataIngestion:
    # :  says that data_ingestion_config should be of DataIngestionConfig Class
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion Log Started.{'='*20} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Housing_Exception(e, sys)


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise Housing_Exception(e, sys)