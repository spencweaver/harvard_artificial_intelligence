import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
import sys

import os
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import word_tokenize
from collections import Counter
from numpy import log as ln
import string

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 190)

import speech_recognition

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    print('loading the data ...')
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)
    while True:
        # Prompt user for query
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            # engine.say("To say something press enter: ")
            # engine.runAndWait()
            
            input("To say something press enter: ")
            audio = recognizer.listen(source)
            
        
        query = recognizer.recognize_google(audio)
        print(f"You said: '{query}'")
        # query = set(tokenize(input("Query: ")))
        query = set(tokenize(query))


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
            
            
            
            engine.say(match)
            engine.runAndWait()
            


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    content = {}

    
    files = os.listdir(directory)
    subject_list = ['Ask me about']
    for file in files:
        file, _ = file.split('.')
        name = file.split('_')
        string = ' '.join(name)
        string = string + ','
        subject_list.append(string)
    
    subject_string = ' '.join(subject_list)
    subject_string += '.'
    
    engine.say(subject_string)
    engine.runAndWait()


    for file in files:

        path = os.path.join(directory, file)
        f = open(path)
        content[file] = f.read()
    return content
    raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # print(type(document))
    document = word_tokenize(document)
    document = [word.lower() for word in document if word.lower() not in string.punctuation if word.lower() not in nltk.corpus.stopwords.words("english")]


    return document
    raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # print(type(documents))
    length = len(documents.keys())
    nat_log = ln(length)
    # print(f"length {length}")
    # print(f"nat_log {nat_log}")
    
    total_words = set(word for key in documents for word in documents[key])

    word_dict = dict()
    for word in total_words:
        # print(word)

        word_counter = 0
        for key, values in documents.items():
            if word in values:
                word_counter += 1

        word_dict[word] = nat_log / word_counter
        # print(word_dict[word])

    # print(len(documents.values()))
    # print(len(word_dict))
    return(word_dict)
    raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    filenames = []
    # print(query)
    # print(files)
    # print(idfs)
    # print(f"n ---> {n}")
    

    

    ranks = dict()
    for file, words in files.items():
        # print("######################")
        # print(file)

        ranks[file] = 0
        

        for word in query:
            # if word in words:
                # print(f"word in words {word}")

                # print(f"count ---> {count}")
            count = words.count(word)
            # print(f">>> '{word}' count ----> {count}")
            # print(f"idfs[word]::: {idfs[word]}")
            ranks[file] += count * idfs[word]
            # print(f"ranks[file]::: {ranks[file]}")
            # print(idfs[word])
    # print(ranks)
    ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}
    # for key, value in ranks.items():
    #     print(f"{key} ---> {value}")
    titles = list(ranks.keys())
    # print(titles)
    # titles = titles[::-1]
    # print(titles)

    # for t in titles:
    #     print(ranks[t])

    # print(titles[:n])
    return titles[:n]



    raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # print(query)
    # print(sentences)
    # print(n)
    ranks = dict()
    for sen, list_ in sentences.items():
        # print('#######################################')
        ranks[sen] = 0
        for q in query:
            if q in list_:
                # print('------------------------------------')
                
                # print(f"ranks[sen] before: {ranks[sen]}")
                ranks[sen] += idfs[q]
                # print(f"ranks[sen] after: {ranks[sen]}")
    # print(ranks)

    ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}
    # print(ranks)
    ranks_items = ranks.items()
    ranks_items = list(ranks_items)[:10]

    # print("ranks")

    sen_list = list(ranks.keys())
    # for key, value in ranks.items():
    #     print(f"{key} ---> {value}")
    # print(sen_list)
    # sen_list = sen_list[::-1]
    # print(sen_list)

    # for t in sen_list:
    #     print(ranks[t])

    # print(sen_list[:n])
    # print(type(nltk.corpus.stopwords.words("english")))
    # print(string.punctuation)
    # for sen in sen_list[:6]:
    #     print(sen)

    ranks_items = ranks.items()
    highest_value = list(ranks_items)[:1]
    highest_value = highest_value[0][1]
    # highest_value = highest_value[1]
    # print('highest value')
    # print(highest_value)

    values = list(ranks.values())
    # print(f"values ----+ {values}")

    #### If there is a tie
    value_count = values.count(highest_value)
    if value_count > 1:
        # print(value_count)
        counter = 0
        term_dict = dict()
        for key, value in ranks.items():
            term_counter = 0
            for word in query:
                if word in sentences[key]:
                    term_counter += 1

            term_dict[key] = term_counter / len(sentences[key])
            counter += 1
            if counter == value_count:
                # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                break
        term_dict = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}
        # print(term_dict)
        term_list = list(term_dict.keys())
        return term_list[:n]
        
        # print(sen_list)
    # print('******************************************************')
    return sen_list[:n]

    raise NotImplementedError


if __name__ == "__main__":
    main()
