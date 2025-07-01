"""
Configurações do Sistema de Biblioteca EAJ Macaíba
"""

import os
from pathlib import Path

class Config:
    """Configurações base"""
    
    # Configurações da aplicação
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'biblioteca-eaj-macaiba-2024'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Configurações do servidor
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Configurações de dados
    DATA_FILE = Path('bd/juncao_csv.csv')
    DATA_ENCODING = 'latin1'
    DATA_SEPARATOR = ','
    
    # Configurações de pesquisa
    MAX_RESULTS = 100
    DEFAULT_RESULTS = 50
    
    # Configurações de interface
    ITEMS_PER_PAGE = 20
    SEARCH_DELAY = 300  # ms
    
    # Configurações de cache
    CACHE_TIMEOUT = 300  # 5 minutos
    
    @classmethod
    def get_data_path(cls):
        """Retorna o caminho completo do arquivo de dados"""
        return cls.DATA_FILE.absolute()
    
    @classmethod
    def validate_data_file(cls):
        """Valida se o arquivo de dados existe"""
        return cls.DATA_FILE.exists()

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    HOST = 'localhost'
    PORT = 5000

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000

class TestingConfig(Config):
    """Configurações para testes"""
    DEBUG = True
    TESTING = True
    DATA_FILE = Path('tests/test_data.csv')

# Palavras-chave para categorização
CIENCIA_KEYWORDS = [
    "genética", "biologia", "agricultura", "zootecnia", "meio ambiente", 
    "ecologia", "botânica", "zoologia", "microbiologia", "bioquímica", 
    "fisiologia", "física", "química"
]

ENGENHARIA_KEYWORDS = [
    "construção", "indústria química", "tecnologia agrícola", "controle de qualidade", 
    "engenharia", "cálculo estrutural", "materiais de construção", "elétrica", 
    "eletricidade", "circuitos elétricos", "eletrotécnica", "instalações prediais", 
    "energia renovável", "irrigação e drenagem", "armazenamento e secagem de grãos", 
    "construções rurais", "agricultura de precisão", "máquinas e equipamentos", 
    "gestão produção", "logística", "produção", "qualidade", "pcp", "mecânica", 
    "hidráulica", "pneumática", "automação"
]

SOFTWARE_KEYWORDS = [
    'programação', 'debian', 'computação', 'php', 'inteligência artificial', 'assembly', 
    'algoritmo', 'robô', 'java', 'robótica', 'dados', 'banco dados', 'c++', 'fortram', 
    'sistemas', 'linux', 'redes', 'hardware', 'computador', 'informática', 'ponteiros', 
    'wi-fi', 'i.a', 'códgio', 'codificação', 'html', 'css', 'javascript', 'python', 
    'desenvolvimento', 'software', 'aplicação', 'web'
]

HUMANAS_KEYWORDS = [
    "política", "história", "sociologia", "filosofia", "economia",
    "direito", "educação", "literatura", "arte", "geografia", "antropologia"
]

GESTAO_KEYWORDS = [
    "administração", "gestão", "marketing", "finanças",
    "empreendedorismo", "planejamento", "inovação", "estratégia"
]

NATURAIS_KEYWORDS = [
    "oceanografia", "geologia", "meteorologia", "climatologia", "astronomia"
]

SAUDE_KEYWORDS = [
    "medicina", "enfermagem", "saúde", "saúde pública", "nutrição",
    "fisioterapia", "odontologia", "psicologia", "farmacologia", "epidemiologia"
]

DIREITO_KEYWORDS = [
    "direito", "legislação", "justiça", "processo civil",
    "processo penal", "constituição", "penal", "trabalhista"
]

EDUCACAO_KEYWORDS = [
    "ensino", "pedagogia", "didática", "educação", "escola", "professor"
]

ARQUITETURA_KEYWORDS = [
    "arquitetura", "urbanismo", "planejamento urbano", "paisagismo"
]

TECNOLOGIA_KEYWORDS = [
    "tecnologia", "inovação", "industrial", "ciência aplicada"
]

# Configuração baseada no ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
    'HUMANAS_KEYWORDS': HUMANAS_KEYWORDS,
    'GESTAO_KEYWORDS': GESTAO_KEYWORDS,
    'NATURAIS_KEYWORDS': NATURAIS_KEYWORDS,
    'SAUDE_KEYWORDS': SAUDE_KEYWORDS,
    'DIREITO_KEYWORDS': DIREITO_KEYWORDS,
    'EDUCACAO_KEYWORDS': EDUCACAO_KEYWORDS,
    'ARQUITETURA_KEYWORDS': ARQUITETURA_KEYWORDS,
    'TECNOLOGIA_KEYWORDS': TECNOLOGIA_KEYWORDS
}

def get_config():
    """Retorna a configuração baseada no ambiente"""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])

# Caminho para o arquivo de dados
DATA_PATH = 'bd/juncao_csv_corrigido.csv'

# Palavras-chave para categorização
CIENCIA_KEYWORDS = [
    "genética", "biologia", "agricultura", "zootecnia", "meio ambiente", 
    "ecologia", "botânica", "zoologia", "microbiologia", "bioquímica", 
    "fisiologia", "física", "química"
]

ENGENHARIA_KEYWORDS = [
    "construção", "indústria química", "tecnologia agrícola", "controle de qualidade", 
    "engenharia", "cálculo estrutural", "materiais de construção", "elétrica", 
    "eletricidade", "circuitos elétricos", "eletrotécnica", "instalações prediais", 
    "energia renovável", "irrigação e drenagem", "armazenamento e secagem de grãos", 
    "construções rurais", "agricultura de precisão", "máquinas e equipamentos", 
    "gestão produção", "logística", "produção", "qualidade", "pcp", "mecânica", 
    "hidráulica", "pneumática", "automação"
]

SOFTWARE_KEYWORDS = [
    'programação', 'debian', 'computação', 'php', 'inteligência artificial', 'assembly', 
    'algoritmo', 'robô', 'java', 'robótica', 'dados', 'banco dados', 'c++', 'fortram', 
    'sistemas', 'linux', 'redes', 'hardware', 'computador', 'informática', 'ponteiros', 
    'wi-fi', 'i.a', 'códgio', 'codificação', 'html', 'css', 'javascript', 'python', 
    'desenvolvimento', 'software', 'aplicação', 'web'
]

HUMANAS_KEYWORDS = [
    "política", "história", "sociologia", "filosofia", "economia",
    "direito", "educação", "literatura", "arte", "geografia", "antropologia"
]

GESTAO_KEYWORDS = [
    "administração", "gestão", "marketing", "finanças",
    "empreendedorismo", "planejamento", "inovação", "estratégia"
]

NATURAIS_KEYWORDS = [
    "oceanografia", "geologia", "meteorologia", "climatologia", "astronomia"
]

SAUDE_KEYWORDS = [
    "medicina", "enfermagem", "saúde", "saúde pública", "nutrição",
    "fisioterapia", "odontologia", "psicologia", "farmacologia", "epidemiologia"
] 
