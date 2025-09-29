import pandas as pd
import os
from typing import List

from src.models.financial_data import FinancialData
from src.config import logger

def write_data_to_csv(data: List[FinancialData], file_path: str, overwrite: bool = True):
    """
    Converte uma lista de objetos FinancialData em um DataFrame e o salva
    em um arquivo CSV.

    Args:
        data (List[FinancialData]): Lista de dados financeiros normalizados.
        file_path (str): Caminho completo onde o arquivo CSV será salvo.
        overwrite (bool): Se True, sobrescreve o arquivo existente.
    """
    if not data:
        logger.warning(f"Nenhum dado fornecido para escrita em CSV: {file_path}")
        return

    logger.info(f"Iniciando escrita de {len(data)} registros para {file_path}")

    try:
        # Converte a lista de dataclasses (registros) para um DataFrame - Pandas
        df = pd.DataFrame(data)

        # Configura o modo de escrita
        mode = 'w' if overwrite else 'a'
        header = overwrite or not os.path.exists(file_path)

        # Garante que o diretório existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Salva o DataFrame em CSV
        df.to_csv(
            file_path,
            mode=mode,
            header=header,
            index=False, 
            sep=';',     
            decimal=','  
        )
        logger.info(f"Dados salvos com sucesso em: {file_path}")

    except Exception as e:
        logger.error(f"Erro ao escrever dados para CSV ({file_path}): {e}")