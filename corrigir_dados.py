import pandas as pd
from pathlib import Path

def converter_csv_para_utf8_corrigido(arquivo_entrada, arquivo_saida):
    """
    Lê um arquivo CSV que foi salvo incorretamente (dupla codificação) 
    e o salva corretamente em UTF-8.
    """
    try:
        caminho_entrada = Path(arquivo_entrada)
        caminho_saida = Path(arquivo_saida)

        if not caminho_entrada.exists():
            print(f"❌ Erro: O arquivo de entrada '{caminho_entrada}' não foi encontrado.")
            return

        print(f"🔄 Lendo o arquivo binário de '{caminho_entrada}'...")
        
        # Lê o arquivo em modo binário e decodifica corretamente
        with open(caminho_entrada, 'rb') as f:
            raw_data = f.read()
        
        # Desfaz a codificação dupla: primeiro decodifica como utf-8, depois codifica como latin1
        texto_corrigido = raw_data.decode('utf-8', errors='ignore').encode('latin1').decode('utf-8')

        # Cria um novo arquivo temporário com o texto corrigido
        caminho_temp = caminho_entrada.parent / "temp_corrigido.csv"
        with open(caminho_temp, 'w', encoding='utf-8') as f:
            f.write(texto_corrigido)

        print("✅ Decodificação dupla corrigida. Lendo para o pandas...")
        
        # Lê o arquivo temporário agora que está em UTF-8 válido
        df = pd.read_csv(caminho_temp, sep=',', on_bad_lines='skip')
        
        print(f"💾 Salvando o arquivo final '{caminho_saida}' com encoding 'utf-8'...")
        df.to_csv(caminho_saida, index=False, encoding='utf-8', sep=',')
        
        # Remove o arquivo temporário
        caminho_temp.unlink()
        
        print("🎉 Conversão final concluída com sucesso!")

    except Exception as e:
        print(f"❌ Ocorreu um erro durante a conversão: {e}")

if __name__ == '__main__':
    arquivo_original = 'bd/juncao_csv.csv'
    arquivo_corrigido_final = 'bd/dados_corrigidos.csv' # Vamos sobrescrever o antigo
    
    converter_csv_para_utf8_corrigido(arquivo_original, arquivo_corrigido_final) 