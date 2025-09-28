from os.path import join
from os import getenv

from dotenv import load_dotenv
import logging
from pathlib import Path

load_dotenv()

# CAMINHO BASE/LOCAL
try:
    LOCAL_DIR = Path(__file__).resolve().parent.parent
except NameError:
    LOCAL_DIR = Path.cwd()

# CAMINHOS LOG
LOG_DIR = join(LOCAL_DIR, 'logs')
LOG_FILE = join(LOG_DIR, 'app.log')

# CAMINHOS OUTPUT
RPA_DOWNLOAD_DIR = join(LOCAL_DIR, 'data')

# CHAVES E ACESSOS
TWELVE_API_KEY = getenv('TWELVE_API_KEY')

# LOGGING CONFIG
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename=LOG_FILE, 
    filemode='a'            
)

logger = logging.getLogger(__name__)