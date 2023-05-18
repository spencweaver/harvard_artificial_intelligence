import nltk
# from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V | N VP | NP VP | NP VP Conj VP | NP VP Conj NP VP

AP -> Adj | Adj AP | Det AP
NP -> N | Det N | Det NP | AP NP | N PP | Adj N | Adj NP
PP -> P NP
VP -> V | V NP | V Adv | V PP | Adv V | VP NP | V PP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # tokenize the sentence
    # lowercase the sentence and remove punctuation
    sentence = wordpunct_tokenize(sentence)
    sentence = [word.lower() for word in sentence if word.isalpha()]
    return sentence


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # initialize a list for chunks
    # check every part of the tree
    # then look through subtrees
    chunk_list = []
    for t in tree:  
        if t.label() == "N":
            chunk_list.append(t)
        if t.label() == "NP":
            for s in t.subtrees():
                print(s)
                if s.label() == "N":
                    chunk_list.append(s)
    return chunk_list


if __name__ == "__main__":
    main()
