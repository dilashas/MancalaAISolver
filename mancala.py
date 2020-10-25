import cs210_utils
from utils import Struct
from games import Game

class MancalaGame(Game):
    Player1 = 0
    Player2 = 1

    #Player1's Mancala is on the 7th pit (Index 6)
    Player1_Mancala = 6

    #Player2's Mancala is on the 14th pit (Index 13)
    Player2_Mancala = 13

    #Player1's left-most pit is at index 0
    Player1_Start = 0

    #Player2's left-most pit is at index 7
    Player2_Start = 7

    #Initial umber of stone in each pit except the two Mancalas
    stones = 4

    def __init__(self):

        #Create 14 elements in a list representing pits in a Mancala layout
        self.board = [self.stones] * 14

        #Setting both Mancalas empty initially
        self.board[self.Player1_Mancala] = 0
        self.board[self.Player2_Mancala] = 0

        #Create 6 possible moves
        self.moves = [0, 1, 2, 3, 4, 5]
        self.start = Struct(to_move = self.Player1, utility = 0, board = self.board, moves = self.moves)

    def legal_moves(self, state):
        """Return a list of the allowable moves at this point.
        A state represents the number of stones in each pit on the board.
        """

        #Everything is legal as long as we have 1 stone in the pit
        return state.moves

    def make_move(self, move, state):
        #Base case
        if move not in state.moves:
            return state

        #Make tuple mutable
        board = state.board.copy()
        to_move = self.to_move(state)

        #Figure out whose move it is
        if to_move == self.Player1:
            Player_Start = self.Player1_Start
            Player_Mancala = self.Player1_Mancala
        else:
            Player_Start = self.Player2_Start
            Player_Mancala = self.Player2_Mancala

        #Figure out the state and how many stones to move
        nextPosition = Player_Start + move
        numberOfMoves = board[nextPosition]

        #Make the initiated move
        board[nextPosition] = 0
        while numberOfMoves > 0:
            #Skip opponent's Mancala
            if nextPosition > 12:
                nextPosition = 0
            else:
                nextPosition += 1

            #If stone lands on Player2's mancala
            if nextPosition == 13 and to_move == self.Player1:
                nextPosition = 0

            #If stone lands on Player1's mancala
            elif nextPosition == 6 and to_move == self.Player2:
                nextPosition += 1

            board[nextPosition] += 1

            #Number of moves decreases each time
            numberOfMoves -= 1

        # If the last stone dropped is in an empty pocket on a player's side, then
        # capture that piece and any pieces in the pocket directly opposite to it
        if nextPosition != 13 and nextPosition != 6:
            #nextPosition//7 => Opposite pit
            if board[nextPosition] == 1 and nextPosition//7 == to_move and board[12 - nextPosition] != 0:
                board[Player_Mancala] += board[nextPosition]
                board[Player_Mancala] += board[12 - nextPosition]
                board[nextPosition] = 0
                board[12 - nextPosition] = 0
            to_move = 1 - to_move

        #Implement the new state
        moves = []
        utility = 0
        if to_move == self.Player1:
            Player1_side = range(self.Player1_Start, self.Player1_Mancala + 1)
            for i in Player1_side:
                if board[i] != 0:
                    moves.append(i)
                    utility = board[self.Player1_Mancala]
        else:
            Player2_side = range(self.Player2_Start, self.Player2_Mancala)
            for i in Player2_side:
                if board[i] != 0:
                    moves.append(i - 7)
            utility = board[self.Player2_Mancala]
        return Struct(to_move = to_move, utility = utility, board = board, moves = moves)

    def utility(self, state, player):
        '''Return the value of this final state to player.
        # >>> g = MancalaGame() # doctest: +SKIP
        # >>> g.utility(g.state, g.player) # doctest: +SKIP
        # 1
        '''
        value = 0
        if player == self.Player1:
            Player1_side = range(self.Player1_Start, self.Player1_Mancala + 1)
            for i in Player1_side:
                value += state.board[i]
        elif player == self.Player2:
            Player2_side = range(self.Player2_Start, self.Player2_Mancala + 1)
            for i in Player2_side:
                value += state.board[i]
        return value

    def terminal_test(self, state):
        """Return True if this is a final state for the game.
        # >>> g = MancalaGame() # doctest: +SKIP
        # >>> g.terminal_test(g.state) # doctest: +SKIP
        # False
        """
        finalState = True

        #It is the final state of the game if either side of the pits
        #is entirely empty
        if state.to_move == self.Player1:
            Player2_side = range(self.Player2_Start, self.Player2_Mancala);
            for i in Player2_side:
                if state.board[i] != 0:
                    finalState = False
                    break
        else:
            Player1_side = range(self.Player1_Start, self.Player1_Mancala);
            for i in Player1_side:
                if state.board[i] != 0:
                    finalState = False
                    break
        return state.moves == [] or finalState

    def to_move(self, state):
        """Return the player whose move it is in this state.
        # >>> g = MancalaGame() # doctest: +SKIP
        # >>> g.to_move(g.state) # doctest: +SKIP
        # 0
        """
        return state.to_move

    def max_to_move(self, state):
        "Return True if the player whose move it is in this state is the first player to move."
        return self.Player1_Mancala


    def display(self, state):
        """Print or otherwise display the state.
        # >>> g = MancalaGame() # doctest: +SKIP
        # >>> g.display(g.state) # doctest: +SKIP
        #   [4, 4, 4, 4, 4, 4]
        # 0                    0
        #   [4, 4, 4, 4, 4, 4]
          """
        board = state.board
        Player1_side = range(self.Player1_Start, self.Player1_Mancala + 1)

        #Print the board horizonatally and have MAX be the player for the bottom row of pits
        for i in Player1_side:
            if i == 0:
                print(" ", board[13])
                print(board[i], " - ", board[12 - i])

            #Player1's Mancala
            elif i == 6:
                print(" ", board[i])

            else:
                print(board[i], " - ", board[12 - i])

        print(" ")

    def evaluation(self, state):
        """This function takes a game and a state and returns a value for that state.
        Because this function is going to be used in minimax search, we want to have positive
        values for states that are good for the maximizing player and negative values for states
        that are good for the minimizer, regardless of who's move it is in the game."""

        Player1_Utility = 0
        Player2_Utility = 0

        for i in range(0,7):
            Player1_Utility = Player1_Utility + state.board[i]

        for i in range(7,14):
            Player2_Utility = Player2_Utility + state.board[i]

        return Player1_Utility - Player2_Utility

    if __name__ == '__main__':
        cs210_utils.cs210_mainstartup()

