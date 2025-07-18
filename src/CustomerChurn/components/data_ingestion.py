import os
import urllib.request as request
import zipfile
from CustomerChurn import logger
from CustomerChurn.utils.common import get_size
from CustomerChurn.config.configuration import DataIngestionConfig
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        """
        Initializes the DataIngestion class with configuration settings.

        Args:
            config (DataIngestionConfig): Configuration object containing
            data ingestion settings such as source URL, local file path,
            and unzip directory.
        """
        
        self.config = config
        
        
    def download_file(self):
        # os.makedirs(os.path.dirname(self.config.local_data_file), exist_ok=True)
        
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url= self.config.source_URL,
                filename= self.config.local_data_file,
            )
            logger.info(f"{filename} downloaded with the following info: \n{headers}")
        else:
            logger.info(f"file already exists of size: {get_size(Path(self.config.local_data_file))}")
            
    
    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)