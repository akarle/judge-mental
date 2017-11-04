try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
from PIL import ImageEnhance
from enchant.checker import SpellChecker


def extract_evidence(image_name):
    """Returns text extracted from image with image_name"""
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

    image = Image.open(image_name)
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
        return ""
    else:
        return text