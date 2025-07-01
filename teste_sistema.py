#!/usr/bin/env python3
"""
Script de teste para verificar se o sistema está funcionando
"""

def testar_dependencias():
    """Testa se todas as dependências estão instaladas"""
    print("🔍 Testando dependências...")
    
    try:
        import flask
        print("✅ Flask instalado")
    except ImportError:
        print("❌ Flask não encontrado")
        return False
    
    try:
        import pandas
        print("✅ Pandas instalado")
    except ImportError:
        print("❌ Pandas não encontrado")
        return False
    
    try:
        import numpy
        print("✅ Numpy instalado")
    except ImportError:
        print("❌ Numpy não encontrado")
        return False
    
    try:
        import pyecharts
        print("✅ PyECharts instalado")
    except ImportError:
        print("❌ PyECharts não encontrado")
        return False
    
    return True

def testar_aplicacao():
    """Testa se a aplicação pode ser importada"""
    print("\n🔍 Testando aplicação...")
    
    try:
        import app
        print("✅ Aplicação importada com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar aplicação: {e}")
        return False

def testar_arquivo_dados():
    """Testa se o arquivo de dados existe"""
    print("\n🔍 Testando arquivo de dados...")
    
    import os
    from pathlib import Path
    
    data_file = Path("bd/juncao_csv.csv")
    if data_file.exists():
        print(f"✅ Arquivo de dados encontrado: {data_file}")
        return True
    else:
        print(f"❌ Arquivo de dados não encontrado: {data_file}")
        return False

def main():
    """Função principal"""
    print("=" * 50)
    print("🧪 TESTE DO SISTEMA DE BIBLIOTECA")
    print("=" * 50)
    
    # Testar dependências
    deps_ok = testar_dependencias()
    
    # Testar aplicação
    app_ok = testar_aplicacao()
    
    # Testar arquivo de dados
    data_ok = testar_arquivo_dados()
    
    print("\n" + "=" * 50)
    print("📊 RESULTADO DOS TESTES")
    print("=" * 50)
    
    if deps_ok and app_ok and data_ok:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O sistema está pronto para uso")
        print("\n🚀 Para executar o sistema:")
        print("   python app.py")
        print("   ou")
        print("   python run.py")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("🔧 Verifique os erros acima e corrija")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 