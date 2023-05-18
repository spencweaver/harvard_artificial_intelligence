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
        for variable, words in self.domains.items():
            for word in words.copy():
                if variable.length != len(word):
                    self.domains[variable].remove(word)

        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """


        overlap = self.crossword.overlaps[(x, y)]
        print(overlap)

        set_x = self.domains[x].copy()
        set_y = self.domains[y].copy()

        # print(set_x, set_y)

        del_c = 0

        for word in set_x:
            print(word)
            counter = 0
            
            for w in set_y:
                if word[overlap[0]] == w[overlap[1]]:
                    print("equals")
                    counter += 1
            print(counter)
            if counter == 0:
                self.domains[x].remove(word)
                del_c += 1

        if del_c == 0:
            return False
        else:
            return True
                

        # raise NotImplementedError

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
            for a,b in self.crossword.overlaps.items():
                
                if b is not None:
                    queue.append(a)
                    # print(f"&&&&&&&&&&&&&&&&&&&&&-\nqueue {queue}\n&&&&&&&&&&&&&&&&&&&&&-")
        else:
            queue = arcs
        
        c = 0
        while queue:
            print(f"ccccccc {c}")
            c += 1
            x, y = queue.pop()

            # print(f"x, y lengths ::::::: {len(self.domains[x]), len(self.domains[y])}\n")
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    # print("false")
                    return False
                
                # print(f"x {x}")
                neighbors = self.crossword.neighbors(x)
                # print(f"neighbors of {x}:==> {neighbors}")    

                neighbors.remove(y)
                print(f"neighbors of after {x}:==> {neighbors}")    
                for z in neighbors:
                    queue.append((z,x))

        print("True")
        return True


        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False
        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        print("overlaps")
        overlaps = self.crossword.overlaps
        print(overlaps)

        for key in self.domains.keys():
            print(f"keyyyyy {key}")
            for k in overlaps.keys():
                print(k)
                if key in k:
                    print("yyyyyyyeeeeeessssss")
                    print(overlaps[k])

        # assignment_keys = set(assignment.keys())
        # print(type(assignment_keys))
        # print(assignment_keys)

        for key, word in assignment.items():

            for k, w in assignment.items():

                if key != k and overlaps[(key, k)] is not None:
                    
                    overlap = overlaps[(key, k)]
                    if word[overlap[0]] != w[overlap[1]]:

                        return False
                        

                print("key --> k")
                print(k)
        return True
        # import numpy as np
        # x = np.array([1,2,3])
        # y = np.array([4,5])
        # result = np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])
        # print(result)
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        print(f"x {x}")
        neighbors = self.crossword.neighbors(x)
        print(f"neighbors of {x}:==> {neighbors}")
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        return (self.domains.keys() - assignment.keys()).pop()

        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # print(f"variables {self.crossword.variables}")
        # print(f"number of variables {len(self.crossword.variables)}")
        # print(assignment)
        # print(len(assignment))
        # print(f"self.domains {self.domains}")
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        print(f"var {var}")

        # assignment[var] = .pop()
        
        for value in self.domains[var]:
            print(value)


        print(f"assignment {assignment}")
        print(len(assignment))


        for word in self.domains[var]:
            # print(word)
            assignment[var] = word
            if self.consistent(assignment):
                print("consistent")
                result = self.backtrack(assignment)
                if result:
                    return result
            else:
                del assignment[var]

        return None

        # for domain in self.domains:

        #     print(f"domain {domain}")
        #     print(f"self.domains[domain] {self.domains[domain]}")
        #     if len(self.domains[domain]) == 0:
        #         print("none")
        #         return None
        # assignment = {a: values.pop() for a, values in self.domains.items()}
        # return assignment

        # raise NotImplementedError


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
