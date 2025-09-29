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
CSV_REPORT_PATH = join(RPA_DOWNLOAD_DIR, 'currency_report.csv')

# CHAVES E ACESSOS
TWELVE_API_KEY = getenv('TWELVE_API_KEY')

# API URL
API_URL = 'https://api.twelvedata.com/'
ENDPOINT = 'time_series'

# SCRAPING URL
PORTAL_URL = 'https://www.investing.com/currencies/usd-brl-historical-data'

# LOGGING CONFIG
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename=LOG_FILE, 
    filemode='a'            
)

logger = logging.getLogger(__name__)


# INJECTION SCRIPTS
js_error_supression = """
            // Desabilita TODOS os logs do console
            console.log = function() {};
            console.error = function() {};
            console.warn = function() {};
            console.debug = function() {};
            console.info = function() {};
            console.trace = function() {};
            
            // Captura e ignora todos os erros JavaScript
            window.onerror = function() { return true; };
            window.addEventListener('error', function(e) { e.stopImmediatePropagation(); }, true);
            window.addEventListener('unhandledrejection', function(e) { e.stopImmediatePropagation(); }, true);
            
            // Remove todos os event listeners problemáticos
            document.querySelectorAll('*').forEach(function(el) {
                el.onerror = null;
            });
        """