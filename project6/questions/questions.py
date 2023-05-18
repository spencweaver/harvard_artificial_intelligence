import nltk
import sys

import os
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import word_tokenize
from collections import Counter
from numpy import log as ln
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)
    while True:
        # Prompt user for query
        query = set(tokenize(input("Query: ")))

        # Determine top file matches according to TF-IDF
        filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

        # Extract sentences from top files
        sentences = dict()
        for filename in filenames:
            for passage in files[filename].split("\n"):
                for sentence in nltk.sent_tokenize(passage):
                    tokens = tokenize(sentence)
                    if tokens:
                        sentences[sentence] = tokens

        # Compute IDF values across sentences
        idfs = compute_idfs(sentences)

        # Determine top sentence matches
        matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
        for match in matches:
            print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    # initialize a dictionary for the files
    # find the files then loop through each file
    # read each file into memory and close
    content = {}
    files = os.listdir(directory)
    for file in files:
        path = os.path.join(directory, file)
        f = open(path)
        content[file] = f.read()
        f.close()
    return content


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # tokenize all the words in the document
    # lowercase all words and remove all punctuation and remove all stop words
    document = word_tokenize(document)
    document = [
        word.lower() for word in document if word.lower()
        not in string.punctuation if word.lower()
        not in nltk.corpus.stopwords.words("english")
        ]
    return document


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # initialize a variable for the number of documents
    # initialize a set for all words in all documents
    # count the number of words in each document
    # add to word dictionary
    length = len(documents.keys())
    total_words = set(word for key in documents for word in documents[key])
    word_dict = dict()
    for word in total_words:
        word_counter = 0
        for values in documents.values():
            if word in values:
                word_counter += 1
        word_dict[word] = ln(length / word_counter)
    return (word_dict)


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # open a ranks dictionary
    # search through each of the files' words
    # and search for each of the query words
    # sort each of the responses
    # and index to n
    ranks = dict()
    for file, words in files.items():
        ranks[file] = 0
        for word in query:
            count = words.count(word)
            ranks[file] += count * idfs[word]
    ranks = {
                k: v for k, v in sorted(
                    ranks.items(),
                    key=lambda item: item[1], reverse=True
                    )
        }
    titles = list(ranks.keys())
    return titles[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # open a ranks dictionary
    # loop through the sentences
    # add all the matches to idfs
    ranks = dict()
    for sen, list_ in sentences.items():
        ranks[sen] = 0
        for q in query:
            if q in list_:
                ranks[sen] += idfs[q]

    # sort the ranks and convert to list
    ranks = {
        k: v for k, v in sorted(
            ranks.items(),
            key=lambda item: item[1], reverse=True)
        }
    ranks_items = ranks.items()
    ranks_items = list(ranks_items)[:10]

    # get a list of sentences
    sen_list = list(ranks.keys())

    # find the highest value
    ranks_items = ranks.items()
    highest_value = list(ranks_items)[:1]
    highest_value = highest_value[0][1]

    # make a list of values
    values = list(ranks.values())

    # check if there is a tie of highest values
    # count up the amount of query words in the sentence
    # then divide by sentence length
    value_count = values.count(highest_value)
    if value_count > 1:
        counter = 0
        term_dict = dict()
        for key in ranks.keys():
            term_counter = 0
            for word in query:
                if word in sentences[key]:
                    term_counter += 1

            # save the sentence ranking to term_dict
            term_dict[key] = term_counter / len(sentences[key])
            counter += 1

            # break if past the highest values
            if counter == value_count:
                break

        # sort and return the best sentence
        term_dict = {
            k: v for k, v in sorted(
                term_dict.items(),
                key=lambda item: item[1], reverse=True)
            }
        term_list = list(term_dict.keys())
        return term_list[:n]

    return sen_list[:n]


if __name__ == "__main__":
    main()
