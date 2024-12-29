# Task Tracker CLI

Task Tracker CLI é uma aplicação em Python que permite gerenciar tarefas diretamente pelo terminal. Com ele, você pode adicionar, listar, atualizar, remover e alterar o status das suas tarefas de forma simples e eficiente.

## Funcionalidades

- Adicionar tarefas com descrição personalizada.
- Listar tarefas com filtros por status (`todo`, `in-progress`, `done`).
- Atualizar a descrição de uma tarefa.
- Remover tarefas.
- Alterar o status de uma tarefa para:
  - **TODO** (pendente)
  - **IN-PROGRESS** (em andamento)
  - **DONE** (concluído)

---

## Tecnologias Utilizadas

- **Python 3.8+**
- Manipulação de arquivos JSON para persistência dos dados.
- Uso da biblioteca `sys` para leitura de argumentos da linha de comando.

---

## Como Usar

### Pré-requisitos

- Python 3.8 ou superior instalado em sua máquina.

### Como instalar apenas este projeto
Para clonar apenas o diretório deste projeto, você pode usar o comando **sparse checkout** do Git:

1. Clone o repositório principal sem o conteúdo completo:
   ```bash
   git clone --no-checkout https://github.com/SouzaSantosK/Python_Projects.git
   cd Python_Projects
   ```
2. Ative o sparse checkout:
   ```bash
   git sparse-checkout init --cone
   git sparse-checkout set Task_Tracker_Cli
   ```
3. Faça o checkout:
   ```bash
   git checkout
   ```
5. Por fim, certifique-se de que os arquivos do projeto, incluindo o `tasks.json` foram instalados no diretório. Caso `tasks.json` não exista, o programa criará automaticamente.


### Comandos Disponíveis

#### Adicionar uma Tarefa
Adicione uma nova tarefa com uma descrição personalizada.
```bash
python task_manager.py add "Descrição da tarefa"
```

#### Listar Tarefas
Liste todas as tarefas ou filtre por status.
```bash
python task_manager.py list
python task_manager.py list [todo|in-progress|done]
```
Exemplo:
```bash
python task_manager.py list
python task_manager.py list todo
```

#### Atualizar Tarefa
Atualize a descrição de uma tarefa existente.
```bash
python task_manager.py update <id> "Nova descrição"
```
Exemplo:
```bash
python task_manager.py update 2 "Enviar e-mail de follow-up com arquivo anexo"
```

#### Remover uma Tarefa
Remova uma tarefa pelo ID.
```bash
python task_manager.py delete <id>
```
Exemplo:
```bash
python task_manager.py delete 3
```

#### Alterar o Status de uma Tarefa
Altere o status de uma tarefa para:
- `mark-in-progress`
- `mark-done`
- `mark-todo`

```bash
python task_manager.py mark-in-progress <id>
python task_manager.py mark-done <id>
python task_manager.py mark-todo <id>
```
Exemplo:
```bash
python task_manager.py mark-done 1
```

### Exemplo de Arquivo `tasks.json`
O programa utiliza um arquivo JSON para armazenar as tarefas. Aqui está um exemplo:
```json
[
    {
        "id": 1,
        "description": "Finalizar o relatório semanal",
        "status": "todo",
        "createdAt": "2024-12-20T10:00:00",
        "updatedAt": "2024-12-20T10:00:00"
    },
    {
        "id": 2,
        "description": "Enviar e-mail de follow-up para o cliente",
        "status": "in-progress",
        "createdAt": "2024-12-21T11:00:00",
        "updatedAt": "2024-12-22T12:00:00"
    }
]
```
Se o arquivo `tasks.json` não existir, ele será criado automaticamente ao executar o programa.

### Tratamento de Erros
O programa oferece mensagens para erros comuns, como:
- Comando inválido.
- ID de tarefa inexistente.
- Falta de argumentos necessários para o comando.
- Arquivo `tasks.json` corrompido ou ausente.
