import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import sklearn

from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing  import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import classification_report, confusion_matrix
from math import sqrt


# For more verbose printing and added information make "True"
DEBUG = False

dataset = pd.read_csv("HW3Data.csv")
if DEBUG:
    print("Imported Dataset")
    print(dataset.shape)
    print(dataset)
    print(dataset.describe().transpose())

x = dataset.drop('Class', axis=1)
y = dataset['Class']

#Break up input data into randomized chunks of data
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

if DEBUG:
    print("X_train")
    print(X_train)
    print("X_test")
    print(X_test)
    print("y_train")
    print(y_train)
    print("y_test")
    print(y_test)

#Scale the data
scaler = StandardScaler()
scaler.fit(X_train)

X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)

#Multi Layer Perceptron Multiplier - Neural Net Classifier
mlp = MLPClassifier(hidden_layer_sizes=(2,))
mlp.fit(X_train_s, y_train) #fit classifier to training data

# Part 1
predict_test  = mlp.predict(X_test) # 30% of data
predict_train = mlp.predict(X_train)# 70% of data

df_pred_train = pd.DataFrame(data={'pred': predict_train})

colors = np.where(df_pred_train['pred']==1,'r','k')
shape =  np.where(df_pred_train["pred"]==y_train.tolist(),'1','o')

X_plt = X_train["X"].tolist()
Y_plt = X_train["Y"].tolist()

for i in range(len(y_train.tolist())):
    plt.plot(int(X_plt[i]), int(Y_plt[i]), c=colors[i], marker=shape[i])

# Put points data through MLP and predict outcome
plt.savefig('part1_1.png')
#plt.show()


# Part 2
print("Confusion Matrix")
print(confusion_matrix(y_test, predict_test))
print(classification_report(y_test, predict_test))

# Part 3
x2, y2 = np.meshgrid(np.arange(70), np.arange(70))
x2, y2 = x2.flatten(), y2.flatten()
points = np.vstack((x2,y2)).T
predict_points = mlp.predict(points)

plt_x, plt_y = zip(*points)

d = {'x': plt_x, 'y':plt_y, 'c':predict_points}
df = pd.DataFrame(data=d)

colors = np.where(df['c']==1, 'r', 'k')
df.plot.scatter(x='x', y='y', c=colors)
plt.title('Prediction 70 by 70')
plt.savefig('70by70_part3.png')
plt.clf()

# Part 4
dataset = pd.read_csv("HW3Data.csv")
if DEBUG:
    print("Imported Dataset")
    print(dataset.shape)
    print(dataset)
    print(dataset.describe().transpose())

x = dataset.drop('Class', axis=1)
y = dataset['Class']

#Break up input data into randomized chunks of data
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

if DEBUG:
    print("X_train")
    print(X_train)
    print("X_test")
    print(X_test)
    print("y_train")
    print(y_train)
    print("y_test")
    print(y_test)

#Scale the data
scaler = StandardScaler()
scaler.fit(X_train)

X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)

#Multi Layer Perceptron Multiplier - Neural Net Classifier
mlp = MLPClassifier(hidden_layer_sizes=(2,))
mlp.fit(X_train_s, y_train) #fit classifier to training data

# Part 1
predict_test  = mlp.predict(X_test) # 30% of data
predict_train = mlp.predict(X_train)# 70% of data

df_pred_train = pd.DataFrame(data={'pred': predict_train})

colors = np.where(df_pred_train['pred']==1,'r','k')
shape = np.where(df_pred_train["pred"]==y_train.tolist(),'1','o')


X_plt = X_train["X"].tolist()
Y_plt = X_train["Y"].tolist()

for i in range(len(y_train.tolist())):
    plt.plot(int(X_plt[i]), int(Y_plt[i]), c=colors[i], marker=shape[i])

# Put points data through MLP and predict outcome
plt.savefig('part1_2.png')


# Part 2
print("Confusion Matrix")
print(confusion_matrix(y_test, predict_test))
print(classification_report(y_test, predict_test))

# Part 3
x2, y2 = np.meshgrid(np.arange(70), np.arange(70))
x2, y2 = x2.flatten(), y2.flatten()
points = np.vstack((x2,y2)).T
predict_points = mlp.predict(points)

plt_x, plt_y = zip(*points)

d = {'x': plt_x, 'y':plt_y, 'c':predict_points}
df = pd.DataFrame(data=d)

colors = np.where(df['c']==1, 'r', 'k')
df.plot.scatter(x='x', y='y', c=colors)
plt.title('Prediction 70 by 70')
plt.savefig('70by70_part4.png')