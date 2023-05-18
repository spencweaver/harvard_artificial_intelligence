from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A's statement
    Implication(Not(And(AKnave, AKnight)), AKnave),
    # A cannot be both knave and knight
    Not(And(AKnave, AKnight)),
    # A must be knave or knight
    Or(AKnave, AKnight),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A's statement and implications
    Implication(Not(And(AKnave, BKnave)), AKnave),
    Implication(AKnave, BKnight),
    Implication(AKnight, And(AKnave, BKnave)),
    # A, B cannot be both knave and knight
    Not(And(AKnave, AKnight)),
    Not(And(BKnight, BKnave)),
    # A, B must be knave or knight
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A's statement
    Implication(Not(Or(And(AKnave, BKnave), And(AKnight, BKnight))), AKnave),
    # B's statement
    Implication(Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))), BKnave),
    # additional implications
    Implication(AKnight, BKnight),
    Implication(AKnave, BKnight),
    Implication(BKnight, AKnave),
    Implication(BKnave, AKnave),
    # A, B cannot be both knave and knight
    Not(And(AKnave, AKnight)),
    Not(And(BKnight, BKnave)),
    # A, B must be knave or knight
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A statement
    Implication(Or(AKnight, AKnave), AKnight),
    Implication(Not(Or(AKnight, AKnave)), AKnave),
    # B's statement
    Implication(BKnight, And(BKnave, AKnave)),
    Implication(Not(CKnave), BKnave),
    # C's statement
    Implication(Not(AKnight), CKnave),
    Implication(AKnight, CKnight),
    # A, B, C cannot be both knave and knight
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not((And(CKnight, CKnave))),
    # A, B, C all must be knave or knight
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnight, CKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
