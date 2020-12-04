import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix


dataset = pd.read_csv("HW3Data.csv")
dataset.shape

x = dataset.drop('Class', axis=1)
y = dataset['Class']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

# Create decision tree classifier and train it
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print_all = 1

# Part 1

if print_all:
    #export text from decision tr
    print("Decision Tree (text): \n")
    print(tree.export_text(classifier))

# Part 2

if print_all:
    print("\nConfusion Matrix: \n")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report: \n")
    print(classification_report(y_test, y_pred))


# Part 3
x2, y2 = np.meshgrid(np.arange(70), np.arange(70))
x2, y2 = x2.flatten(), y2.flatten()
points = np.vstack((x2,y2)).T
pred = classifier.predict(points)

plt_x, plt_y = zip(*points)

d = {'x': plt_x, 'y':plt_y, 'c':pred}
df = pd.DataFrame(data=d)

colors = np.where(df['c']==1, 'r', 'k')
df.plot.scatter(x='x', y='y', c=colors)
plt.title('Prediction 70 by 70')
plt.savefig('70by70_part3.png')

if print_all:
    plt.plot()


# Part 4

print(dataset)
colors_org = np.where(dataset['Class']==1,'r','k')
print(colors_org)

dataset.plot.scatter(x="X", y="Y", c=colors_org)
plt.title('Prediction xlsx Data')
plt.savefig('scatter_part4.png')

if print_all:
    plt.plot()
