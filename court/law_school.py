# Imports
import os
import csv
import numpy as np
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt
from sklearn.externals import joblib


# Def Graph Helpers
def hist_plot(data, labels, title):
    plt.clf()
    plt.hist(data, 100, label=labels)
    plt.legend(loc='upper right')
    plt.title(title)
    plt.savefig(os.path.join('..', 'figures', title.replace(' ', '') + '.jpg'))


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
lasso = LassoCV(n_jobs=-1, random_state=0, verbose=2, cv=5)

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
# lasso.fit(x_train, y_train)


# Evaluate Classifiers for each judge
def eval_judge(name, x_test, y_test):
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

    print "RMSE for %s: %d" % (name, score)
    print "R^2 Score for %s: %d" % (name, r2score)

    # Graph errors
    errs = np.subtract(trim_preds, y_test)

    to_graph = np.vstack((y_test, trim_preds)).T
    hist_plot(to_graph, ['Gold', 'Predicted'],
              'Gold vs Predicted Ratings for %s' % name)

    hist_plot(errs, ['Errors'], 'Errors for %s' % name)

    # Save Classifiers
    joblib.dump([lr, cv], 'judge.pkl')


hist_plot(labels, ['Gold Labels'], 'Gold Label Distribution')
eval_judge('LinearRegression', x_test, y_test)
# eval_judge('Lasso', x_test, y_test)
