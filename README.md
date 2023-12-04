# Mancala Game

## Rules of the Game

### Game Setup:

- Two rows with six pits each.
- Player 1 (top row, CPU Player) and Player 2 (bottom row, Human Player).
- Each player has a home (leftmost and rightmost pits) which keeps track of their points.
- The game starts out with 4 stones per pit.

### Objective:
- Capture more stones than your opponent.
- Game ends when all pits on one side are empty.

### Gameplay:

#### Starting the Game:

- Players take turns; 
- Player 2 (so the human player) starts.

#### Turn Mechanics:

- Select a pit, pick up its stones, and distribute counterclockwise. This is all simulated in one click.
- If the last stone lands in the player's home, they get another turn.

#### Capturing Stones:

- If the last stone lands in an empty pit on the player's side, and the opposite pit on the opponent's side has stones, capture all those stones.

#### End Game:

- Game ends when one player's pits are empty.
- Remaining stones on the opponent's side are captured.

#### Determining the Winner:

- Count seeds in the store; player with the most seeds wins.

## Key Data Structures:

### Matrices:

- Represent the game board; used to store the visual/image representation of the number of stones in each pit.
- Accessed and modified to visually simulate stone movement.

### Dictionary (board_update method):

- Serves to easily simulate the counterclockwise movement of mancala.
- Helps the visual board representation by translating board_dictionary to respective pits and scores in the matrix.
- Manages the logical state of the board independently of the visual interface.

### Tree (AI player)
- Dynamically created to evaluate each possible move
- Serves to visualise the possible upcoming moves
- This helps the AI evaluate what move would lead to the best outcome


## Key Algorithms:

### DFS sum
- Used to transverse the tree of possible moves 
- It adds the score by the human player (as a loss) and the ai (as a gain) to check what combination would be best. 
- The entire implementation of the AI player includes a depth parameter that can be adjusted to make the ai think more turns ahead.

### Merge sort
- Used to sort the leaderboard kept in leaderboard.txt
- This algorithm was chosen because of its time complexity characteristics reaching at worst 0(nlogn)
