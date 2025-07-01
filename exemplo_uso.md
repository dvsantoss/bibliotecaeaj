# 📚 Exemplo de Uso - Sistema de Biblioteca EAJ Macaíba

## 🚀 Como Executar

### Opção 1: Script Automático (Recomendado)
```bash
python run.py
```

### Opção 2: Execução Direta
```bash
python app.py
```

### Opção 3: Com Flask
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## 🌐 Acessando o Sistema

Após executar, acesse: **http://localhost:5000**

## 🔍 Funcionalidades Demonstradas

### 1. Dashboard de Estatísticas
- **Visualização em tempo real** do acervo
- **Gráfico interativo** com distribuição por categoria
- **Cards informativos** com números destacados

### 2. Sistema de Pesquisa

#### Pesquisa Simples
```
Termo: "programação"
Resultado: Livros sobre programação, algoritmos, desenvolvimento
```

#### Pesquisa por Categoria
```
Categoria: "Computação e Software"
Resultado: Todos os livros de TI, sistemas, algoritmos
```

#### Pesquisa Combinada
```
Termo: "engenharia"
Categoria: "Engenharia e Tecnologia"
Resultado: Livros de engenharia específicos
```

### 3. Exemplos de Pesquisas

#### Para Ciências da Natureza:
- **"agricultura"** - Livros sobre agricultura
- **"biologia"** - Livros de biologia
- **"ecologia"** - Livros sobre ecologia e meio ambiente

#### Para Engenharia:
- **"construção"** - Livros sobre construção civil
- **"elétrica"** - Livros de engenharia elétrica
- **"mecânica"** - Livros de mecânica

#### Para Computação:
- **"programação"** - Livros de programação
- **"sistemas"** - Livros sobre sistemas
- **"algoritmo"** - Livros de algoritmos

## 📊 API Endpoints

### Verificar Status do Sistema
```bash
curl http://localhost:5000/api/health
```

### Obter Estatísticas
```bash
curl http://localhost:5000/api/stats
```

### Pesquisar Livros
```bash
# Pesquisa simples
curl "http://localhost:5000/api/search?q=programação"

# Pesquisa por categoria
curl "http://localhost:5000/api/search?category=software"

# Pesquisa combinada
curl "http://localhost:5000/api/search?q=engenharia&category=engenharia"
```

### Listar Livros Iniciais
```bash
curl http://localhost:5000/api/books
```

## 🎯 Casos de Uso Práticos

### 1. Bibliotecário Buscando Livros de Programação
1. Acesse o sistema
2. Digite "programação" no campo de busca
3. Selecione "Computação e Software" na categoria
4. Visualize os resultados com detalhes dos livros

### 2. Professor Pesquisando Material de Agricultura
1. Digite "agricultura" na busca
2. Selecione "Ciências da Natureza"
3. Encontre livros específicos da área

### 3. Aluno Procurando Livros de Engenharia Elétrica
1. Digite "elétrica" na busca
2. Selecione "Engenharia e Tecnologia"
3. Veja disponibilidade e localização dos livros

## 🔧 Configurações Avançadas

### Variáveis de Ambiente
```bash
# Modo de desenvolvimento
export FLASK_ENV=development

# Modo de produção
export FLASK_ENV=production

# Configurar porta
export PORT=8080

# Configurar host
export HOST=0.0.0.0
```

### Personalizar Palavras-chave
Edite o arquivo `config.py` para adicionar novas palavras-chave:

```python
CIENCIA_KEYWORDS = [
    "genética", "biologia", "agricultura", "zootecnia", 
    "meio ambiente", "ecologia", "botânica", "zoologia",
    "microbiologia", "bioquímica", "fisiologia",
    "sua_nova_palavra_chave"  # Adicione aqui
]
```

## 📱 Interface Responsiva

### Desktop
- Dashboard completo com gráficos
- Pesquisa avançada com filtros
- Visualização detalhada dos resultados

### Tablet/Mobile
- Interface adaptada para telas menores
- Navegação otimizada para toque
- Gráficos responsivos

## 🎨 Recursos Visuais

### Animações
- **Hover effects** nos cards
- **Transições suaves** entre páginas
- **Loading states** durante pesquisas
- **Feedback visual** para ações

### Design
- **Gradientes modernos** no fundo
- **Efeitos de vidro** (glassmorphism)
- **Ícones intuitivos** do Font Awesome
- **Tipografia clara** com fonte Inter

## 🔍 Dicas de Pesquisa

### Termos Eficazes
- Use palavras-chave específicas
- Combine termos relacionados
- Utilize sinônimos quando necessário

### Filtros Úteis
- **Categoria**: Para focar em uma área específica
- **Texto**: Para busca livre em todos os campos
- **Combinação**: Para resultados mais precisos

## 📈 Monitoramento

### Logs do Sistema
```bash
# Ver logs em tempo real
tail -f logs/app.log

# Verificar status da API
curl http://localhost:5000/api/health
```

### Métricas
- Número total de livros
- Distribuição por categoria
- Tempo de resposta das consultas
- Uso de memória e CPU

## 🚀 Deploy em Produção

### Usando Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Usando Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🆘 Solução de Problemas

### Erro: "Arquivo de dados não encontrado"
```bash
# Verificar se o arquivo existe
ls -la bd/juncao_csv.csv

# Verificar permissões
chmod 644 bd/juncao_csv.csv
```

### Erro: "Dependências não instaladas"
```bash
# Instalar dependências
pip install -r requirements.txt

# Ou usar o script automático
python run.py
```

### Erro: "Porta já em uso"
```bash
# Mudar porta
export PORT=8080
python app.py

# Ou matar processo na porta 5000
lsof -ti:5000 | xargs kill -9
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do sistema
2. Teste o endpoint de health check
3. Consulte a documentação completa
4. Entre em contato com a equipe técnica 