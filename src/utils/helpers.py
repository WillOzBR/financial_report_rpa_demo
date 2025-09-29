from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def format_date(date_str: str) -> Optional[str]:
    """
    Converte uma data de string (AAAA-MM-DD ou AAAA.MM.DD) para DD/MM/AAAA.
    Em caso de erro, retorna None.
    """
    for sep in ["-", "."]:
        try:
            dt = datetime.strptime(date_str, f"%Y{sep}%m{sep}%d")
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            continue
    logger.error(f"Formato de data inesperado: {date_str}")
    return None

def treat_float(value) -> float:
    '''
        Trata e converte uma string numérica para float, lidando com vírgulas e pontos.

        Args:
            value (str | float | int): Valor a ser convertido.

        return:
            float: Valor convertido para float.'''
    try:
        if isinstance(value, (str)):
            value = value.strip().replace(',', '.')

        return float(value)
    except (ValueError, TypeError) as e:
        logger.error(f"Erro ao converter valor para float: {value}")
        raise ValueError(f"Não foi possível converter '{value}' para float") from e
