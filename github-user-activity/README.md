# GitHub User Activity CLI

Projeto desenvolvido como parte do **roadmap de Python do roadmap.sh**, com o objetivo de praticar o consumo de **APIs REST**, manipulação de **JSON** e criação de uma **aplicação de linha de comando (CLI)** utilizando apenas bibliotecas padrão do Python.

---

## 📌 Sobre o projeto

O **GitHub User Activity CLI** é uma ferramenta de linha de comando que busca e exibe as atividades recentes de um usuário do GitHub diretamente no terminal.

A aplicação consome a **API pública do GitHub** para obter eventos recentes e os apresenta de forma legível, como por exemplo:

* Push de commits em repositórios
* Abertura de issues
* Repositórios estrelados
* Comentários em issues

O projeto foi intencionalmente mantido simples, com foco **educacional**, servindo como introdução prática ao uso de APIs.

---

## 🚀 Funcionalidades

* Aceita o **username do GitHub** como argumento via terminal
* Consome o endpoint de eventos do GitHub
* Processa e exibe diferentes tipos de eventos
* Evita exibição duplicada de eventos do mesmo tipo para o mesmo repositório
* Utiliza cache simples em memória para reduzir chamadas repetidas à API
* Tratamento básico de erros (usuário inexistente, falha de conexão)

---

## 🧠 Conceitos praticados

Este projeto aborda diretamente os seguintes conceitos de Python e desenvolvimento de software:

* Consumo de APIs REST
* Requisições HTTP com `urllib`
* Manipulação de dados JSON
* Argumentos de linha de comando (`sys.argv`)
* Estruturas de dados (`dict`, `set`, listas)
* Controle de estado da aplicação
* Separação de responsabilidades em funções
* Tratamento de exceções (`try / except`)

---

## 🛠️ Tecnologias utilizadas

* **Python 3**
* **GitHub REST API**
* Bibliotecas padrão do Python:

  * `sys`
  * `json`
  * `urllib.request`
  * `urllib.error`

> ❗ Não foram utilizadas bibliotecas externas como `requests`, conforme proposto no desafio.

---

## 📦 Como executar o projeto

### Pré-requisitos

* Python 3.8+
* Conexão com a internet

### Execução

Clone o repositório:

```bash
git clone https://github.com/SouzaSantosK/Python_Roadmap.git
cd github-user-activity
```

Execute o script passando o username do GitHub:

```bash
python github_activity.py <username>
```

Exemplo:

```bash
python github_activity.py SouzaSantosK
```

---

## 🧩 Estrutura do projeto

```text
github-user-activity/
├── github_activity.py
└── README.md
```

---

## 🔮 Possíveis melhorias futuras

Este projeto cumpre seu papel introdutório, mas poderia ser expandido com:

* Paginação completa da API do GitHub
* Filtros por tipo de evento (ex: apenas PushEvents)
* Argumentos mais avançados usando `argparse`
* Cache persistente em arquivo
* Testes automatizados
* Transformação em pacote instalável (`pip install`)
* Melhor tratamento de rate limit da API

Essas melhorias foram deixadas de fora propositalmente para manter o foco educacional do projeto.

---

## 📚 Referências

* GitHub REST API Documentation
* roadmap.sh — Python Roadmap

---
