"""
Project 1
CS50's Introduction to Artificial Intelligence with Python
https://cs50.harvard.edu/ai/2023/

Attempted by
Daychyi Ku
https://github.com/Daychyi

AI can win if it is lucky enough to 
not choose the mined-cell in random move 
before all mines are found.
"""

import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

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
        if (len(self.cells) == self.count):
            return self.cells
        return None
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if (len(self.cells) == 0):
            return self.cells
        return None
        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
             self.cells.remove(cell)
             if self.count:
                self.count -= 1
             else:
                raise ValueError(f"{__class__.__name__}: Count cannot be zero with mines")
        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        # raise NotImplementedError


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

    def neighbour_cells(self, cell):
        """
        Returns the set of unlabelled cells that are neighbour of a given cell,
        not including the cell itself.
        """
        neighbour = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add cell to neigbour if not labelled as safe or mine
                if (i,j) not in self.mines or self.safes:
                    if 0<=i<8 and 0<=j<8:
                        neighbour.add((i, j))

        return neighbour
    
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
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # get unlabelled neighouring cells and add to knowledge as new Sentence
        neighbour = self.neighbour_cells(cell)
        self.knowledge.append(Sentence(neighbour,count))

        for sentence in self.knowledge:
            # print(f"sentence:{sentence}")
            
            if sentence.count == 0: #mark as safe
                safe_cells = copy.deepcopy(sentence.cells)
                self.knowledge.remove(sentence)
                for c in safe_cells:
                    self.mark_safe(c)
            elif len(sentence.cells)== sentence.count: #mark as mines
                mine_cells = copy.deepcopy(sentence.cells)
                self.knowledge.remove(sentence)
                for c in mine_cells:
                    self.mark_mine(c)
        
        # print(f"moves_made: {self.moves_made}")
        # print(f"safe: {self.safes}")
        # print(f"mine: {self.mines}")
        # raise NotImplementedError
    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None
        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        max_move = self.height*self.width - 8 #number of mines
        while len(self.moves_made) < max_move: 
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            move = (i,j)
            if move not in self.moves_made:
                if move not in self.mines:
                    # print(f"AI random move: {move}")
                    return move
        # raise NotImplementedError
