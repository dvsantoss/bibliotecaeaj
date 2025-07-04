# Sistema de Biblioteca - EAJ Macaíba

Sistema moderno de gestão e análise do acervo bibliográfico da Biblioteca Setorial Prof. Rodolfo Helinski - Escola Agrícola de Jundiaí (EAJ) - Macaíba/UFRN.

## 🚀 Funcionalidades

### 📊 Dashboard Interativo
- **Estatísticas em tempo real** do acervo
- **Gráficos dinâmicos** com distribuição por categoria
- **Interface responsiva** e moderna

### 🔍 Sistema de Pesquisa Avançada
- **Busca por texto** em título, autor, subtítulo e assunto
- **Filtros por categoria** (Ciências, Engenharia, Computação)
- **Resultados em tempo real** com paginação

### 📚 Categorização Inteligente
- **Classificação automática** baseada em palavras-chave
- **3 categorias principais**:
  - Ciências da Natureza (Biologia, Agricultura, Ecologia)
  - Engenharia e Tecnologia (Construção, Elétrica, Mecânica)
  - Computação e Software (Programação, Sistemas, Algoritmos)

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Visualização**: ECharts (PyECharts)
- **Processamento de Dados**: Pandas
- **Design**: Interface moderna com gradientes e efeitos visuais

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passos para instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd biblioteca-main
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**
```bash
python app.py
```

4. **Acesse no navegador**
```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
biblioteca-main/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── README.md             # Documentação
├── templates/
│   └── index.html        # Interface principal
├── bd/
│   ├── juncao_csv.csv    # Base de dados principal
│   ├── biblioteca.csv    # Dados da biblioteca
│   └── livros.csv        # Dados dos livros
├── api.ipynb             # Notebook de análise
├── filter.ipynb          # Notebook de filtros
└── software.csv          # Livros de software
```

## 🔧 Configuração

### Variáveis de Ambiente
O sistema utiliza as seguintes configurações padrão:
- **Porta**: 5000
- **Host**: 0.0.0.0
- **Modo**: Debug (desenvolvimento)

### Base de Dados
O sistema lê automaticamente o arquivo `bd/juncao_csv.csv` que deve conter:
- `registro_sistema`: ID único do livro
- `titulo`: Título do livro
- `sub_titulo`: Subtítulo (opcional)
- `assunto`: Assunto/classificação
- `autor`: Autor do livro
- `ano`: Ano de publicação
- `editora`: Editora
- Outros campos bibliográficos

## 📊 API Endpoints

### GET `/api/stats`
Retorna estatísticas do acervo
```json
{
  "total": 3255,
  "ciencia": 1375,
  "engenharia": 1148,
  "software": 732
}
```

### GET `/api/search?q=termo&category=categoria`
Pesquisa livros por termo e categoria
```json
{
  "results": [...],
  "total": 25
}
```

### GET `/api/books`
Retorna lista inicial de livros
```json
{
  "results": [...],
  "total": 50
}
```

## 🎨 Interface

### Características Visuais
- **Design moderno** com gradientes e efeitos de vidro
- **Responsivo** para desktop, tablet e mobile
- **Animações suaves** e transições
- **Ícones intuitivos** do Font Awesome
- **Tipografia clara** com fonte Inter

### Componentes Principais
1. **Navbar** com identificação da biblioteca
2. **Cards de estatísticas** com números destacados
3. **Gráfico interativo** de distribuição por categoria
4. **Seção de pesquisa** com filtros
5. **Lista de resultados** com cards de livros

## 🔍 Como Usar

### Pesquisa Simples
1. Digite um termo no campo de busca
2. Pressione Enter ou clique em "Pesquisar"
3. Visualize os resultados

### Pesquisa por Categoria
1. Selecione uma categoria no dropdown
2. Opcionalmente, adicione um termo de busca
3. Clique em "Pesquisar"

### Visualização de Estatísticas
- Os números são atualizados automaticamente
- O gráfico mostra a distribuição percentual
- Hover sobre o gráfico para detalhes

## 🚀 Melhorias Implementadas

### Interface
- ✅ Design moderno e responsivo
- ✅ Animações e transições suaves
- ✅ Cards com efeito hover
- ✅ Loading states e feedback visual
- ✅ Gráfico interativo com ECharts

### Funcionalidades
- ✅ Sistema de pesquisa avançada
- ✅ Filtros por categoria
- ✅ Busca em tempo real
- ✅ Paginação de resultados
- ✅ Contagem de resultados
- ✅ Categorização automática

### Performance
- ✅ Carregamento assíncrono de dados
- ✅ Cache de resultados
- ✅ Otimização de consultas
- ✅ Interface responsiva

## 📈 Estatísticas Atuais

Baseado no acervo atual:
- **Total de livros**: 3.255
- **Ciências da Natureza**: 1.375 (42%)
- **Engenharia e Tecnologia**: 1.148 (35%)
- **Computação e Software**: 732 (23%)

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Teste a aplicação
5. Envie um pull request

## 👥 Autores

- Gustavo Martins e Davi Santos
- Desenvolvido para a Biblioteca Setorial Prof. Rodolfo Helinski
- Escola Agrícola de Jundiaí (EAJ) - Macaíba
- Universidade Federal do Rio Grande do Norte (UFRN)
- 
## 📞 Suporte

Para dúvidas ou suporte técnico, entre em contato com a gente:

davi.seabra.121@ufrn.edu.br
ou
gustavo.martins.119@ufrn.edu.br
