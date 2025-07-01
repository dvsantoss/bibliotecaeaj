import pandas as pd
from config import get_config
import sys

# Garante que o terminal possa imprimir UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def verificar_arquivo_dados():
    """
    Lê o arquivo de dados configurado e imprime as primeiras linhas para verificação.
    """
    print("--- Verificando o arquivo de dados configurado ---")
    
    try:
        config = get_config()
        data_path = config.get_data_path()
        encoding = config.DATA_ENCODING

        print(f"Caminho do arquivo: {data_path}")
        print(f"Codificação esperada: {encoding}")

        df = pd.read_csv(data_path, encoding=encoding, sep=',')
        
        print("\n✅ Arquivo lido com sucesso!")
        print("\nPrimeiros 10 títulos do arquivo:")
        
        # Pega os 10 primeiros títulos únicos e não nulos
        titulos_validos = df['titulo'].dropna().unique()[:10]
        
        for i, title in enumerate(titulos_validos):
            print(f"  {i+1}. {title}")
            
    except FileNotFoundError:
        print(f"\n❌ ERRO: O arquivo '{data_path}' não foi encontrado.")
    except Exception as e:
        print(f"\n❌ ERRO ao ler o arquivo: {e}")

    print("\n--- Fim da verificação ---")

if __name__ == '__main__':
    verificar_arquivo_dados() 