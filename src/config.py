from os.path import join

import dotenv
import logging
from pathlib import Path

# CAMINHO BASE/LOCAL
try:
    LOCAL_DIR = Path(__file__).resolve().parent.parent
except NameError:
    LOCAL_DIR = Path.cwd()


# CAMINHOS LOG
LOG_DIR = join(LOCAL_DIR, 'logs')
LOG_FILE = join(LOG_DIR, 'app.log')


# CAMINHOS OUTPUT
RPA_DOWNLOAD_DIR   = join(LOCAL_DIR, 'data')


# LOGGING CONFIG
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename=LOG_FILE, 
    filemode='a'            
)

logger = logging.getLogger(__name__)