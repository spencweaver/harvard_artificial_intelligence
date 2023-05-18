import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # loop through each variable and words in each variable
        # then check the length to make sure they match
        for variable, words in self.domains.items():
            for word in words.copy():
                if variable.length != len(word):
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # find all the overlaps for x and y
        overlap = self.crossword.overlaps[(x, y)]

        # find the set of x and y words then copy
        set_x = self.domains[x].copy()
        set_y = self.domains[y].copy()

        # count the number of deletions that took place
        del_c = 0
        for word in set_x:

            # count the amount of overlaps
            counter = 0
            for w in set_y:
                if word[overlap[0]] == w[overlap[1]]:
                    counter += 1

            # if no overlaps delete the word
            if counter == 0:
                self.domains[x].remove(word)
                del_c += 1

        # check for any deletions
        if del_c == 0:
            return False
        else:
            return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # load up the queue
        queue = []
        if arcs is None:
            for a, b in self.crossword.overlaps.items():
                if b is not None:
                    queue.append(a)
        else:
            queue = arcs

        while queue:
            # load x and y from the queue
            x, y = queue.pop()

            # check if revision took place
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False

                # find neighbors to add to the queue and remove y
                neighbors = self.crossword.neighbors(x)
                neighbors.remove(y)
                for z in neighbors:
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # if every variable is in the assignment dictionary return true
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # find all the overlaps
        # find the cartesian product of the assignment keys
        # and ignore the same keys
        # return false if an overlap does not match
        overlaps = self.crossword.overlaps
        for key, word in assignment.items():
            for k, w in assignment.items():
                if key != k and overlaps[(key, k)] is not None:
                    overlap = overlaps[(key, k)]
                    if word[overlap[0]] != w[overlap[1]]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # an attempt to order that breaks the code
        word_list = list(self.domains[var].copy())
        word_list = sorted(word_list)

        for w in assignment.values():
            if w in word_list and w != assignment[var]:
                word_list.remove(w)

        return word_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # find all the variables that are not assigned
        # then pop off one to analyze
        return (self.domains.keys() - assignment.keys()).pop()

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # return if every variable has an assignment
        if self.assignment_complete(assignment):
            return assignment

        # select the next variable
        var = self.select_unassigned_variable(assignment)

        # try every word in the variable domain
        # if consistent try the next variable
        # delete assignment key if not consistent
        for word in self.domains[var]:
            assignment[var] = word
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            else:
                del assignment[var]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
