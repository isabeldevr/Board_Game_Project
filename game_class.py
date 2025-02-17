import time
from game2dboard import Board
import copy
import leaderboard

ROWS = 4
COLUMNS = 8
CELL_SIZE = 117
CELL_SPACING = 10
STONE_IMAGE_FILES = [f"{i}.png" for i in range(0, 48)]  # CHANGE?
FINAL_ROUND_SCORE = 0


class TreeNode:
    def __init__(self, player, score=0, move=None):
        self.player = player
        self.score = score
        self.move = move
        self.children = []

    def calculate_path_sum(self) -> int:
        """ Calculate the sum along the entire path using dfs transversal technique
        Input: None
        Output: int """
        if not self.children:
            return self.score

        # Recursive call for internal nodes
        return self.score + max(child.calculate_path_sum() for child in self.children)


class MancalaGame:

    def __init__(self):
        self.current_player = None
        self.board = Board(ROWS, COLUMNS)
        self.board.title = "Mancala"
        self.board.cell_size = CELL_SIZE
        self.board.cell_spacing = CELL_SPACING
        self.board.margin = 0
        self.board.background_image = "mancala_board.png"
        if not self.board.background_image:
            self.board.cell_color = "bisque"
        self.board.create_output(background_color="black", color="bisque", font_size=12)
        self.board.on_start = self.start
        self.board.on_key_press = self.keyboard_command
        self.board.on_mouse_click = self.mouse_click
        self.board_dictionary = {}
        self.board.cursor = "arrow"

    def start(self) -> None:
        """ Initializes the game.
        Input: None
        Output: None. Calls the draw_board method with the initial board """

        # Initialise the UI
        self.initialise_board_ui()

        # Initialising the player: human player goes first
        self.current_player = 2
        self.board.print(f"Let's play Mancala! \t Player {self.current_player}, goes first!")

        # Initialise the board dictionary
        self.board_dictionary = {
            "Row_1": [4, 4, 4, 4, 4, 4],
            "Row_2": [4, 4, 4, 4, 4, 4],
            "Player1_score": 0,
            "Player2_score": 0,
        }

    def initialise_board_ui(self):
        """ We initialise the state of the board's user interface
        Input: None
        Output: None """
        for row in range(1, 3):
            for col in range(1, 7):
                self.board[row][col] = 4

        # Set player's homes
        self.board[1][0] = "Player 1"
        self.board[2][0] = 0
        self.board[1][7] = 0
        self.board[2][7] = "Player 2, You"


    def keyboard_command(self, key) -> None:
        """ Handle quitting and re-start of game
        Input: key pressed
        Output: None. Calls the start or quit method """
        global FINAL_ROUND_SCORE
        try:
            if key == "q":
                self.board.close()
                FINAL_ROUND_SCORE = 0
            elif key == "r":
                self.board.clear()
                self.start()
                FINAL_ROUND_SCORE = 0
            elif key == "l":
                leaderboard.leaderboard_display(FINAL_ROUND_SCORE)
        except Exception as e:
            print(f"An error occurred: {e}")

    def draw_board(self) -> None:
        """Draws the board"""
        self.board.show()

    def turn(self) -> None:
        """ This method is the turn of the human player
        Input: None
        Output: None. Calls the ai_player method """
        if self.current_player == 1:
            self.board.cursor = None
            row, col = self.ai_player()
            self.board.print("Player 1 is thinking...")
            return self.mouse_click(1,row, col + 1)
        else:
            self.board.cursor = "arrow"

    def mouse_click(self, btn: int, row: int, col: int) -> None:
        """ Handles mouse clicks
        Input: btn, row clicked, col clicked
        Output: None. Calls the moving_stones method"""
        # detach the mouse click handler
        # we need to return None at this stage but keep running the game
        # proceed with code execution
        import threading
        def do(row, col):
            try:
                # Handle wrong turn clicks
                if self.current_player == 1:
                    time.sleep(5)
                    print("sleeping")
                    self.board.cursor = None
                    return self.moving_stones(row, col)

                # Check if the click is valid
                if self.board[row][col] == 0 or row != 2 or col in {0, 7} or row in {0, 3}:
                    self.board.print("Invalid move! Try again.")
                    return None

                # Call the moving_stones method
                self.board.print("")
                self.board.cursor = "arrow"
                return self.moving_stones(row, col)

            except Exception as e:
                print(f"An error occurred: {e}")
        run = threading.Thread(target=do, args=(row, col))
        run.start()
        return None

    def moving_stones(self, row: int, col: int) -> None:
        """ Moves stones around the board:
        Input: row of chosen cell, column  of chosen cell
        Output: None. Calls the board_update method """
        try:
            col -= 1
            start_row, start_col = row, col
            stones = self.board_dictionary[f"Row_{self.current_player}"][col]

            # Remove stones from pit
            self.board_dictionary[f"Row_{row}"][col] = 0

            while stones > 0:
                # Move to the next column
                col += 1

                # If we reached the end of the row
                if col >= len(self.board_dictionary[f"Row_{row}"]):
                    self.board_dictionary[f"Player{self.current_player}_score"] += 1
                    stones -= 1
                    row = 3 - row
                    col = -1
                    if stones == 0:
                        break

                # Update the count of stones in the current cell
                else:
                    self.board_dictionary[f"Row_{row}"][col] += 1
                    stones -= 1

            # Check if game over
            last_row, last_col = row, col
            end_game = self.check_game_over()

            # If game can continue
            if not end_game:
                self.stone_capture(start_row, start_col, last_row, last_col, self.board_dictionary)

                self.board_update(self.board_dictionary)
                return self.current_player_update(last_row, last_col)
            else:
                return self.board_update(self.board_dictionary)

        except Exception as e:
            print(f"An error occurred: {e}")

    def board_update(self, board_dictionary: dict) -> None:
        """ Updates the board
        Input: board_dictionary
        Output: None """
        for col in range(1, 7):
            self.board[1][COLUMNS - col - 1] = board_dictionary["Row_1"][col - 1]
            self.board[2][col] = board_dictionary["Row_2"][col - 1]
        self.board[1][7] = board_dictionary["Player2_score"]
        self.board[2][0] = board_dictionary["Player1_score"]


    def ai_player(self) -> (int, int):
        """ This method is the AI player
        Input: None
        Output: best move coordinates (row, col) """
        root = TreeNode(None)  # we create a root node
        return self.make_best_move(root, self.current_player, 2)

    def make_best_move(self, root, player_to_evaluate, depth) -> (int, int):
        """ This method makes the best move
        Input: player_to_evaluate, depth
        Output: best move (row, col) """
        if depth == 0:
            return None

        best_move = None
        best_score = float('-inf')
        possible_moves = self.possible_moves_by_player(player_to_evaluate)

        for move in possible_moves:
            # Create a new root for each possible CPU move
            move_root = TreeNode(player_to_evaluate)
            self.evaluate_move(move_root, player_to_evaluate, move, depth)

            # Calculate the sum along the entire path for each move
            total_score = move_root.calculate_path_sum()

            # Update best move if the current move leads to a higher total score
            if total_score > best_score:
                best_score = total_score
                best_move = move

        return best_move

    def possible_moves_by_player(self, player_to_evaluate) -> list:
        """ This method returns the possible moves by player
        Input: player_to_evaluate
        Output: list """
        values = []
        for col in range(6):
            values.append((player_to_evaluate, col))
        return values

    def evaluate_move(self, root, player_to_evaluate, move, depth) -> int:
        """ This method evaluates the move
        Input: move, depth of recursion
        Output: points obtained for the move"""

        dictionary_copy = copy.deepcopy(self.board_dictionary)
        points = 0
        stones = dictionary_copy[f"Row_{self.current_player}"][move[1]]

        # Remove stones from pit
        dictionary_copy[f"Row_{self.current_player}"][move[1]] = 0
        row = self.current_player
        col = move[1]

        while stones > 0:
            # Move to the next column
            col += 1

            # Check if we reached the end of the row
            if col >= len(dictionary_copy[f"Row_{row}"]):
                dictionary_copy[f"Player{self.current_player}_score"] += 1
                points += 1
                stones -= 1
                row = 3 - row
                col = -1
                if stones == 0:
                    break

            # Update the count of stones in the current cell
            else:
                dictionary_copy[f"Row_{row}"][col] += 1
                stones -= 1

        # Check if we capture stones
        last_row, last_col = row, col
        self.stone_capture(move[0], move[1], last_row, last_col, dictionary_copy)

        # Create nodes
        if player_to_evaluate == self.current_player:
            root.children.append(TreeNode(player_to_evaluate, points, move))
        else:
            root.children.append(TreeNode(player_to_evaluate, -points, move))

        # Check if recursion should continue
        if depth > 0:
            player_to_evaluate = 3 - self.current_player
            self.make_best_move(root.children[-1], player_to_evaluate, depth - 1)

        return points

    def stone_capture(self, start_row: int, start_col: int, last_row: int, last_col: int, dictionary: dict) -> None:
        """ Checks if we can capture stones by checking if we land in an empty pit on our side
        Input: starting row, starting column, last row, last column, dictionary
        Output: None """
        if start_row == last_row and start_col != last_col and dictionary[f"Row_{last_row}"][last_col] == 1:
            dictionary[f"Row_{last_row}"][last_col] += dictionary[f"Row_{3 - last_row}"][last_col]
        return None

    def current_player_update(self, last_row: int, last_col: int) -> None:
        """ Updates the current player based on the last move
        Input: last row, last column
        Output: None """
        if last_row == 2 and last_col == 6:
            self.current_player = 1
            self.board.print("Player 1 goes again!")
        elif last_row == 1 and last_col == 0:
            self.current_player = 2
            self.board.print("You can go again!")
            self.board.cursor = "arrow"
        else:
            self.current_player = 3 - self.current_player

        # Move the following line outside the if condition
        self.board.print("Player {}'s turn".format(self.current_player))

        # Check whose turn it is
        return self.turn()

    def check_game_over(self) -> bool:
        """ Checks if the game is over and if so declares a winner. First to finish is always the winner.
        Input: None
        Output: bool """
        global FINAL_ROUND_SCORE
        for row in range(1, 3):
            if (self.board_dictionary[f"Row_{row}"] == [0, 0, 0, 0, 0, 0] or self.board_dictionary[
                f"Row_{3 - row}"] == [0, 0, 0, 0, 0, 0]) and self.board_dictionary[f"Player{row}_score"] > \
                    self.board_dictionary[f"Player{3 - row}_score"]:
                FINAL_ROUND_SCORE = self.board_dictionary[f"Player{row}_score"]
                self.declare_winner(row)
                return True
        return False

    def declare_winner(self, player: int) -> None:
        """ This method declares the winner
        Input: first player to finish
        Output: bool """
        self.board_update(self.board_dictionary)
        self.board.cursor = None
        self.board.print(f"Player {player} wins! \n Press 'r' to restart, 'q' to quit or 'l' to see the leaderboard in the terminal.")
        return None

# SOME NOTES
# Añadir time complexities
# it would be cool to have an outro screen
# current player revise method (turns are a bit wonky, it's not easy to see who is playing I want to introduce a delay )
# Handle draws
# 6. We need to add the stone images to the board (so layer the stones instead of the numbers)
