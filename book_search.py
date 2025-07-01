#!/usr/bin/env python3
"""
Sistema de Busca de Livros
Terminal interativo para buscar livros na base de dados local.
"""

import pandas as pd
from pathlib import Path
import sys

class BookSearch:
    """Sistema de busca de livros na base de dados."""
    
    def __init__(self, data_file: str = "bd/juncao_csv_corrigido.csv"):
        """
        Inicializa o sistema de busca.
        
        Args:
            data_file: Caminho para o arquivo de dados dos livros (CSV).
        """
        self.data_file = Path(data_file)
        self.books_data = None
        self._load_books_data()

    def _load_books_data(self):
        """Carrega os dados dos livros do arquivo CSV."""
        try:
            if not self.data_file.exists():
                print(f"❌ Erro: Arquivo de dados não encontrado em '{self.data_file}'")
                sys.exit(1)
            
            self.books_data = pd.read_csv(self.data_file, encoding='latin1', low_memory=False)
            # Converter colunas de busca para string para evitar erros de tipo
            for col in ['titulo', 'autor', 'assunto']:
                if col in self.books_data.columns:
                    self.books_data[col] = self.books_data[col].astype(str)
            print(f"✅ Base de dados carregada: {len(self.books_data)} livros encontrados.")
        except Exception as e:
            print(f"❌ Erro ao carregar o arquivo de dados: {e}")
            sys.exit(1)

    def search_books(self, query: str) -> pd.DataFrame:
        """
        Busca livros na base de dados que correspondam à consulta.
        A busca é feita nos campos 'titulo', 'autor' e 'assunto'.
        
        Args:
            query: O termo de busca.
            
        Returns:
            Um DataFrame do pandas com os resultados da busca.
        """
        if self.books_data is None or query.strip() == "":
            return pd.DataFrame()

        # Busca case-insensitive
        search_query = query.lower()
        
        results = self.books_data[
            self.books_data['titulo'].str.lower().str.contains(search_query, na=False) |
            self.books_data['autor'].str.lower().str.contains(search_query, na=False) |
            self.books_data['assunto'].str.lower().str.contains(search_query, na=False)
        ]
        
        return results

    def display_results(self, results: pd.DataFrame):
        """
        Exibe os resultados da busca de forma formatada.
        
        Args:
            results: DataFrame com os livros encontrados.
        """
        print("\n" + "=" * 60)
        if results.empty:
            print("❌ Nenhum livro encontrado para sua busca.")
            return

        print(f"🔎 {len(results)} livro(s) encontrado(s):")
        print("-" * 60)
        
        # Colunas para exibir
        display_columns = ['titulo', 'autor', 'assunto', 'localizacao', 'status_material']
        
        for _, book in results.iterrows():
            print(f"📖 Título: {book.get('titulo', 'N/A')}")
            print(f"   👤 Autor: {book.get('autor', 'N/A')}")
            print(f"   📂 Assunto: {book.get('assunto', 'N/A')}")
            print(f"   📍 Localização: {book.get('localizacao', 'N/A')}")
            print(f"   ℹ️ Status: {book.get('status_material', 'N/A')}")
            print("-" * 40)

def main():
    """Função principal do terminal de busca."""
    print("=" * 60)
    print("📖 Sistema de Busca de Livros da Biblioteca")
    print("=" * 60)
    
    try:
        # Inicializar o sistema de busca
        search_system = BookSearch()
        
        print("\n🎯 Como usar:")
        print("- Digite um termo para buscar (título, autor ou assunto).")
        print("- Digite 'sair' para encerrar.")
        print("-" * 60)
        
        while True:
            try:
                query = input("\n🔍 Digite sua busca: ").strip()
                
                if query.lower() in ['sair', 'exit', 'quit', 'q']:
                    print("\n👋 Obrigado por usar o sistema de busca!")
                    break
                
                if not query:
                    print("❌ Por favor, digite um termo para buscar.")
                    continue
                
                # Realizar a busca e exibir os resultados
                results = search_system.search_books(query)
                search_system.display_results(results)
                
            except KeyboardInterrupt:
                print("\n\n👋 Sistema encerrado pelo usuário.")
                break
            except Exception as e:
                print(f"❌ Ocorreu um erro: {e}")
                continue
                
    except Exception as e:
        print(f"❌ Erro fatal ao inicializar o sistema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 