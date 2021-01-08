
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from skimage import data, img_as_float
from skimage import exposure
from skimage.viewer import ImageViewer

# note complete source
import pytesseract36 as pytesseract

from PIL import Image

class Tesseract:

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# https://pypi.org/project/pytesseract/

    if __name__ == '__main__':
        pass
#        test0()

    @staticmethod
    def images():
        files = [
            os.path.join("liion", "PMC7040616", "pdfimages", "image.3.1.203_392.180_407", "raw.png"),
            os.path.join("liion", "PMC7052380", "pdfimages", "image.7.3.309_547.90_487", "raw.png"),
        ]
        return files

    def __init__(self, png=None, debug=True):

        print("Tesseract ctr")
        self.debug = debug
        self.image_file = os.path.join('images', 'capacitycycle.png') if png == None else png
        self.init0()
        print("end ctr", self.image_file)

    def init0(self):
        self.tesseract_strings = None
        self.bboxes = None
        self.data = None
        print("init-ed")

    def get_strings(self):
        if (self.tesseract_strings == None and not self.image_file == None):
            if self.debug:
                print("exists", self.image_file)
            self.tesseract_strings = pytesseract.image_to_string(Image.open(self.image_file))
            if self.debug:
                print("t_strings", self.tesseract_strings)

            if self.debug:
                print(self.tesseract_strings)
        return self.tesseract_strings

    # In order to bypass the image conversions of pytesseract, just use relative or absolute image path
    # NOTE: In this case you should provide tesseract supported images or tesseract will return error
    # print(pytesseract.image_to_string('test.png'))

    # Batch processing with a single file containing the list of multiple image file paths
    # print(pytesseract.image_to_string('images.txt'))

    # Timeout/terminate the tesseract job after a period of time
    """
    try:
        print(pytesseract.image_to_string('test.jpg', timeout=2)) # Timeout after 2 seconds
        print(pytesseract.image_to_string('test.jpg', timeout=0.5)) # Timeout after half a second
    except RuntimeError as timeout_error:
        # Tesseract processing is terminated
        pass
    """
    # Get bounding box estimates
    def get_bounding_boxes(self):
        if self.bboxes == None:
            self.bboxes = pytesseract.image_to_boxes(Image.open(self.image_file))
            if self.debug:
                print("boxes\n", self.bboxes[:100], "\n...\n", self.bboxes[-100:])
        return self.bboxes

    def get_data(self):
    # Get verbose data including boxes, confidences, line and page numbers
        if self.data == None and not self.image_file == None:
            self.data = pytesseract.image_to_data(Image.open(self.image_file))
            if self.debug:
                print("chunks\n", self.data,"\n", self.data[:200], "\n...\n", self.data[-200:])
        return self.data

    def get_pandas(self, config=None):
        image = Image.open(self.image_file)
        lang=None
        config=''
        nice=0
        timeout=0
        args = [image, 'box', lang, config, nice, timeout]
        self.pandas = pytesseract.get_pandas_output(Image.open(self.image_file))
        if self.debug:
            print(self.pandas)
            pass
        return self.pandas


    def get_osd(self):
    # Get information about orientation and script detection
        osd = pytesseract.image_to_osd(Image.open(self.image_file))
        if self.debug:
            print("osd: \n", osd)
        return osd

    def get_dict_from_osd(self, osd):
        return pytesseract.osd_to_dict(self.get_osd())

    def create_pdf(self):
        # Get a searchable PDF
        pdf = pytesseract.image_to_pdf_or_hocr(self.image_file, extension='pdf')
        if self.debug:
#            print(pdf)
            pass
        return pdf

    def create_hocr(self):
    # Get HOCR output
        hocr = pytesseract.image_to_pdf_or_hocr(self.image_file, extension='hocr')
        if self.debug:
#            print(hocr)
            pass
        return hocr

    def create_pandas(self, *args):
    # Get Pandas output NOT TESTED
        self.pandas = get_pandas()

    def test(self):
        print("get_strings\n", self.get_strings())
        print("get_bounding_boxes\n", self.get_bounding_boxes())
        if self.debug:
            chunks = self.get_data()
            print("get_chunks\n", type(chunks), " ", len(chunks), "\n", chunks)
        osd = self.get_osd()
        print("get_osd\n", type(osd), osd)

        pdf = self.create_pdf()
#        print("create_pdf\n", pdf)
        hocr = self.create_hocr()
#        print("create_hocr\n", hocr)
        args = None # TESTING
        pandas = self.get_pandas(args)
        print("create_pandas\n", pandas)

"""
    def __init__(self, png, debug=False):
        self.image_file = png
        self.debug = debug
        self.image = Image.open(self.image_file, 'r')


"""
