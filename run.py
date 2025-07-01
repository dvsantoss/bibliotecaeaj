#!/usr/bin/env python3
"""
Script de execução para o Sistema de Biblioteca EAJ Macaíba
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Erro: Python 3.8 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detectado")

def install_requirements():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        sys.exit(1)

def check_data_files():
    """Verifica se os arquivos de dados existem"""
    data_file = Path("bd/juncao_csv.csv")
    if not data_file.exists():
        print("❌ Erro: Arquivo de dados não encontrado")
        print("Certifique-se de que o arquivo 'bd/juncao_csv.csv' existe")
        sys.exit(1)
    print("✅ Arquivo de dados encontrado")

def run_app():
    """Executa a aplicação Flask"""
    print("🚀 Iniciando o Sistema de Biblioteca...")
    print("📊 Dashboard disponível em: http://localhost:5000")
    print("⏹️  Pressione Ctrl+C para parar")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar a aplicação: {e}")
        sys.exit(1)

def main():
    """Função principal"""
    print("=" * 50)
    print("📚 Sistema de Biblioteca - EAJ Macaíba")
    print("=" * 50)
    
    # Verificações iniciais
    check_python_version()
    check_data_files()
    
    # Perguntar se deve instalar dependências
    try:
        import flask
        import pandas
        print("✅ Dependências já instaladas")
    except ImportError:
        response = input("📦 Instalar dependências? (s/n): ").lower()
        if response in ['s', 'sim', 'y', 'yes']:
            install_requirements()
        else:
            print("❌ Dependências não instaladas. Execute: pip install -r requirements.txt")
            sys.exit(1)
    
    # Executar aplicação
    run_app()

if __name__ == "__main__":
    main() 