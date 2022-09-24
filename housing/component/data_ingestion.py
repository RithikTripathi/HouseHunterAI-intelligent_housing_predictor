from turtle import down
from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.exception import Housing_Exception
from housing.logger import logging
import sys, os
import tarfile # to extract zip file
from six.moves import urllib # to download data


class DataIngestion:
    # :  says that data_ingestion_config should be of DataIngestionConfig Class
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'='*20}Data Ingestion Log Started.{'='*20} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Housing_Exception(e, sys)


    def download_housing_data(self) -> str:
        try:
            # extracting remote url to downnload dataset
            download_url = self.data_ingestion_config.dataset_download_url

            # folder location to download file
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            # in case dir folder exist, remove it and make new, else make new
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            os.makedirs(tgz_download_dir, exist_ok=True)


            housing_file_name = os.path.basename(download_url)

            # complete file path to download
            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)

            # logging
            logging.info(f"Downloading file from :[{download_url}] into :[{tgz_file_path}]")
            # using urllib to download data in designated folder
            urllib.request.urlretrieve(download_url, tgz_file_path)
            # logging
            logging.info(f"File :[{tgz_file_path}] Downloaded Successfully. ")

            # returning file path where we have returned the source file
            return tgz_file_path

        except Exception as e:
            raise Housing_Exception(e,sys) from e

    def extract_tgz_file(self):
        pass

    def split_data_as_train_test(self):
        pass

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            # downloading the file and obtaining file location
            tgz_file_path = self.download_housing_data()
        except Exception as e:
            raise Housing_Exception(e, sys)