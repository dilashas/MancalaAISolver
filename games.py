##############################################################################
#
# File:         games.py
# Date:         Thu  6 Oct 2011  15:37
# Author:       Ken Basye
# Description: Game search and game support (borrowed heavily from AIMA Python
# package)
#
##############################################################################


"""
Games, or Adversarial Search

"""
import random
import cs210_utils
from utils import Struct, infinity, argmax

# ______________________________________________________________________________
# Minimax Search
def no_print(x, y=None, z=None, a=None, b=None, c=None):
    pass


def minimax_value(game, state):
    """Given a state in a game, calculate the value of the state by searching
    forward all the way to the terminal states"""

    if game.terminal_test(state):
        if game.max_to_move(state):
            return game.utility(state, game.to_move(state))
        else:
            return -game.utility(state, game.to_move(state))

    elif game.max_to_move(state):
        max_score = -999
        max_action = None
        for (action, child) in game.successors(state):
            score = minimax_value(game, child)
            if score > max_score:
                max_score = score
        return max_score
    else:
        min_score = 999
        for (action, child) in game.successors(state):
            score = minimax_value(game, child)
            if score < min_score:
                min_score = score
        return min_score


def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states
    """

    options = game.successors(state)
    best_pair = options[0];
    best_action, best_child = options[0]
    best_score = minimax_value(game, best_child)
    for pair in options[1:]:
        action, child = pair
        score = minimax_value(game, child)
        if game.max_to_move(state) and score > best_score:
            best_pair = pair
            best_score = score
        elif (not game.max_to_move(state)) and score < best_score:
            best_pair = pair
            best_score = score

    best_action, best_child = best_pair
    return best_action


def alpha_beta_full_value(game, state, alpha, beta, depth=0):
    """game is a Game, state is a state to search forward from, alpha and beta
    are cutoffs.  Returns the value of the state to the player whose turn it is"""
    if game.terminal_test(state):
        if game.max_to_move(state):
            return game.utility(state, game.to_move(state))
        else:
            return -game.utility(state, game.to_move(state))
    elif game.max_to_move(state):
        for action_child_state_pair in game.successors(state):
            action, child = action_child_state_pair
            score = alpha_beta_full_value(game, child, alpha, beta, depth + 1)
            if depth == 1 or depth == 2 or depth == 0:
                no_print("AB depth: ", depth, "with state: ", state, "score: ", score)
            if score >= beta:  # beta pruning
                no_print("Beta pruning with score: ", score, "Beta: ", beta)
                return score
            if score > alpha:
                alpha = score
        return alpha
    else:
        for (action, child) in game.successors(state):
            score = alpha_beta_full_value(game, child, alpha, beta, depth + 1)
            if score <= alpha:  # alpha pruning
                no_print("Alpha pruning with score: ", score, "Alpha: ", alpha)
                return score
            if score < beta:
                beta = score
        return beta


def alphabeta_full_search(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states using alpha-beta pruning"""

    options = game.successors(state)
    best_pair = options[0];
    best_action, best_child = options[0]
    best_score = alpha_beta_full_value(game, best_child, -999, 999)
    for pair in options[1:]:
        action, child = pair
        score = alpha_beta_full_value(game, child, -999, 999)
        if game.max_to_move(state) and score > best_score:
            best_pair = pair
            best_score = score
        elif (not game.max_to_move(state)) and score < best_score:
            best_pair = pair
            best_score = score

    best_action, best_child = best_pair
    return best_action


def alpha_beta_value(game, state, alpha, beta, cutoff_test, eval_fn, depth=0):
    """game is a Game, state is a state to search forward from, alpha and beta
    are cutoffs.  cutoff_test is a boolean function of state and depth. eval_fn
    is a function of game and state returning the value of state to the player
    who's turn it is Returns the value of the state to the player whose turn it
    is"""
    if cutoff_test(state, depth):
        no_print("Cutoff at depth: ", depth, "with state: ", state, "score: ", game.evaluation(state))
        return game.evaluation(state)
    if game.terminal_test(state):
        if game.max_to_move(state):
            return game.utility(state, game.to_move(state))
        else:
            return -game.utility(state, game.to_move(state))
    elif game.max_to_move(state):
        for action_child_state_pair in game.successors(state):
            action, child = action_child_state_pair
            score = alpha_beta_value(game, child, alpha, beta, cutoff_test, eval_fn, depth + 1)
            if depth == 1 or depth == 2:
                no_print("AB depth: ", depth, "with state: ", state, "score: ", score)
            if score >= beta:  # beta pruning
                no_print("Beta pruning with score: ", score, "Beta: ", beta)
                return score
            if score > alpha:
                alpha = score
        return alpha
    else:
        for (action, child) in game.successors(state):
            score = alpha_beta_value(game, child, alpha, beta, cutoff_test, eval_fn, depth + 1)
            if score <= alpha:  # alpha pruning
                no_print("Alpha pruning with score: ", score, "Alpha: ", alpha)
                return score
            if score < beta:
                beta = score
        return beta


def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (
        lambda game, state: (1 if game.max_to_move(state) else -1) * game.utility(state, game.to_move(state)))
    best_score_max = -infinity
    best_score_min = infinity
    best_action = None
    for a in game.legal_moves(state):
        child = game.make_move(a, state)
        score = alpha_beta_value(game, child, -999, 999, cutoff_test, eval_fn)
        if game.max_to_move(state) and score > best_score_max:
            best_action = a
            best_score_max = score
        elif (not game.max_to_move(state)) and score < best_score_min:
            best_action = a
            best_score_min = score
    no_print("AB search returning action: ", best_action, "with scores: ", best_score_min, best_score_max)
    return best_action


