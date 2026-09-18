import csv

from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

model = svm.SVC()

with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)
    data = []
    for row in reader:
        data.append({
            "feature" : [float(cell) for cell in row[:4]],
            "label" : "Authentic" if row[4] == "0" else "Counterfeit"
        })

feature = [row["feature"] for row in data]
label = [row["label"] for row in data]

x_training , x_testing , y_training , y_testing  = train_test_split(
    feature , label , test_size=0.4 
)

model.fit(x_training, y_training)

predictions = model.predict(x_testing)

correct = (y_testing == predictions).sum()
incorrect = (y_testing != predictions).sum()
total = len(predictions)

print(f"results for model {type(model).__name__}")
print(f"correct: {correct}")
print(f"incorrect: {incorrect}")
print(f"accuracy: {100 * correct / total:.2f}%")