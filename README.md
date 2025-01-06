<h1 align="center">
  <br />
  <img
    src="src\img\Idle.png"
    alt="A Saga do Conhecimento - Batalha"
    width="150"
  />
  <br />
  <b>A Saga do Conhecimento - Batalha</b>
  <br />
  <sub
    ><sup><b>(PYGAME-QUIZ-GAME)</b></sup></sub
  >
  <br />
  
  
</h1>


A Pygame-based educational quiz game that combines learning with interactive battles.

This project is an engaging educational game designed to help students learn various subjects through a battle-style quiz format. Players select their grade level and subject, then face off against an enemy character by answering questions correctly.

Story Mode coming soon

## Key Features:

🧠 Educational Quizzes: Covers a variety of subjects (Math, Science, History, and more) and grade levels.

⚔️ Battle Mechanics: Answer correctly to attack, defend, or cast spells in turn-based battles.

🎨 Dynamic Visuals: Animated characters and a vibrant, pixel art aesthetic.

🎵 Immersive Audio: Background music and sound effects enhance the gaming experience.

📈 Player Progression: Gain points, unlock abilities, and explore new areas. (coming soon)




## 📂 Repository Structure


- `main.py`: The main entry point and game logic
- `questions.py`: Contains the question database for different subjects and grade levels

## 🚀 Getting Started


### Installation

1. Ensure you have Python 3.7+ installed
2. Install Pygame:
   ```
   pip install pygame
   ```
3. Clone the repository:
   ```
   git clone https://github.com/theezequiel42/saga-do-conhecimento-batalha.git
   cd saga-do-conhecimento-batalha

   ```

### Running the Game

To start the game, run:

```
python main.py
```

### 🎮 Gameplay

1. Select your grade level from the main menu
2. Choose the subjects you want to be quizzed on
3. Answer questions correctly to deal damage to the enemy
4. Manage your health and mana while battling
5. Defeat the enemy by reducing their health to zero

<br />
  <img
    src="src\img\gameplay.png"
    alt="Gameplay"
    width="1000"
  />
  <br />

<br />
  <img
    src="src\img\gameplay2.png"
    alt="Gameplay"
    width="1000"
  />
  <br />

### 🛠️ Configuration


The game's configuration, including screen size, colors, and music files, can be adjusted in the `main.py` file.

To add or modify questions, edit the `questions.py` file. Questions are organized by grade level and subject.

## Data Flow

1. The game starts in `main.py`, initializing Pygame and loading assets
2. Players select their grade level and subjects
3. Questions are fetched from `questions.py` based on the player's selections
4. The battle screen is displayed, showing the player and enemy characters
5. Questions are presented to the player with a timer
6. Player's answers affect the health and mana of both characters
7. The game continues until either the player or enemy is defeated
8. Results are displayed, and the player can choose to play again or exit

```
[Player Input] -> [Game State] -> [Question Selection] -> [Battle Logic] -> [Character Animation] -> [Screen Update]
     ^                                                         |
     |                                                         v
[Score Calculation] <- [Answer Validation] <- [Timer Management]
```

## 🛡️ Infrastructure

The project primarily consists of Python scripts and does not have a dedicated infrastructure stack. However, it does utilize the following key components:

- Pygame: For rendering graphics, handling input, and playing audio
- Python's built-in `random` module: For randomizing question selection
- `asyncio`: For handling asynchronous operations



# Jogo de Quiz Educacional: A Saga do Conhecimento - Batalha

Um jogo de quiz educacional baseado em Pygame que combina aprendizado com batalhas interativas.

Este projeto é um jogo educacional envolvente projetado para ajudar os alunos a aprender vários assuntos por meio de um formato de quiz estilo batalha. Os jogadores selecionam seu nível de escolaridade e assunto, então enfrentam um personagem inimigo respondendo às perguntas corretamente.

O jogo apresenta:
- Vários assuntos e níveis de ensino
- Sistema de batalha interativo
- Personagens animados
- Barras dinâmicas de saúde e mana
- Perguntas cronometradas
- Música de fundo e efeitos sonoros

## Estrutura do repositório

- `main.py`: O principal ponto de entrada e lógica do jogo
- `questions.py`: Contém o banco de dados de perguntas para diferentes assuntos e níveis de ensino

## Instruções de uso

### Instalação

1. Certifique-se de ter o Python 3.7+ instalado
2. Instale o Pygame:
```
pip install pygame
```
3. Clone o repositório:
```
git clone https://github.com/theezequiel42/saga-do-conhecimento-batalha.git
cd saga-do-conhecimento-batalha

```

### Executando o jogo

Para iniciar o jogo, execute:

```
python main.py
```

### Jogabilidade

1. Selecione seu nível de ensino no menu principal
2. Escolha os assuntos sobre os quais deseja ser questionado
3. Resposta perguntas corretamente para causar dano ao inimigo
4. Gerencie sua saúde e mana durante a batalha
5. Derrote o inimigo reduzindo sua saúde a zero

### Configuração

A configuração do jogo, incluindo tamanho da tela, cores e arquivos de música, pode ser ajustada no arquivo `main.py`.

Para adicionar ou modificar perguntas, edite o arquivo `questions.py`. As perguntas são organizadas por nível de ensino e assunto.

## Fluxo de dados

1. O jogo começa em `main.py`, inicializando o Pygame e carregando ativos
2. Os jogadores selecionam seu nível de escolaridade e disciplinas
3. As perguntas são obtidas de `questions.py` com base nas seleções do jogador
4. A tela de batalha é exibida, mostrando os personagens do jogador e do inimigo
5. As perguntas são apresentadas ao jogador com um cronômetro
6. As respostas do jogador afetam a saúde e o mana de ambos os personagens
7. O jogo continua até que o jogador ou o inimigo seja derrotado
8. Os resultados são exibidos e o jogador pode escolher jogar novamente ou sair

```
[Entrada do jogador] -> [Estado do jogo] -> [Seleção de perguntas] -> [Lógica de batalha] -> [Animação do personagem] -> [Atualização da tela]
^                                                                              |
|                                                                              v
[Cálculo da pontuação] <- [Validação da resposta] <- [Gerenciamento do cronômetro]
```

## Infraestrutura

O projeto consiste principalmente em scripts Python e não tem uma pilha de infraestrutura dedicada. No entanto, ele utiliza os seguintes componentes principais:

- Pygame: para renderizar gráficos, manipular entradas e reproduzir áudio
- Módulo `random` integrado do Python: para randomizar a seleção de perguntas
- `asyncio`: para manipular operações assíncronas