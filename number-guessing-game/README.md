# Number Guessing Game
Este é um jogo de adivinhação de números baseado em CLI (Interface de Linha de Comando), desenvolvido como parte do desafio do roadmap.sh.

## Objetivo
O computador escolhe um número entre 1 e 100, e você deve adivinhá-lo com base nas dicas e no nível de dificuldade escolhido.

## ✨ Funcionalidades
* Níveis de Dificuldade: Escolha entre Fácil (10 chances), Médio (5 chances) ou Difícil (3 chances).

* Dicas: O jogo informa se o número secreto é maior ou menor que o seu palpite.

* Sistema de High Score: O jogo armazena a pontuação (vitórias) por categoria de dificuldade durante a sessão.

* Múltiplas Rodadas: Opção de continuar jogando sem precisar reiniciar o programa.

#### Tecnologias Utilizadas:
* Python 3.11+
* Poetry (Gerenciamento de ambiente e dependências)

## 📦 Instalação e Execução
Para rodar este projeto localmente, você precisará ter o Poetry instalado.

1. Clonar o repositório
    ```bash
    git clone https://github.com/SouzaSantosK/Python_Roadmap.git
    cd number-guessing-game
    ```

2. Instalar dependências e ambiente
O Poetry criará um ambiente virtual isolado e instalará as configurações necessárias:

    ```Bash
    poetry install
    ```

3. Executar o jogo
Você pode rodar o script diretamente através do Poetry:

    ```bash
    poetry run python main.py
    ```
## 🕹️ Como Jogar
* Ao iniciar, escolha o nível de dificuldade digitando o número correspondente (1, 2 ou 3).

* Digite seu palpite quando solicitado.

* Siga as dicas de "maior" ou "menor" até acertar o número ou esgotar suas tentativas.

* Ao final, o jogo exibirá seu High Score atual e perguntará se deseja jogar novamente.

### 🛠️ Melhorias Futuras
* Persistência de High Scores em arquivo JSON.

* Adição de um cronômetro para medir o tempo de resposta.

* Sistema de "Dicas Quentes" (avisar se o palpite está muito perto do número real).