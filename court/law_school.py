# Imports
import os
import csv
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt
from sklearn.externals import joblib

# Load Data
data_file = os.path.join('..', 'data', 'combined.csv')
data = []
labels = []

print "Buying LSAT books (loading in the data...)"
with open(data_file, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        data += [row[1]]
        labels += [float(row[2])]

# Instantiate Classifiers
lr = LinearRegression(n_jobs=-1)

# Extract Features From Data
print "Studying for LSAT (extracting features from the data...)"
cv = CountVectorizer()
feats = cv.fit_transform(data)

# Split into Train / Test sets
x_train, x_test, y_train, y_test = \
    train_test_split(feats, labels, test_size=0.33, random_state=0)

# Train Classifiers
print "Judge is going to school (training the classifiers...)"
lr.fit(x_train, y_train)

# Evaluate Classifiers
preds = lr.predict(x_test)
trim_preds = preds.clip(min=0, max=5)  # clip to 0-5 range
count = 0
for i in range(len(trim_preds)):
    diff = trim_preds[i] - y_test[i]
    if abs(diff) > .5:
        print diff
        count += 1

print "Number of egregious errors: ", count
print "Number of verdicts: ", len(y_test)

r2score = r2_score(y_test, trim_preds)
score = mean_squared_error(y_test, trim_preds)

print "RMSE: ", score
print "R^2 Score ", r2score

# Graph errors
errs = np.subtract(trim_preds, y_test)

to_graph = np.vstack((y_test, trim_preds)).T
plt.hist(to_graph, 50, label=['gold', 'pred'])
plt.legend(loc='upper right')
plt.title('Gold vs Predicted Ratings')

fig2 = plt.figure(2)
plt.hist(errs, 50, label=['errors'])
plt.legend(loc='upper right')

fig3 = plt.figure(3)
plt.hist(labels, 100, label=['Gold Labels'])
plt.legend(loc='upper right')
plt.title('Gold Label Distribution')
plt.show()

# Save Classifiers
joblib.dump([lr, cv], 'judge.pkl')
