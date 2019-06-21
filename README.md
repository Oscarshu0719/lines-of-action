# lines-of-action

## Introduction

**Lines Of Action (LOA)** is a strategy game for two players invented by *Claude Soucie*. The objective is to connect all of one's pieces into a single group.

### Rules

#### Goal

- Bring all of one's checkers together into a contiguous body so that they are connected vertically, horizontally or diagonally (8-connectivity). 
- If one's enemy only has one checker, then the player wins the game.

#### Movement

- Players alternate moves, with Black having the first move.
- Checkers move horizontally, vertically, or diagonally.
- A checker moves exactly as many spaces as there are checkers (both friendly and enemy) on the line in which it is moving.
- A checker may jump over friendly checkers, but not over an enemy checker.
- If a checker moves to an enemy checker, then remove the enemy checker, and move the checker to the space.
- If a player has some checker to move, then the player cannot abstain.
- If a player does not move a checker for one minute, then the player loses the game.

(From [Wikipedia](<https://en.wikipedia.org/wiki/Lines_of_Action>))

## Algorithm specification

**Monte Carlo Tree Search (MCTS)** is implemented in this project for the AI movement and let the user to play with the AI, instead of other human players. 

A the start, the AI takes about 10 seconds to decide the movement. As the decrease of the number of the chess, the AI takes less time to decide.

## Usage 

``` python
python main.py
```

## Requirements

- `Python3`
- `PyQt5`
- Details in `conf/requirements.txt`

## GUI

- Mainwindow.
  ![main_window](readme_img\main_window.PNG)
- Left-click the chess to highlight the legal movements.
  ![main_window](readme_img\highlight_grid.PNG)
- Right-click to quit.
  ![main_window](readme_img\right_click.PNG)

## License

MIT License.

