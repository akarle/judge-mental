from sklearn.externals import joblib
from PIL import Image, ImageEnhance
import pytesseract
from enchant.checker import SpellChecker
import sys


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


pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

image = Image.open('/home/ubuntu/judge-mental/court/image.jpg')
image = image.resize((image.width * 2, image.height * 2), Image.BILINEAR)
image = ImageEnhance.Contrast(image).enhance(5.0)

text = pytesseract.image_to_string(image)

chkr = SpellChecker("en_US")
chkr.set_text(text)
count = 0
for err in chkr:
    count += 1

goodness = float(count) / len(text.split())
if goodness > 0.15:
    print "-99"
    sys.stdout.flush()
else:
    print str(verdict([text])[0])
    sys.stdout.flush()
