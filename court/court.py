from sklearn.externals import joblib
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
from enchant.checker import SpellChecker
import sys
import os
import piexif


def go_to_court(court_path, tesseract_path):
    def verdict(evidence):
        """ Make a verdict (review) about evidence (plot summary) """
        # Import Judge (clf, count_vec) combo
        clf, cv = joblib.load(os.path.join(court_path, 'judge.pkl'))

        # Use cv to transform the data
#        print "Reviewing older cases (transforming summary)"
        feats = cv.transform(evidence)

        # Use clf to return a verdict
#        print "Order in the court! Verdict produced! (review returned)"
        return clf.predict(feats)

    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    image = Image.open(os.path.join(court_path, 'image.jpg'))
    exif_dict = piexif.load(image.info["exif"])
    w, h = image.size
    exif_dict['0th'][piexif.ImageIFD.XResolution] = (w, 1)
    exif_dict['0th'][piexif.ImageIFD.YResolution] = (h, 1)
    exif_bytes = piexif.dump(exif_dict)
    image.save('image', 'jpeg', exif=exif_bytes)
    image = Image.open(os.path.join(court_path, 'image.jpg'))
#    image.rotate(90)
    image = image.resize((image.width * 2, image.height * 2), Image.BILINEAR)
    image = ImageEnhance.Contrast(image).enhance(5.0)

    text = pytesseract.image_to_string(image)
#    print text
    with open(os.path.join(court_path, 'text.txt'), 'w') as f:
        f.write(text.encode('utf8'))
    chkr = SpellChecker("en_US")
    chkr.set_text(text)
    count = 0
    for err in chkr:
        # print err.word
        count += 1

    # print count
    # print len(text.split())
    goodness = float(count) / len(text.split())
    if goodness > 0.15:
        print "-99"
        sys.stdout.flush()
    else:
        print str(verdict([text])[0])
        sys.stdout.flush()
