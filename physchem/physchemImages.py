def physchem_image_dict():
    import os
    HOME = os.path.expanduser("~")
    JUPYTER = os.path.join(HOME, "workspace", "jupyter")
    IMAGES = os.path.join(JUPYTER, "physchem", "images")
    PHYSCHEM_LIION = os.path.join(JUPYTER, "physchem", "liion")
    PHYSCHEM_IMAGES = os.path.join(JUPYTER, "physchem", "images")
    imgdict = {"RED_BLACK" : os.path.join(PHYSCHEM_IMAGES, "red_black_cv.png"),
            "CAPACITY" : os.path.join(PHYSCHEM_IMAGES, "capacitycycle.png"),
            "GREEN" : os.path.join(PHYSCHEM_LIION, 'PMC7077619/pdfimages/image.8.3.81_523.164_342/raw.png'),
            "PANEL2" : os.path.join(PHYSCHEM_LIION, 'PMC7075112/pdfimages/image.5.2.98_499.292_449/raw.png'),
            "PLOT2" : os.path.join(PHYSCHEM_LIION, 'PMC7075112/pdfimages/image.4.3.117_479.722_864/raw.png'),
            "PLOT3" : os.path.join(PHYSCHEM_LIION, 'PMC7074852/pdfimages/image.7.3.86_507.385_495/raw.png'),
            "PLOT32" : os.path.join(PHYSCHEM_LIION, 'PMC7067258/pdfimages/image.5.1.52_283.71_339/raw.png'),
              }
    return imgdict
