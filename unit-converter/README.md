# 🚀 Unit Converter (Flask)

Um conversor de unidades web intuitivo e funcional que permite realizar conversões de **Comprimento**, **Peso** e **Temperatura**. O projeto foca em boas práticas de desenvolvimento web, utilizando herança de templates e uma lógica de conversão centralizada.

## 📝 Desafio
O objetivo é desenvolver uma aplicação web para conversão de medidas, enfrentando os seguintes desafios técnicos:
* **Herança de HTML:** Utilizar o motor de templates Jinja2 para evitar a repetição de código (DRY), criando uma estrutura base única para todas as páginas.
* **Lógica de Conversão Escalável:** Implementar um sistema que não dependesse de centenas de fórmulas individuais, mas sim de uma "unidade base" para cálculos.
* **Tratamento de Exceções:** Validar entradas de formulário para evitar erros de servidor (500) e fornecer feedback amigável ao usuário em casos de valores negativos ou campos vazios.

## 💡 A Solução
A aplicação foi estruturada utilizando **Flask** para o backend e **Jinja2** para o frontend dinâmico.

### Destaques Técnicos:
* **Base Comum:** O arquivo `base.html` contém a lógica da Navbar ativa e o esqueleto do formulário, que é estendido pelos outros templates.
* **Algoritmo de Conversão:** Para **Comprimento e Peso**, o sistema converte o valor de entrada para uma unidade base (metros ou gramas) e, em seguida, converte para a unidade final.
    * Para **Temperatura**, utiliza-se o Celsius como ponte para as conversões entre Fahrenheit e Kelvin.
* **Validação:** Utilização blocos `try/except` para capturar erros de valor (`ValueError`) e chaves inválidas (`KeyError`), retornando mensagens específicas para cada erro.



## 🛠️ Tecnologias Utilizadas
* **Python 3.x**: Linguagem de programação.
* **Flask**: Micro-framework para desenvolvimento web.
* **Jinja2**: Templates de herança e lógica no HTML.
* **CSS3**: Estilização.
* **Python Virtual env**: Ambiente virtual.

## ⚙️ Como instalar e iniciar o projeto

Siga os passos abaixo para configurar o ambiente e rodar o conversor localmente:

### 1. Clonar o repositório
```bash
git clone https://github.com/SouzaSantosK/Python_Roadmap.git
cd unit-converter
```
### 2. Criar um ambiente virtual Python
```bash
# No Windows:
python -m venv venv
venv\Scripts\activate

# No Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install flask
```

### 4. Executar o programa
```bash
python main.py
```

### 5. Acessar no navegador
Com o servidor rodando, acesse:
```bash
http://127.0.0.1:5000/length
```