import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def load_data(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        data = []
        for row in reader:
            months = {
                "Jan": 0,
                "Feb": 1,
                "Mar": 2,
                "Apr": 3,
                "May": 4,
                "June": 5,
                "Jul": 6,
                "Aug": 7,
                "Sep": 8,
                "Oct": 9,
                "Nov": 10,
                "Dec": 11,
            }
            visitorType = {
                "Returning_Visitor" : 1,
                "New_Visitor" : 0,
                "Other" : 0
            }
            Weekend = 1 if row[16] == "TRUE" else 0
            data.append({
                "evidence" : [int(row[0]), float(row[1]), int(row[2]), float(row[3]), int(row[4]), float(row[5]),
                              float(row[6]), float(row[7]), float(row[8]), float(row[9]), months[row[10]], 
                              int(row[11]), int(row[12]), int(row[13]), int(row[14]), visitorType[row[15]], Weekend],
                "label" : 1 if row[17] == "TRUE" else 0
            })
    evidence = [row["evidence"] for row in data]
    label = [row["label"] for row in data]
    return evidence, label

def train_model(x_train, y_train):
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(x_train, y_train)
    return model

def evaluate(label, prediction):
    true_positive = 0
    false_negative = 0
    false_positive = 0
    true_negative = 0

    for actual, predicted in zip(label, prediction):
        if actual == 1 and predicted == 1:
            true_positive += 1
        elif actual == 1 and predicted == 0:
            false_negative += 1
        elif actual == 0 and predicted == 1:
            false_positive += 1
        else:
            true_negative += 1

    sensitivity = true_positive / (true_positive + false_negative)
    specificity = true_negative / (true_negative + false_positive)

    return sensitivity, specificity

if __name__ == "__main__":
    main()