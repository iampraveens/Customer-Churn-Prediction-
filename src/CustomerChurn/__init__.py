import logging 
import os
import sys
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

log_path = os.path.join(os.getcwd(), 'logs')

os.makedirs(log_path, exist_ok=True)

LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.FileHandler(LOG_FILEPATH),
                        logging.StreamHandler(sys.stdout)
                    ],
                    format="[%(asctime)s] %(lineno)d %(name)s - %(module)s - %(levelname)s - %(message)s")

logger = logging.getLogger("CustomerChurnLogger")