def alphabeta_search2(state, game, d=4, cutoff_test=None, eval_fn=None):
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda game, state: game.utility(state, player))
    options = game.successors(state)
    best_pair = options[0];
    best_action, best_child = options[0]
    best_score = alpha_beta_value(game, best_child, cutoff_test, eval_fn, -999, 999)
    for pair in options[1:]:
        action, child = pair
        score = alpha_beta_value(game, child, cutoff_test, eval_fn, -999, 999)
        if game.max_to_move(state) and score > best_score:
            best_pair = pair
            best_score = score
        elif (not game.max_to_move(state)) and score < best_score:
            best_pair = pair
            best_score = score

    best_action, best_child = best_pair
    return best_action


# ______________________________________________________________________________
# Players for Games

def query_player(game, state, display=True):
    "Make a move by querying standard input."
    if display: game.display(state)
    return num_or_str(input('Your move? '))


def query_player_py_exp(game, state, display=True):
    """
    Make a move by querying standard input. The input string is evaluated as a
    Python expression and returned
    """
    if display: game.display(state)
    return eval(input('Your move? '))


def random_player(game, state, display=True):
    "A player that chooses a legal move at random."
    if display: game.display(state); print()
    return random.choice(game.legal_moves(state))


def minimax_player(game, state, display=True):
    if display: game.display(state); print()
    return minimax_decision(state, game)


def alphabeta_full_player(game, state, display=True):
    if display: game.display(state); print()
    return alphabeta_full_search(state, game)


def alphabeta_player(game, state, display=True):
    if display: game.display(state); print()
    return alphabeta_search(state, game)


def alphabeta_player2(game, state, eval_fn, d = 4, display=True):
    if display: game.display(state); print()
    return alphabeta_search(state, game, d, eval_fn=eval_fn)


def play_game(game, named_players):
    from games import play_game
    """Play an n-person, move-alternating game.
    game is a Game instance;
    named_players is a tuple of pairs (player_name, player_function)
    player_functions take a game and a state and return a move to make (see above)

    >>> g0 = TicTacToe()
    >>> quiet_af_player = lambda g, s: alphabeta_full_player(g, s, False)
    >>> players = (('X', quiet_af_player), ('O', quiet_af_player))
    >>> play_game(g0, players)
    Game over - last move was by player X
    XXO
    OOX
    XOX
    Player X has utility: 0
    Player O has utility: 0
    >>> quiet_ab_player = lambda g, s: alphabeta_player(g, s, display=False)
    >>> players = (('X', quiet_ab_player), ('O', quiet_ab_player))
    >>> play_game(g0, players)
    Game over - last move was by player X
    XXO
    OOX
    XOX
    Player X has utility: 0
    Player O has utility: 0
    """

    state = game.initial
    game_over = False
    while not game_over:
        for named_player in named_players:
            player_name, player_function = named_player
            move = player_function(game, state)
            state = game.make_move(move, state)
            if game.terminal_test(state):
                print
                print("Game over - last move was by player %s" % (player_name,))
                game.display(state)
                game_over = True
                break  # for loop

    # Announce results
    for named_player in named_players:
        player_name, player_function = named_player
        print("Player %s has utility: %s" % (player_name, game.utility(state, player_name)))


def play_game2(game, named_players):
    from mancala import MancalaGame
    """Play an n-person game where moves don't have to alternate.
    game is a Game instance;
    named_players is a tuple of pairs (player_name, player_function)
    player_functions take a game and a state and return a move to make (see above)

    >>> b0 = MancalaGame()
    >>> quiet_af_player = lambda g, s: alphabeta_full_player(g, s, False)
    >>> players = (('X', quiet_af_player), ('O', quiet_af_player))
    >>> play_game(b0, players)
    """

    state = game.start
    game_over = False
    # print(named_players)
    while not game_over:
        for named_player in named_players:
            player_name, player_function = named_player
            # print(game.to_move(state))
            #Making it so that moves don't have to alternate
            #Using to_move() function to find out whose turn it is
            while game.to_move(state) == player_name:
                move = player_function(game, state)
                state = game.make_move(move, state)
                # print(game.to_move(state))
                if game.terminal_test(state):
                    # print
                    # print("Game over - last move was by player %s" % (player_name,))
                    # game.display(state)
                    game_over = True
                    break
            if game_over:
                break
    #Return a dict with player names as keys and final utilities as values
    outcomes = {}
    for named_player in named_players:
        player_name, player_function = named_player
        outcomes[player_name] = game.utility(state, player_name)
    return outcomes


# print("Player %s has utility: %s" % (player_name, game.utility(state, player_name)))



# ______________________________________________________________________________
# Some Sample Games

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement
    legal_moves, make_move, utility, and terminal_test. You may
    override display and successors or you can inherit their default
    methods. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        abstract

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        abstract

    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def max_to_move(self, state):
        "Return True if the player whose move it is in this state is the first player to move."
        abstract

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.__dict__.update(h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def max_to_move(self, state):
        "Return True if the player whose move it is in this state is the first player to move."
        return state.to_move == self.initial.to_move

    def make_move(self, move, state):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy();
        board[move] = state.to_move
        moves = list(state.moves);
        moves.remove(move)
        return Struct(to_move=('O' if state.to_move == 'X' else 'X'),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        if player == 'X':
            return state.utility
        else:
            assert player == 'O'
            return -state.utility

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '_'), end="")
            print()

    def compute_utility(self, board, move, player):
        "If X wins with this move, return 1; if O return -1; else return 0."
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, deltas):
        delta_x, delta_y = deltas
        "Return true if there is a line through move on board for player."
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k


class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return [(x, y) for (x, y) in state.moves
                if y == 0 or (x, y - 1) in state.board]


if __name__ == '__main__':
    cs210_utils.cs210_mainstartup()