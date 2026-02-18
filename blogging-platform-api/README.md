# 📝 Blogging Platform API

Uma API RESTful robusta e assíncrona para gerenciamento de uma plataforma de blogs. Desenvolvida em Python, esta API permite criar, ler, atualizar, deletar e buscar posts, incluindo um sistema dinâmico de relacionamento muitos-para-muitos com Tags.

## 🚀 Recursos

- **CRUD**: Crie, liste, atualize e delete postagens do blog.
- **Gerenciamento de Tags**: Criação de novas tags automaticamente ou reaproveita tags existentes (relacionamento _Many-to-Many_).
- **Busca e Filtros**: Busque posts específicos utilizando termos que filtram por título, conteúdo ou categoria (`?term=`).
- **Validação**: Validação de dados de entrada e saída, garantindo integridade (ex: tamanho mínimo de caracteres) e retornando erros semânticos (400, 404, ...).
- **Documentação Automática**: Interface interativa do Swagger UI gerada automaticamente.

## 🛠️ Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e de alta performance.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM (Object Relational Mapper) para comunicação com o banco de dados.
- **[SQLite](https://www.sqlite.org/index.html)**: Banco de dados leve e embutido.
- **[Alembic](https://alembic.sqlalchemy.org/)**: Ferramenta para migrações de banco de dados (versionamento do banco).
- **[Pydantic V2](https://docs.pydantic.dev/)**: Validação e serialização de dados (Schemas).
- **[Pytest](https://docs.pytest.org/) & [HTTPX](https://www.python-httpx.org/)**: Suite de testes automatizados assíncronos.
- **[Poetry](https://python-poetry.org/)**: Gerenciamento de dependências e ambientes virtuais.

---

## 💻 Configurar e Executar

### Pré-requisitos

- Python 3.11+ instalado
- [Poetry](https://python-poetry.org/docs/#installation) instalado na sua máquina

### 1. Clonar o repositório

```bash
git clone [https://github.com/SEU_USUARIO/blogging-platform-api.git](https://github.com/SEU_USUARIO/blogging-platform-api.git)
cd blogging-platform-api
```

### 2. Instalar as dependências

Como o projeto utiliza o Poetry, a instalação das dependências e a criação do ambiente virtual são feitas com um único comando:

```bash
poetry install
```

Inicie o ambiente virtual criado pelo Poetry:

```bash
poetry venv activate
```

### 3. Configurar o Banco de Dados

O projeto utiliza o Alembic para gerenciar o banco de dados. Para criar as tabelas no SQLite localmente, rode as migrações:

```bash
alembic upgrade head
```

### 4. Executar o Servidor

```
uvicorn main:app --reload
```

## 📖 Documentação da API

Com o servidor rodando, acesse seu navegador:

- **Swagger UI**: http://127.0.0.1:8000/docs

## 🧪 Executando Testes

Para rodar os testes dos end-points da API utilizando um banco de dados temporário em memória, execute:

```
pytest -v
```
