from sklearn.externals import joblib


def verdict(evidence):
    """ Make a verdict (review) about evidence (plot summary) """
    # Import Judge (clf, count_vec) combo
    clf, cv = joblib.load('judge.pkl')

    # Use cv to transform the data
    print "Reviewing older cases (transforming summary)"
    feats = cv.transform(evidence)

    # Use clf to return a verdict
    print "Order in the court! Verdict produced! (review returned)"
    return clf.predict(feats)
