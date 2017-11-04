#!/usr/bin/env python

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
from PIL import ImageEnhance
from enchant.checker import SpellChecker
import sys

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

image = Image.open('image.jpg')
image = image.resize((image.width * 2, image.height * 2), Image.BILINEAR)
image = ImageEnhance.Contrast(image).enhance(5.0)

text = pytesseract.image_to_string(image)

chkr = SpellChecker("en_US")
chkr.set_text(text)
count = 0
for err in chkr:
    count += 1

goodness = float(count) / len(text.split())
print goodness
if goodness > 0.15:
    print ""
    sys.stdout.flush()
else:
    print text
    sys.stdout.flush()
