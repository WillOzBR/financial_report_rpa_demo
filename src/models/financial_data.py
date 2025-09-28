from dataclasses import dataclass

@dataclass
class FinancialData:
    data_coleta: str
    fonte_informacao: str
    valor_alta: float
    valor_baixa: float
    valor_fechamento: float