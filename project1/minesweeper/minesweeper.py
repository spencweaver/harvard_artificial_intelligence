import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=16):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # return the cells that are mines
        if self.count == len(self.cells):
            return self.cells

        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # return the cells that have zero mines
        if self.count == 0 and len(self.cells) != 0:
            return self.cells

        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # remove mine from set by creating a new set and minus 1 from count
        new_set = set()
        for c in self.cells:
            if c != cell:
                new_set.add(c)
            else:
                self.count -= 1
        self.cells = new_set

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    # method to find all surrounding cells that are valid moves
    def get_neighbors(self, cell, count):
        neighbors_list = []

        # loop over all the surrounding cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Append the cell to the neighbors list
                if 0 <= i < self.height and 0 <= j < self.width \
                        and (i, j) not in self.safes \
                        and (i, j) not in self.mines \
                        and (i, j) not in self.moves_made:
                    neighbor_cell = (i, j)
                    neighbors_list.append(neighbor_cell)

                # reduce count if already known to be a mine
                if (i, j) in self.mines:
                    count -= 1

        return neighbors_list, count

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # step 1
        # add move to ai knowledge
        self.moves_made.add(cell)

        # step 2
        # mark safe in ai knowledge
        self.mark_safe(cell)

        # step 3
        # add the surrounding cells with mine count
        neighbors, count = self.get_neighbors(cell, count)
        knowledge = Sentence(neighbors, count)
        self.knowledge.append(knowledge)

        # step 4
        # Find all mines for all sentences
        for sentence in self.knowledge:
            if sentence.known_mines():
                for mine in sentence.known_mines():
                    self.mines.add(mine)
                    for s in self.knowledge:
                        s.mark_mine(mine)

        # step 5
            # Remove all safe cells if the count is greater than 0
            if sentence.known_safes():
                for safe in sentence.known_safes():
                    for s in self.knowledge:
                        if s.count > 0 and safe in s.cells:
                            s.mark_safe(safe)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # search through sentences until a safe move is found
        for sentence in self.knowledge.copy():
            if sentence.known_safes() is None:
                continue

            # remove empty sentences
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
                continue

            # if safemoves return one
            if sentence.known_safes() is not None:
                cell = sentence.cells.pop()
                return cell

        # return none if no safe moves known
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Check if game is over by summing known mines and moves_made
        if len(self.moves_made) + len(self.mines) == self.height * self.width:
            return None

        # search for random moves that have not been made, return when found
        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)

            # make sure it is still a decent and valid move
            if (i, j) not in self.moves_made \
                    and (i, j) not in self.mines:
                return (i, j)
