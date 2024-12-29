import sys
import json
from datetime import datetime

TASKS_FILE = "tasks.json"
MARK_IN_PROGRESS = "in-progress"
MARK_DONE = "done"
MARK_TODO = "todo"


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        show_help("main")
        return

    command = args[0]
    argument = args[1] if len(args) > 1 else None

    tasks = load_tasks()

    if not tasks and command != "add":
        print("Nenhuma tarefa encontrada. Você deve adicionar uma tarefa primeiro.")
        show_help("add")
        return

    commands = {
        "add": lambda: add_task(argument),
        "delete": lambda: handle_task(delete_task, command, argument),
        "update": lambda: handle_task(
            update_task, command, argument, args[2] if len(args) > 2 else None
        ),
        "mark-in-progress": lambda: handle_task(mark_status, command, argument),
        "mark-done": lambda: handle_task(mark_status, command, argument),
        "mark-todo": lambda: handle_task(mark_status, command, argument),
        "list": lambda: list_task(argument),
    }

    if command in commands:
        commands[command]()
    else:
        print(f"Comando não reconhecido: {command}.")
        show_help("main")


def show_help(command):
    help_messages = {
        "main": """
Comandos disponíveis:
- add [descrição]: Adiciona uma nova tarefa.
- delete [ID]: Remove uma tarefa pelo ID.
- update [ID] [nova descrição]: Atualiza a descrição de uma tarefa.
- list [status]: Lista as tarefas (status: todo, in-progress, done).
- mark-in-progress [ID]: Marca uma tarefa como "in-progress".
- mark-done [ID]: Marca uma tarefa como "done".
- mark-todo [ID]: Marca uma tarefa como "todo".
""",
        "add": "Use 'add [descrição]' para adicionar uma nova tarefa.",
        "delete": "Use 'delete [ID]' para remover uma tarefa pelo ID.",
        "update": "Use 'update [ID] [nova descrição]' para atualizar uma tarefa.",
        "list": "Use 'list [todo | in-progress | done]' para filtrar tarefas por status.",
        "mark-in-progress": "Use 'mark-in-progress [ID]' para marcar uma tarefa como 'in-progress'.",
        "mark-done": "Use 'mark-done [ID]' para marcar uma tarefa como 'done'.",
        "mark-todo": "Use 'mark-todo [ID]' para marcar uma tarefa como 'todo'.",
    }

    print(help_messages.get(command, "Erro: Comando não reconhecido."))


def list_task(status_filter=None):
    if status_filter not in [None, "todo", "in-progress", "done"]:
        print(f"Erro: Status '{status_filter}' inválido.")
        show_help("list")
        return

    tasks = load_tasks()
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return

    if status_filter:
        filtered_tasks = [task for task in tasks if task["status"] == status_filter]
        if not filtered_tasks:
            print(f"Nenhuma tarefa encontrada com o status '{status_filter}'.")
            return
        tasks = filtered_tasks

    for task in tasks:
        print(
            f"ID: {task['id']} | Descrição: {task['description']} | Status: {task['status']} | Criada em: {task['createdAt']} | Última alteração: {task['updatedAt']}"
        )


def handle_task(func, command, *args):
    if not args or not args[0]:
        print(f"Erro: Nenhum argumento fornecido para o comando '{command}'.")
        show_help(command)
        return

    if not args[0].isdigit():
        print(f"Erro: O ID fornecido '{args[0]}' não é válido.")
        show_help(command)
        return

    index = int(args[0])

    try:
        if len(args) > 1:  # update
            func(index, args[1])
        elif command == "delete":
            func(index)  # delete
        else:
            func(index, command)  # status
    except IndexError:
        print("Erro: Argumentos insuficientes fornecidos para o comando.")
        show_help(command)
    except Exception as e:
        print(f"Erro inesperado: {e}")


def mark_status(task_id, command_type):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            if command_type == "mark-in-progress":
                task["status"] = MARK_IN_PROGRESS
            elif command_type == "mark-done":
                task["status"] = MARK_DONE
            elif command_type == "mark-todo":
                task["status"] = MARK_TODO
            else:
                print(f"Erro: Comando de status '{command_type}' não é válido.")
                show_help(command_type)
                return
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(
                f"Tarefa '{task['description']}' alterada para o status '{task['status']}'."
            )
            return

    print("Erro: ID da tarefa não encontrado.")
    show_help(command_type)


def update_task(task_id, new_description):
    if not new_description:
        print("Erro: Nenhuma nova descrição foi fornecida para a tarefa.")
        show_help("update")
        return

    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            old_description = task["description"]
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(
                f"Tarefa {task_id} atualizada de '{old_description}' para '{new_description}'."
            )
            return

    print("Erro: ID da tarefa não encontrado.")
    show_help("update")


def delete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Tarefa ID {task_id} removida com sucesso.")
            return

    print("Erro: ID da tarefa não encontrado.")
    show_help("delete")


def add_task(description):
    if not description:
        print("Erro: Nenhuma descrição fornecida para a tarefa.")
        show_help("add")
        return

    task = {
        "id": generate_task_id(),
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(f"Tarefa adicionada com sucesso: {description} (ID: {task['id']})")


def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Erro: O arquivo de tarefas está corrompido. Criando um novo arquivo...")
        save_tasks([])
        return []


def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        print(f"Erro ao salvar tarefas: {e}")


def generate_task_id():
    tasks = load_tasks()
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


if __name__ == "__main__":
    main()
