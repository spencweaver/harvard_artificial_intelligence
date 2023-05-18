# import csv
import sys

import pandas as pd

from sklearn.metrics import confusion_matrix

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # read in the data
    df = pd.read_csv(filename)

    # format the date column correctly
    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]
    d = {month_: i for i, month_ in enumerate(months)}
    df['Month'] = df['Month'].replace(d)

    # format the "VisitorType", "Weekend", and "Revenue" columns
    df["VisitorType"] = df["VisitorType"].replace(
        {"New_Visitor": 0, "Returning_Visitor": 1, "Other": 0}
        )

    df["Weekend"] = df["Weekend"].replace({False: 0, True: 1})
    df["Revenue"] = df["Revenue"].replace({False: 0, True: 1})

    # create empty lists for evidence and labels
    # for every loop iteration save row values to the row_ variable
    # then split the data for both the evidence and labels lists
    # then return as a tuple
    evidence, labels = [], []
    for _, row in df.iterrows():
        row_ = list(row.values)
        evidence.append(row_[:17])
        labels.append(row_[17])

    return tuple([evidence, labels])


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # create a model instance
    model = KNeighborsClassifier(n_neighbors=1)

    # fit data to model and return
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # create the confusion matrix
    # pull out the relavent information
    # example code from Chris Sorenson's Titanic Jupyter notebook
    matrix = confusion_matrix(
        labels, predictions, labels=None, sample_weight=None, normalize=None
        )
    true_neg, false_pos, false_neg, true_pos = matrix.ravel()

    # calculate the sensitivity and specificity scores
    # based on the supplied formulas and return
    sensitivity = true_pos / (true_pos + false_neg)
    specificity = true_neg / (true_neg + false_pos)

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
