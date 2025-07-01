#!/usr/bin/env python3
"""
Sistema de Recomendação de Livros usando Gemini AI
Terminal interativo para recomendações de livros baseadas em tópicos de aprendizado
"""

import os
import sys
import google.generativeai as genai
from pathlib import Path
import pandas as pd
from typing import List, Dict, Optional
import json

class BookRecommender:
    """Sistema de recomendação de livros usando Gemini AI"""
    
    def __init__(self, api_key: str, data_file: str = "bd/juncao_csv_corrigido.csv"):
        """
        Inicializa o sistema de recomendação
        
        Args:
            api_key: Chave da API do Gemini
            data_file: Caminho para o arquivo de dados dos livros
        """
        self.api_key = api_key
        self.data_file = Path(data_file)
        self.books_data = None
        self.model = None
        
        # Configurar Gemini AI
        self._setup_gemini()
        
        # Carregar dados dos livros
        self._load_books_data()
    
    def _setup_gemini(self):
        """Configura a API do Gemini"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("✅ Gemini AI configurado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao configurar Gemini AI: {e}")
            sys.exit(1)
    
    def _load_books_data(self):
        """Carrega os dados dos livros do arquivo CSV"""
        try:
            if not self.data_file.exists():
                print(f"❌ Arquivo de dados não encontrado: {self.data_file}")
                sys.exit(1)
            
            self.books_data = pd.read_csv(self.data_file, encoding='latin1')
            print(f"✅ Dados carregados: {len(self.books_data)} livros encontrados")
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            sys.exit(1)
    
    def get_book_recommendations(self, topic: str, num_recommendations: int = 5) -> List[Dict]:
        """
        Obtém recomendações de livros para um tópico específico
        
        Args:
            topic: Tópico ou área de interesse
            num_recommendations: Número de recomendações desejadas
            
        Returns:
            Lista de dicionários com informações dos livros recomendados
        """
        try:
            # Preparar contexto com dados dos livros disponíveis
            books_context = self._prepare_books_context()
            
            # Prompt para o Gemini
            prompt = f"""
            Você é um especialista em bibliotecas e recomendações de livros.
            
            Baseado no tópico "{topic}", recomende {num_recommendations} livros da biblioteca.
            
            Dados dos livros disponíveis:
            {books_context}
            
            Instruções:
            1. Analise o tópico solicitado
            2. Identifique livros relevantes da biblioteca
            3. Retorne apenas os livros mais apropriados
            4. Para cada livro, forneça:
               - Título
               - Autor
               - Assunto
               - Justificativa da recomendação
            
            Formato da resposta (JSON):
            {{
                "recommendations": [
                    {{
                        "title": "Título do Livro",
                        "author": "Nome do Autor",
                        "subject": "Assunto",
                        "justification": "Por que este livro é recomendado para o tópico"
                    }}
                ]
            }}
            
            Tópico solicitado: {topic}
            """
            
            # Fazer chamada para o Gemini
            response = self.model.generate_content(prompt)
            
            # Processar resposta
            recommendations = self._parse_gemini_response(response.text)
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Erro ao obter recomendações: {e}")
            return []
    
    def _prepare_books_context(self) -> str:
        """Prepara o contexto dos livros para o prompt"""
        if self.books_data is None:
            return "Nenhum dado de livro disponível"
        
        # Selecionar colunas relevantes (usando os nomes corretos do CSV)
        relevant_columns = ['titulo', 'autor', 'assunto', 'sub_titulo']
        available_columns = [col for col in relevant_columns if col in self.books_data.columns]
        
        if not available_columns:
            return "Dados de livros disponíveis, mas colunas não identificadas"
        
        # Criar resumo dos livros (primeiros 50 para não sobrecarregar o prompt)
        books_summary = self.books_data[available_columns].head(50).to_string(index=False)
        return f"Primeiros 50 livros da biblioteca:\n{books_summary}"
    
    def _parse_gemini_response(self, response_text: str) -> List[Dict]:
        """Processa a resposta do Gemini e extrai as recomendações"""
        try:
            # Tentar extrair JSON da resposta
            if '{' in response_text and '}' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                
                data = json.loads(json_str)
                return data.get('recommendations', [])
            else:
                # Fallback: tentar extrair informações manualmente
                return self._extract_recommendations_manual(response_text)
                
        except json.JSONDecodeError:
            # Fallback para parsing manual
            return self._extract_recommendations_manual(response_text)
        except Exception as e:
            print(f"❌ Erro ao processar resposta: {e}")
            return []
    
    def _extract_recommendations_manual(self, response_text: str) -> List[Dict]:
        """Extrai recomendações manualmente da resposta do Gemini"""
        recommendations = []
        lines = response_text.split('\n')
        
        current_book = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'título' in line.lower() or 'title' in line.lower():
                if current_book:
                    recommendations.append(current_book)
                current_book = {'title': line.split(':', 1)[-1].strip()}
            elif 'autor' in line.lower() or 'author' in line.lower():
                current_book['author'] = line.split(':', 1)[-1].strip()
            elif 'assunto' in line.lower() or 'subject' in line.lower():
                current_book['subject'] = line.split(':', 1)[-1].strip()
            elif 'justificativa' in line.lower() or 'justification' in line.lower():
                current_book['justification'] = line.split(':', 1)[-1].strip()
        
        if current_book:
            recommendations.append(current_book)
        
        return recommendations
    
    def display_recommendations(self, recommendations: List[Dict], topic: str):
        """Exibe as recomendações de forma formatada"""
        print(f"\n📚 Recomendações para: {topic}")
        print("=" * 60)
        
        if not recommendations:
            print("❌ Nenhuma recomendação encontrada para este tópico.")
            return
        
        for i, book in enumerate(recommendations, 1):
            print(f"\n{i}. 📖 {book.get('title', 'Título não disponível')}")
            print(f"   👤 Autor: {book.get('author', 'Autor não disponível')}")
            print(f"   📂 Assunto: {book.get('subject', 'Assunto não disponível')}")
            print(f"   💡 Justificativa: {book.get('justification', 'Justificativa não disponível')}")
            print("-" * 40)

def main():
    """Função principal do terminal interativo"""
    print("=" * 60)
    print("📚 Sistema de Recomendação de Livros - Gemini AI")
    print("=" * 60)
    
    # Configurar API Key
    api_key = "AIzaSyDxLIpUjBFruuuNLAmZ36WllH0Ymy_kLSk"
    
    try:
        # Inicializar sistema
        recommender = BookRecommender(api_key)
        
        print("\n🎯 Como usar:")
        print("- Digite um tópico ou área que você quer aprender")
        print("- Exemplos: 'programação Python', 'biologia molecular', 'engenharia civil'")
        print("- Digite 'sair' para encerrar")
        print("-" * 60)
        
        while True:
            try:
                # Obter input do usuário
                topic = input("\n🤔 Sobre qual tópico você quer aprender? ").strip()
                
                if topic.lower() in ['sair', 'exit', 'quit', 'q']:
                    print("\n👋 Obrigado por usar o Sistema de Recomendação de Livros!")
                    break
                
                if not topic:
                    print("❌ Por favor, digite um tópico válido.")
                    continue
                
                print(f"\n🔍 Buscando recomendações para: {topic}")
                print("⏳ Aguarde um momento...")
                
                # Obter recomendações
                recommendations = recommender.get_book_recommendations(topic, num_recommendations=5)
                
                # Exibir resultados
                recommender.display_recommendations(recommendations, topic)
                
            except KeyboardInterrupt:
                print("\n\n👋 Sistema encerrado pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                continue
    
    except Exception as e:
        print(f"❌ Erro ao inicializar o sistema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 