# PokerEngine
A Texas Hold'em Poker enigine. Intended for future use in online poker game. Utilizes the pokerkit package.
The code enables runnung a full poker game and retrieving the *gamestate* at each step of the game.


### Example use:
```python
'''
test.py
Poker engine test program
'''

from engine import *

config = PokerConfig(500, 1000, 2000, 3)
players = [Player("Szymon", 10000), Player("Karol", 10000), Player("Jezy", 10000)]

engine = PokerEngine()
engine.set_config(config)

for player in players:
    engine.add_player(player)

engine.reset()
engine.game_step()

while(engine.running):
    if(engine.game_phase != GamePhase.WAITING_MOVE):
        engine.game_step()
    else:
        print(engine.get_game_state())
        print("Input move:")
        name = input()
        value = None
        if(name == MoveType.BET.value or name == MoveType.RAISE.value):
            print("Input value:")
            value = int(input())

        move = Move(MoveType(name), value)
        print(vars(move))
        engine.game_step(move)

    print(engine.get_game_state())
```
