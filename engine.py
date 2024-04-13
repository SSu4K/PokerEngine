from enum import Enum
from pokerkit import *
from player import Player
from move import *


class PokerConfig:
    def __init__(self, ante, small_blind, big_blind, player_count):
        self.ante = ante
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.player_count = player_count


class GamePhase(Enum):
    POSTING_ANTE = "POSTING_ANTES"
    COLLECTING_BET = "COLLECTING_BETS"
    POSTING_BLIND = "POSTING_BLIND"
    BURNING_CARD = "BURNING_CARD"
    DEALING_HOLE = "DEALING_HOLE"
    DEALING_BOARD = "DEALING_BOARD"
    KILLING_HAND = "KILLING_HAND"
    PUSHING_CHIPS = "PUSHING_CHIPS"
    PULLING_CHIPS = "PULLING_CHIPS"
    WAITING_MOVE = "WAITING_MOVE"


class PokerEngine:
    def __init__(self):
        self.running = False
        self.config = PokerConfig(500, 1000, 2000, 3)
        self.players = []
        self.game_phase = None

        self.poker_state = NoLimitTexasHoldem.create_state(
            # Automations
            (
            ),
            True,  # Uniform antes?
            self.config.ante,
            (self.config.small_blind, self.config.big_blind),
            self.config.big_blind,  # Min bet
            (1125600, 2000000, 553500),  # Starting stacks
            self.config.player_count,  # Number of players
        )

    def set_config(self, config):
        self.config = config

    def add_player(self, player):
        if (self.running == True):
            return
        if (len(self.players) < self.config.player_count):
            self.players.append(player)

    def remove_player(self, index):
        if (self.running == True):
            return
        self.players.remove(index)

    def reset(self):

        stacks = (player.money for player in self.players)

        self.poker_state = NoLimitTexasHoldem.create_state(
            # Automations
            (
            ),
            True,  # Uniform antes?
            self.config.ante,
            (self.config.small_blind, self.config.big_blind),
            self.config.big_blind,  # Min bet
            stacks,  # Starting stacks
            self.config.player_count,  # Number of players
        )

    def get_whose_turn(self):
        return self.poker_state.actor_index

    def update_money(self):
        for [player, stack] in zip(self.players, self.poker_state.stacks):
            player.money = stack

    def make_move(self, move):
        if (move.type == MoveType.CALL or move.type == MoveType.CHECK):
            self.poker_state.check_or_call()
        elif (move.type == MoveType.FOLD):
            self.poker_state.fold()
        elif (move.type == MoveType.BET or move.type == MoveType.RAISE):
            self.poker_state.complete_bet_or_raise_to(move.value)

    def game_step(self, move=None):

        if (self.poker_state.status):
            self.running = True
        else:
            self.running = False
            return

        if self.poker_state.can_post_ante():
            self.game_phase = GamePhase.POSTING_ANTE
            self.poker_state.post_ante()

        elif self.poker_state.can_collect_bets():
            self.game_phase = GamePhase.COLLECTING_BET
            self.poker_state.collect_bets()
            self.update_money()

        elif self.poker_state.can_post_blind_or_straddle():
            self.game_phase = GamePhase.POSTING_BLIND
            self.poker_state.post_blind_or_straddle()

        elif self.poker_state.can_burn_card():
            self.game_phase = GamePhase.BURNING_CARD
            self.poker_state.burn_card('??')

        elif self.poker_state.can_deal_hole():
            self.game_phase = GamePhase.DEALING_HOLE
            self.poker_state.deal_hole()

        elif self.poker_state.can_deal_board():
            self.game_phase = GamePhase.DEALING_BOARD
            self.poker_state.deal_board()

        elif self.poker_state.can_kill_hand():
            self.game_phase = GamePhase.KILLING_HAND
            self.poker_state.kill_hand()

        elif self.poker_state.can_push_chips():
            self.game_phase = GamePhase.PUSHING_CHIPS
            self.poker_state.push_chips()

        elif self.poker_state.can_pull_chips():
            self.game_phase = GamePhase.PULLING_CHIPS
            self.poker_state.pull_chips()

        else:
            self.game_phase = GamePhase.WAITING_MOVE
            if (move != None):
                self.make_move(move)

    def get_game_state(self):
        return {
            "config": vars(self.config),
            "players": self.players,

            "phase": self.game_phase.value,
            "turn": self.poker_state.actor_index,

            "hands": self.poker_state.hole_cards,
            "board": self.poker_state.board_cards,

            "stacks": self.poker_state.stacks,
            "bets": self.poker_state.bets
        }
