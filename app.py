import argparse

from src.config import logger, CSV_REPORT_PATH
from src.utils.csv_writer import write_data_to_csv
from src.api.client import get_usd_brl_daily_data
from src.scraping.scraper import get_usd_brl_weekly_data

def main():
    """
    Função principal que orquestra a coleta de dados,
    determinando o modo de execução (API, Scraping, ou ALL) via argumento.
    """
    parser = argparse.ArgumentParser(
        description="Coleta e persistência de dados de câmbio USD/BRL de múltiplas fontes."
    )
    
    parser.add_argument( # Definição de argumentos de execução. "mode"
        'mode', 
        choices=['api', 'scraping', 'all'],
        help="O modo de coleta a ser executado: 'api', 'scraping', ou 'all' (ambos)."
    )
    
    args = parser.parse_args()
    
    logger.info(f"--- INÍCIO DO PROCESSO DE COLETA E PROCESSAMENTO DE DADOS (Modo: {args.mode.upper()}) ---")

    dados_coletados = []
    
    # COLETA VIA API (Histórico Diário)
    if args.mode in ['api', 'all']:
        logger.info("Tentando coletar dados diários via API...")
        dados_api = get_usd_brl_daily_data()
        dados_coletados.extend(dados_api)
        logger.info(f"API retornou {len(dados_api)} registros.")

    # COLETA VIA SCRAPING (Histórico Semanal)
    if args.mode in ['scraping', 'all']:
        logger.info("Tentando coletar dados semanais via Web Scraping (Selenium/BS4)...")
        dados_scrape = get_usd_brl_weekly_data()
        dados_coletados.extend(dados_scrape)
        logger.info(f"Scraping retornou {len(dados_scrape)} registros.")

    
    if not dados_coletados:
        logger.warning("Nenhum dado foi coletado. Encerrando.")
        return

    # 3. EXPORTAR PARA CSV (Usando o módulo csv_writer)
    logger.info(f"Total de registros a serem salvos: {len(dados_coletados)}")
    
    write_data_to_csv(
        data=dados_coletados, 
        file_path=CSV_REPORT_PATH, 
        overwrite=True # Sobrescreve a cada execução
    )

    logger.info("--- PROCESSO CONCLUÍDO COM SUCESSO ---\n\n")

if __name__ == '__main__':
    main()