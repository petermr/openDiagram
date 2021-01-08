
UTF8 ='utf-8'

TITLE = "title"
BBOX  = "bbox"
X_SIZE = "x_size"
OCRX_WORD = "ocrx_word"
OCR_LINE = "ocr_line"
BASELINE = "baseline"
TEXTANGLE = "textangle"


debug = True
class Tesseract:
    # https://pypi.org/project/pytesseract/
    # top
    from PIL import Image
    import os
    import pytesseract
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
#    %matplotlib inline

    from skimage import data, img_as_float
    from skimage import exposure
    from skimage.viewer import ImageViewer

    HOME = os.path.expanduser("~")
    JUPYTER = os.path.join(HOME, "workspace", "jupyter")
    PHYSCHEM = os.path.join(JUPYTER, "physchem")
    PHYSCHEM_IMAGES = os.path.join(PHYSCHEM, "images")

    TEST_PNG = os.path.join(PHYSCHEM_IMAGES, 'capacitycycle.png')

    HTMLNS = "{http://www.w3.org/1999/xhtml}"

    image = None
    debug = True

    if __name__ == '__main__':
        test

    def __init__(self, png, debug=False):
        self.png = png
        self.debug = debug
#        self.image = Image.open(self.png, 'r')


        # If you don't have tesseract executable in your PATH, include the following:
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'
        # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'


    def get_strings(self):
        if (tesseract_strings == None and not self.png == None):
            self.tesseract_strings = pytesseract.image_to_string(Image.open(self.png))

            if self.debug:
                print("tesseract strings", self.tesseract_strings)

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
            self.bboxes = pytesseract.image_to_boxes(Image.open(self.png))
            if self.debug:
                print(self.bboxes[:100], "\n...\n", self.bboxes[-100:])
        return bboxes

    def get_chunks(self):
    # Get verbose data including boxes, confidences, line and page numbers
        if self.chunks == None and not self.png == None:
            self.chunks = pytesseract.image_to_data(Image.open(self.png))
            if self.debug:
                print(type(self.chunks),"\n", self.chunks[:200], "\n...\n", self.chunks[-200:])
        return self.chunks

    def get_image_script(self):
    # Get information about orientation and script detection
        osd = pytesseract.image_to_osd(Image.open(test_png))
        if debug:
            print("osd...\n",osd)
        return osd

    def create_pdf(self):
        # Get a searchable PDF
        pdf = pytesseract.image_to_pdf_or_hocr(test_png, extension='pdf')
        if debug:
            print("pdf...\n", pdf)
        return pdf

    def create_hocr(self):
    # Get HOCR output
        hocr = pytesseract.image_to_pdf_or_hocr(test_png, extension='hocr')
        if debug:
            print("hocr...\n", hocr)
        return hocr

    @staticmethod
    def test0(test_png=TEST_PNG):
        tesseract = Tesseract()

    def get_osd_dict():
        tesseract = tt.Tesseract()
        osd = tesseract.get_osd()
        osd_dict = pytesseract.osd_to_dict(osd)
        if debug:
            print("osd dict ", osd_dict)
        return osd_dict


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
    def get_tesseract_bboxes(image=image):
        bboxes = pytesseract.image_to_boxes(image)
        if debug:
            print(bboxes[:100], "\n...\n", bboxes[-100:])
        return bboxes


    def get_data_as_strings(image=image):
    # Get verbose data including boxes, confidences, line and page numbers
    # hocr may be better
        data = pytesseract.image_to_data(image)
        if debug:
            print(type(data),"\n", data[:200], "\n...\n", data[-200:])
        plot_dict[DATA] = data
        return data

    def get_osd(image):
    # Get information about orientation and script detection
        osd = pytesseract.image_to_osd(image)
        if debug:
            print(osd)
        plot_dict[OSD] = osd
        return osd

    @staticmethod
    def add_title_list_to_dict(key, value_list, dict):
        """add list to dict, converting to int or float if possible"""
        try:
            int_list = list(map(int, value_list))
            dict[key] = int_list
        except ValueError:
            try:
                float_list = ['{:.2f}'.format(float(v)) for v in value_list]
                dict[key] = float_list
            except ValueError:
                dict[key] = value_list
                print(" strings", value_list)

    @staticmethod
    def decode_title(elem):
        """decodes the hocr title attribute into a Python dictionary"""
        title = elem.attrib[TITLE ]
        params = title.split(";")
        dict = {}
        for param in params:
            chunks = param.strip().split(" ", 1)
            key = chunks[0]
            value_list = chunks[1].split(" ")
            Tesseract.add_title_list_to_dict(key, value_list, dict)
        return dict

    @staticmethod
    def get_tesseract_textboxes(image_file):
        import pytesseract36 as pytesseract
        import xml.etree.ElementTree as ET

        HTMLNS = "{http://www.w3.org/1999/xhtml}"

        # Get HOCR output
        """
     <?xml version="1.0" encoding="UTF-8"?>
     <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
     <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
      <head>
       <title></title>
       <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
       <meta name='ocr-system' content='tesseract 4.1.1' />
       <meta name='ocr-capabilities' content='ocr_page ocr_carea ocr_par ocr_line ocrx_word ocrp_wconf'/>
      </head>
      <body>
       <div class='ocr_page' id='page_1' title='image "/Users/pm286/workspace/jupyter/physchem/images/capacitycycle.png"; bbox 0 0 830 652; ppageno 0'>
        <div class='ocr_carea' id='block_1_1' title="bbox 2 93 40 486">
         <p class='ocr_par' id='par_1_1' lang='eng' title="bbox 2 93 40 486">
          <span class='ocr_line' id='line_1_1' title="bbox 2 93 40 486; textangle 90; x_size 38; x_descenders 6; x_ascenders 14">
           <span class='ocrx_word' id='word_1_1' title='bbox 10 374 40 486; x_wconf 96'>Specific</span>
           <span class='ocrx_word' id='word_1_2' title='bbox 10 245 40 363; x_wconf 96'>capacity</span>
           <span class='ocrx_word' id='word_1_3' title='bbox 10 175 40 233; x_wconf 93'>(mA</span>
           <span class='ocrx_word' id='word_1_4' title='bbox 2 93 40 164; x_wconf 0'>hg’)</span>
          </span>
         </p>
         """


        hocr = pytesseract.image_to_pdf_or_hocr(image_file, extension='hocr')
        hocr_html = hocr.decode(UTF8)
        root = ET.fromstring(hocr_html)
        hocrlines = hocr_html.split("\n")
        if debug:
            for hocrline in hocrlines[:25]:
                print(">>", hocrline)
        # namespaces...
        xpathpara = ".//" + HTMLNS + "p"
        paras = root.findall(xpathpara)
        if debug:
            print("paras", len(paras))
        textboxes = []
        for para in paras:
            params = Tesseract.decode_title(para)
            if params == None:
                print("no para params")
            else:
                pass
            lines = para.findall("./"+HTMLNS + "span[@class='"+OCR_LINE+"']")
            for line in lines:
                params = Tesseract.decode_title(line)
                if params == None:
                    print("no line params")
                else:
                    xsize = params.get(X_SIZE)
                    baseline = params.get(BASELINE)
                    textangle = params.get(TEXTANGLE)
                    if debug:
                        print("xsize ", xsize, " baseline ", baseline, "textangle ", textangle)
                # descenders omitted
                words = line.findall("./"+HTMLNS + "span[@class='"+OCRX_WORD+"']")
                for word in words:
                    params = Tesseract.decode_title(word)
                    if params == None:
                        print("no word params")
                    bbox = params.get(BBOX)
                    textboxes.append((word.text, bbox, textangle))

        if debug:
            print(">textboxes>", textboxes[:6])

        return textboxes
