from flask import Flask, render_template, request, jsonify
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
from config import get_config, DATA_PATH, CIENCIA_KEYWORDS, ENGENHARIA_KEYWORDS, SOFTWARE_KEYWORDS, HUMANAS_KEYWORDS, GESTAO_KEYWORDS, NATURAIS_KEYWORDS, SAUDE_KEYWORDS, DIREITO_KEYWORDS, EDUCACAO_KEYWORDS, ARQUITETURA_KEYWORDS, TECNOLOGIA_KEYWORDS
import unicodedata
import os
import requests
from typing import List, Dict
import re

app = Flask(__name__)
app.config.from_object(get_config())

# Configurar GitHub API
GITHUB_API_BASE = "https://api.github.com"
GITHUB_HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer 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",
    "X-GitHub-Api-Version": "2022-11-28"
}

def fix_text_encoding(text):
    """Corrige strings que foram salvas com codificação dupla (ex: latin1 lido como utf-8)."""
    if not isinstance(text, str):
        return text
    try:
        # A 'mágica' para corrigir a codificação dupla
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Caso algum texto não siga o padrão, retorna o original
        return text

def normalize_text(text):
    """Converte para minúsculas e remove acentos."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')

def correct_encoding(text):
    if isinstance(text, str):
        try:
            return text.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            return text
    return text

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Arquivo de dados não encontrado em: {DATA_PATH}")
    
    # Carrega os dados, o pandas vai usar o cabeçalho do próprio arquivo
    df = pd.read_csv(DATA_PATH, encoding='latin1', low_memory=False, on_bad_lines='warn')
    
    # Seleciona apenas as colunas que realmente vamos usar
    colunas_para_usar = [
        'titulo', 'sub_titulo', 'autor', 'editora', 'ano', 'assunto'
    ]
    # Filtra o DataFrame para manter apenas as colunas de interesse
    df = df[colunas_para_usar]

    # Aplica a correção de codificação apenas nas colunas mantidas
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(correct_encoding)
        
    # Converte 'ano' para numérico, tratando erros
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce').fillna(0).astype(int)
    
    return df

def categorize_book(row):
    text_data = ' '.join(str(row[col]).lower() for col in ['titulo', 'sub_titulo', 'assunto'] if pd.notna(row[col]))
    if any(keyword in text_data for keyword in CIENCIA_KEYWORDS):
        return 'ciencia'
    if any(keyword in text_data for keyword in ENGENHARIA_KEYWORDS):
        return 'engenharia'
    if any(keyword in text_data for keyword in SOFTWARE_KEYWORDS):
        return 'software'
    if any(keyword in text_data for keyword in HUMANAS_KEYWORDS):
        return 'humanas'
    if any(keyword in text_data for keyword in GESTAO_KEYWORDS):
        return 'gestao'
    if any(keyword in text_data for keyword in NATURAIS_KEYWORDS):
        return 'naturais'
    if any(keyword in text_data for keyword in SAUDE_KEYWORDS):
        return 'saude'
    if any(keyword in text_data for keyword in DIREITO_KEYWORDS):
        return 'direito'
    if any(keyword in text_data for keyword in EDUCACAO_KEYWORDS):
        return 'educacao'
    if any(keyword in text_data for keyword in ARQUITETURA_KEYWORDS):
        return 'arquitetura'
    if any(keyword in text_data for keyword in TECNOLOGIA_KEYWORDS):
        return 'tecnologia'
    return 'outros'

def search_books(df, query, category):
    """
    Pesquisa livros no DataFrame baseado em query e categoria
    """
    if df.empty:
        return []
    
    # Normalizar a query de busca
    query_normalized = normalize_text(query) if query else ""
    
    # Filtrar por categoria se especificada
    if category and category != 'all':
        df['category'] = df.apply(
            lambda row: categorize_book(row), 
            axis=1
        )
        df = df[df['category'] == category]
    
    # Se não há query, retornar todos os livros (limitado)
    if not query_normalized:
        config = get_config()
        return df.head(config.MAX_RESULTS).to_dict('records')
    
    # Pesquisar nos campos título, subtítulo, autor e assunto
    search_fields = ['titulo', 'sub_titulo', 'autor', 'assunto']
    results = []
    
    for _, row in df.iterrows():
        # Normalizar todos os campos de texto da linha
        row_text = ' '.join([
            normalize_text(str(row[field])) 
            for field in search_fields 
            if pd.notna(row[field])
        ])
        
        # Verificar se a query está presente no texto normalizado
        if query_normalized in row_text:
            # Converter a linha para dicionário e adicionar à lista de resultados
            book_dict = row.to_dict()
            # Limpar valores NaN
            for key, value in book_dict.items():
                if pd.isna(value):
                    book_dict[key] = ''
            results.append(book_dict)
    
    # Limitar o número de resultados
    config = get_config()
    return results[:config.MAX_RESULTS]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    try:
        df = load_data()
        total = len(df)
        
        df['category'] = df.apply(lambda row: categorize_book(row), axis=1)
        counts = df['category'].value_counts()
        
        # Prepare stats for all categories
        stats = {
            'total': total,
            'ciencia': int(counts.get('ciencia', 0)),
            'engenharia': int(counts.get('engenharia', 0)),
            'software': int(counts.get('software', 0)),
            'humanas': int(counts.get('humanas', 0)),
            'gestao': int(counts.get('gestao', 0)),
            'naturais': int(counts.get('naturais', 0)),
            'saude': int(counts.get('saude', 0)),
            'direito': int(counts.get('direito', 0)),
            'educacao': int(counts.get('educacao', 0)),
            'arquitetura': int(counts.get('arquitetura', 0)),
            'tecnologia': int(counts.get('tecnologia', 0)),
            'outros': int(counts.get('outros', 0)),
        }
        # Get top 3 categories (excluding 'outros')
        top_categories = [cat for cat in counts.index if cat != 'outros'][:3]
        top_stats = [
            {'category': cat, 'count': int(counts[cat])}
            for cat in top_categories
        ]
        stats['top_categories'] = top_stats
        return jsonify(stats)
    except Exception as e:
        print(f"Erro ao gerar estatísticas: {e}")
        return jsonify({"error": "Falha ao carregar dados das estatísticas."}), 500

@app.route('/api/search')
def search():
    # Obter parâmetros da requisição
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    # --- LOGGING DETALHADO ---
    print("="*50)
    print("🔍 NOVA PESQUISA RECEBIDA")
    print(f"  - Termo (q): '{query}'")
    print(f"  - Categoria: '{category}'")
    
    # Carregar dados e logar
    df = load_data()
    if df.empty:
        print("  - ❌ ERRO: DataFrame vazio. Não foi possível carregar os dados.")
        return jsonify({'results': [], 'total': 0})
    else:
        print(f"  - ✅ Dados carregados com sucesso: {len(df)} registros.")

    # Executar busca e logar
    results = search_books(df, query, category)
    print(f"  - 🔎 Resultados encontrados: {len(results)}")
    
    # Logar os primeiros resultados (se houver)
    if len(results) > 0:
        print("  - 📚 Primeiros 3 resultados:")
        for i, res in enumerate(results[:3]):
            print(f"    {i+1}. {res.get('titulo', 'N/A')}")
    
    print("="*50)
    # --- FIM DO LOGGING ---

    return jsonify({
        'results': results,
        'total': len(results)
    })

@app.route('/api/books')
def get_books():
    """Retorna uma lista paginada de todos os livros"""
    try:
        # Obter parâmetros de paginação
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        df = load_data()
        if df.empty:
            return jsonify({'results': [], 'total': 0, 'page': page, 'per_page': per_page})
        
        # Calcular paginação
        total_books = len(df)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        # Obter a página atual
        page_data = df.iloc[start_idx:end_idx]
        results = page_data.to_dict('records')
        
        # Limpar valores NaN
        for result in results:
            for key, value in result.items():
                if pd.isna(value):
                    result[key] = ''
        
        return jsonify({
            'results': results,
            'total': total_books,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_books + per_page - 1) // per_page
        })
    except Exception as e:
        print(f"Erro ao carregar livros: {e}")
        return jsonify({'error': 'Falha ao carregar livros.'}), 500

def search_github_repositories(query: str, language: str = None, max_results: int = 10) -> List[Dict]:
    """
    Busca repositórios no GitHub baseado na query
    """
    try:
        # Construir query de busca
        search_query = f"{query}"
        if language:
            search_query += f" language:{language}"
        
        # Adicionar filtros para repositórios educacionais
        search_query += " stars:>10 fork:>5"
        
        url = f"{GITHUB_API_BASE}/search/repositories"
        params = {
            'q': search_query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': max_results
        }
        
        response = requests.get(url, headers=GITHUB_HEADERS, params=params)
        response.raise_for_status()
        
        data = response.json()
        repositories = []
        
        for repo in data.get('items', []):
            repo_info = {
                'name': repo['name'],
                'full_name': repo['full_name'],
                'description': repo['description'] or 'Sem descrição',
                'language': repo['language'] or 'Não especificado',
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'url': repo['html_url'],
                'topics': repo.get('topics', []),
                'created_at': repo['created_at'],
                'updated_at': repo['updated_at']
            }
            repositories.append(repo_info)
        
        return repositories
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na busca do GitHub: {e}")
        return []

def search_github_topics(query: str) -> List[str]:
    """
    Busca tópicos relacionados no GitHub
    """
    try:
        url = f"{GITHUB_API_BASE}/search/topics"
        params = {
            'q': query,
            'per_page': 10
        }
        
        response = requests.get(url, headers=GITHUB_HEADERS, params=params)
        response.raise_for_status()
        
        data = response.json()
        return [topic['name'] for topic in data.get('items', [])]
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao buscar tópicos: {e}")
        return []

def search_searxng_pdfs(query: str, max_results: int = 5) -> list:
    """Search local SearXNG instance for PDFs related to the query."""
    try:
        searxng_url = "http://localhost:8080/search"
        params = {
            'q': f'{query} filetype:pdf',
            'categories': 'files',
            'format': 'json',
            'language': 'pt-BR',
            'safesearch': 1,
            'count': max_results * 2  # Request more results to filter PDFs
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        print(f"🔍 Tentando buscar PDFs no SearXNG local: {searxng_url}")
        resp = requests.get(searxng_url, params=params, headers=headers, timeout=10)
        
        if resp.status_code != 200:
            print(f"❌ Erro ao buscar PDFs no SearXNG local: {resp.status_code}")
            print(f"Resposta: {resp.text[:200]}...")  # Mostrar apenas os primeiros 200 caracteres
            return []
        
        data = resp.json()
        
        pdfs = []
        for result in data.get('results', []):
            url = result.get('url', '')
            # Check if it's a PDF file
            if url.lower().endswith('.pdf') or 'pdf' in result.get('title', '').lower():
                pdfs.append({
                    'title': result.get('title', result['url']),
                    'url': result['url'],
                    'description': result.get('content', ''),
                    'source': 'SearXNG'
                })
            if len(pdfs) >= max_results:
                break
        
        print(f"✅ Encontrados {len(pdfs)} PDFs via SearXNG")
        return pdfs
        
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao SearXNG local. Verifique se o container está rodando.")
        return []
    except requests.exceptions.Timeout:
        print("❌ Timeout ao conectar com SearXNG local.")
        return []
    except Exception as e:
        print(f"❌ Erro ao buscar PDFs no SearXNG local: {e}")
        return []

def get_learning_resources(topic: str, num_recommendations: int = 5) -> List[Dict]:
    """
    Obtém recursos de aprendizado baseado no tópico
    """
    try:
        # Primeiro, buscar livros na biblioteca local
        df = load_data()
        if not df.empty:
            # Buscar livros relacionados ao tópico
            book_results = search_books(df, topic, 'all')
            
            # Formatar livros da biblioteca
            library_books = []
            for book in book_results[:3]:  # Limitar a 3 livros da biblioteca
                library_book = {
                    'title': book.get('titulo', 'Título não disponível'),
                    'author': book.get('autor', 'Autor não disponível'),
                    'subject': book.get('assunto', 'Assunto não disponível'),
                    'type': 'library_book',
                    'justification': f"Livro disponível na biblioteca sobre {topic}",
                    'source': 'Biblioteca Local'
                }
                library_books.append(library_book)
        else:
            library_books = []
        
        # Buscar repositórios do GitHub como complemento
        repositories = search_github_repositories(topic, max_results=num_recommendations - len(library_books))
        
        # Formatar repositórios do GitHub
        github_resources = []
        for repo in repositories:
            github_resource = {
                'title': repo['name'],
                'author': repo['full_name'].split('/')[0],
                'subject': repo['language'] or 'Não especificado',
                'type': 'github_repo',
                'justification': f"Repositório popular com {repo['stars']} estrelas. {repo['description']}",
                'url': repo['url'],
                'stars': repo['stars'],
                'forks': repo['forks'],
                'source': 'GitHub'
            }
            github_resources.append(github_resource)
        
        # Combinar livros da biblioteca e recursos do GitHub
        all_recommendations = library_books + github_resources
        
        # Get extra PDFs from SearXNG
        pdfs = search_searxng_pdfs(topic, max_results=5)  # Increased from 3 to 5
        for pdf in pdfs:
            all_recommendations.append({
                'title': pdf['title'],
                'author': '',
                'subject': 'PDF',
                'type': 'pdf',
                'justification': f"PDF encontrado via SearXNG: {pdf.get('description', 'Conteúdo relacionado ao tópico')}",
                'url': pdf['url'],
                'source': 'SearXNG PDF'
            })
        
        # Fallback: adicionar múltiplas opções de busca se não encontrou PDFs
        if not pdfs:
            # Google search
            google_search_url = f"https://www.google.com/search?q={topic.replace(' ', '+')}+filetype:pdf"
            all_recommendations.append({
                'title': f'Buscar PDFs sobre "{topic}" no Google',
                'author': 'Google',
                'subject': 'PDF',
                'type': 'search_link',
                'justification': 'Link para buscar PDFs relacionados no Google',
                'url': google_search_url,
                'source': 'Google Search'
            })
            
            # Bing search
            bing_search_url = f"https://www.bing.com/search?q={topic.replace(' ', '+')}+filetype:pdf"
            all_recommendations.append({
                'title': f'Buscar PDFs sobre "{topic}" no Bing',
                'author': 'Bing',
                'subject': 'PDF',
                'type': 'search_link',
                'justification': 'Link para buscar PDFs relacionados no Bing',
                'url': bing_search_url,
                'source': 'Bing Search'
            })
            
            # DuckDuckGo search
            ddg_search_url = f"https://duckduckgo.com/?q={topic.replace(' ', '+')}+filetype:pdf"
            all_recommendations.append({
                'title': f'Buscar PDFs sobre "{topic}" no DuckDuckGo',
                'author': 'DuckDuckGo',
                'subject': 'PDF',
                'type': 'search_link',
                'justification': 'Link para buscar PDFs relacionados no DuckDuckGo',
                'url': ddg_search_url,
                'source': 'DuckDuckGo Search'
            })
        
        return all_recommendations[:num_recommendations]
        
    except Exception as e:
        print(f"❌ Erro ao obter recursos de aprendizado: {e}")
        return []

@app.route('/api/recommendations', methods=['POST'])
def get_book_recommendations():
    """Endpoint para obter recomendações de livros e recursos de aprendizado"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        num_recommendations = data.get('num_recommendations', 5)
        
        if not topic:
            return jsonify({'error': 'Tópico é obrigatório'}), 400
        
        # Obter recursos de aprendizado (livros + GitHub)
        resources = get_learning_resources(topic, num_recommendations)
        
        return jsonify({
            'recommendations': resources,
            'topic': topic,
            'total': len(resources)
        })
        
    except Exception as e:
        print(f"❌ Erro ao obter recomendações: {e}")
        return jsonify({'error': 'Falha ao obter recomendações'}), 500

@app.route('/api/health')
def health_check():
    """Endpoint para verificar a saúde da aplicação"""
    try:
        df = load_data()
        return jsonify({
            'status': 'healthy',
            'data_loaded': not df.empty,
            'total_records': len(df) if not df.empty else 0,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 