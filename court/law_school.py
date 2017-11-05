# Imports
import os
import csv
import numpy as np
from sklearn.linear_model import LinearRegression, LassoCV, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from matplotlib import pyplot as plt
from sklearn.externals import joblib
import nltk


# Helper Funcs
def hist_plot(data, labels, title, xlabel="Book Ratings"):
    plt.clf()
    plt.hist(data, 100, label=labels)
    plt.legend(loc='upper right')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of Samples")
    plt.savefig(os.path.join('..', 'figures', title.replace(' ', '') + '.jpg'))


def eval_judge(name, model, x_test, y_test):
    preds = model.predict(x_test)
    trim_preds = preds.clip(min=0, max=5)  # clip to 0-5 range
    count = 0
    for i in range(len(trim_preds)):
        diff = trim_preds[i] - y_test[i]
        if abs(diff) > .5:
            # print diff
            count += 1

    print "Number of egregious errors: ", count
    print "Number of verdicts: ", len(y_test)

    r2score = r2_score(y_test, trim_preds)
    rmse_score = mean_squared_error(y_test, trim_preds)

    print "RMSE for %s: %f" % (name, rmse_score)
    print "R^2 Score for %s: %f" % (name, r2score)

    # Graph errors
    errs = np.subtract(trim_preds, y_test)

    to_graph = np.vstack((y_test, trim_preds)).T
    hist_plot(to_graph, ['Gold', 'Predicted'],
              'Gold vs Predicted Ratings for %s' % name)

    hist_plot(errs, ['Errors'], 'Errors for %s' % name,
              xlabel=("Difference in Gold vs Predicted Rating: " +
              "RMSE: %f , R^2: %f" % (rmse_score, r2score)))

    # Save Classifiers
    joblib.dump([model, cv], 'judge%s.pkl' % name.replace(" ", ''))


def preprocess(string):
    tokens = nltk.word_tokenize(string)
    pos_tokens = nltk.pos_tag(tokens)
    ls = ['POS_' + x[1].lower() + '_' + x[0].lower() for x in pos_tokens]
    return ' '.join(ls)


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
# lr = LinearRegression(n_jobs=-1)
# lasso = LassoCV(n_jobs=-1, random_state=0, max_iter=2, verbose=3, cv=5)
lassopt01 = Lasso(alpha=.01, random_state=0)
lassopt1 = Lasso(alpha=.1, random_state=0)
lasso1 = Lasso(alpha=1, random_state=0)
lasso10 = Lasso(alpha=10, random_state=0)
# rf = RandomForestRegressor(n_estimators=20, random_state=0,
                           # n_jobs=-1, verbose=2)

# Extract Features From Data
print "Studying for LSAT (extracting features from the data...)"
cv = CountVectorizer(preprocessor=preprocess, ngram_range=(1, 2))
feats = cv.fit_transform(data)

print cv.vocabulary_

# Split into Train / Test sets
x_train, x_test, y_train, y_test = \
    train_test_split(feats, labels, test_size=0.2, random_state=0)

# Train Classifiers
print "Judge is going to school (training the classifiers...)"
# lr.fit(x_train, y_train)
# lasso.fit(x_train, y_train)
# rf.fit(x_train, y_train)
lassopt01.fit(x_train, y_train)
lassopt1.fit(x_train, y_train)
lasso1.fit(x_train, y_train)
lasso10.fit(x_train, y_train)


# Evaluate Classifiers for each judge
hist_plot(labels, ['Gold Labels'], 'Gold Label Distribution')
# eval_judge('LinearRegressionUniBiPOS', lr, x_test, y_test)
eval_judge('LassoUniBiPOSalphapt1', lassopt01, x_test, y_test)
eval_judge('LassoUniBiPOSalphapt01', lassopt1, x_test, y_test)
eval_judge('LassoUniBiPOSalpha1', lasso1, x_test, y_test)
eval_judge('LassoUniBiPOSalpha10', lasso10, x_test, y_test)

# eval_judge('Lasso', lasso, x_test, y_test)
# eval_judge('RandomForest', rf, x_test, y_test)
