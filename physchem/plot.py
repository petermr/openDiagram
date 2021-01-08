image = None
IMAGE = "image"
IMAGE_ARRAY = "image_array"

XMIN = "xmin"
XMAX = "xmax"
YMIN = "ymin"
YMAX = "ymax"

plot_dict = {}

BOT_AXIS_TITLE = "bot_axis_title"
BOT_AXIS_SCALE = "bot_axis_scale"
BOT_AXIS_TICKS = "bot_axis_ticks"
BOT_AXIS_LINE =  "bot_axis_line"

LEFT_AXIS_TITLE = "left_axis_title"
LEFT_AXIS_SCALE = "left_axis_scale"
LEFT_AXIS_TICKS = "left_axis_ticks"
LEFT_AXIS_LINE =  "left_axis_line"

TOP_AXIS_TITLE = "top_axis_title"
TOP_AXIS_SCALE = "top_axis_scale"
TOP_AXIS_TICKS = "top_axis_ticks"
TOP_AXIS_LINE =  "top_axis_line"

RIGHT_AXIS_TITLE = "right_axis_title"
RIGHT_AXIS_SCALE = "right_axis_scale"
RIGHT_AXIS_TICKS = "right_axis_ticks"
RIGHT_AXIS_LINE  = "right_axis_line"

WHOLE_AREA     = "whole_area"
BOTTOM_TRIMMED = "bottom_trimmed"

PLOT_AREA = "plot_area"
OSD = "osd"
DATA = "data"

debug = True

import matplotlib.pyplot as plt
def xscale(image):

    plot_box(BOT_AXIS_TITLE)
    plot_box(BOT_AXIS_SCALE)
    plot_box(BOT_AXIS_TICKS)
    plot_box(BOT_AXIS_LINE)

    plot_box(TOP_AXIS_LINE)

def yscale(image):

    plot_box(LEFT_AXIS_TITLE)
    plot_box(LEFT_AXIS_SCALE)
    plot_box(LEFT_AXIS_TICKS)
    plot_box(LEFT_AXIS_LINE)

    plot_box(RIGHT_AXIS_LINE)

def section_scales(image):
    xscale(image)
    yscale(image)

def section_area(image):
    plot_box(PLOT_AREA)


def plot_sections():
    section_scales(image)
    section_area(image)

def make_boxes(textboxes, facecolor='r',
                     edgecolor='None', alpha=0.5):
    """textboxes are (text, numeric_bbox)"""
    import matplotlib.patches as mpatches
    rects = []
    x = []
    y = []
    texts = []
    for textbox in textboxes:
        text = textbox[0]
        box = textbox[1]
        x0 = box[0]
        y0 = box[1]
        x1 = box[2]
        y1 = box[3]
        x.append(x0)
        y.append(y0)
        rect = mpatches.Rectangle((x0, y0), x1 - x0 , y1 - y0, fill=False, facecolor=facecolor, lw=1, ec=edgecolor)
        texts.append((x0, y0, text))
        rects.append(rect)

    return x,y,rects, texts

def create_baselines(textboxes):
    from collections import Counter
    """
        origin is 0,0 so positive y is closest to normal bottom
        also text baselines are more positive
        text may be rotated in either direction
    """
    ytop = Counter()
    ybot= Counter()
    xleft = Counter()
    xright = Counter()
    xbase90 = Counter()
    for textbox in textboxes:
        text = textbox[0]
        box = textbox[1]
        rot = 0 if textbox[2] == None else textbox[2][0]
        print(textbox)
        x0 = box[0]
        y0 = box[1]
        x1 = box[2]
        y1 = box[3]
        width = x1 - x0
        height = y1 - y0
        if rot == 90:
            xbase90[x1] += 1
        elif rot == -90 or rot == 270:
            pass
        else:  # normal
#        y0 is the top of the box, y1 is normally baseline
            ytop[y0] += 1    # top of horizontal text
            ybot[y1] += 1    # baseline of horizontal text
            xleft[x0] += 1   # useful for l-justified ladders
            xright[x1] += 1  # useful for r-justified ladders

    print("\nxleft\n ", xleft, "\nxright\n", xright, "\nytop\n ", ytop,
        "\nybot\n", ybot, "\nxbase90\n", xbase90)

@staticmethod
def plot_textboxes(image, textboxes):
    x, y, rects, texts = make_boxes(textboxes)

    fig,ax = plt.subplots(1)
    ax.imshow(image)

    for text in texts:
        plt.text(text[0], text[1], text[2], color='blue', alpha=0.5)
    for rect in rects:
        ax.add_patch(rect)
        pass

    plt.show()

    image = None

def create_sections(image):

    get_image_and_shape(image)

    xmin = plot_dict.get(XMIN)
    xmax = plot_dict.get(XMAX)
    ymin = plot_dict.get(YMIN)
    ymax = plot_dict.get(YMAX)
    print("xybox", xmin, xmax, ymin, ymax)

    yb0 = (0, 38)
    yb1 = (38, 84)
    yb2 = (86, 96)
    yb3 = (98,103)

    xl0 = (0, 43)
    xl1 = (43, 116)
    xl2 = (116, 130)
    xl3 = (129, 134)

    yt0 = (650, 652)
    yt1 = (648, 650)
    yt2 = (646, 648)
    yt3 = (632, 636)

    xr0 = (825, 830)
    xr1 = (820, 825)
    xr2 = (810, 820)
    xr3 = (792, 797)

    plot_dict[WHOLE_AREA] = (xmin, xmax, ymin, ymax) # for debugging
    plot_dict[BOTTOM_TRIMMED] = (xmin, xmax, ymin + 50, ymax) # for debugging

    plot_dict[BOT_AXIS_TITLE] = (xmin, xmax, yb0[0], yb0[1])
    plot_dict[BOT_AXIS_SCALE] = (xmin, xmax, yb1[0], yb1[1])
    plot_dict[BOT_AXIS_TICKS] = (xl3[0], xr3[1], yb2[0], yb2[1])
    plot_dict[BOT_AXIS_LINE] =  (xl3[0], xr3[1], yb3[0], yb3[1])


    plot_dict[LEFT_AXIS_TITLE] = (xl0[0], xl0[1], ymin, ymax)
    plot_dict[LEFT_AXIS_SCALE] = (xl1[0], xl1[1], ymin, ymax)
    plot_dict[LEFT_AXIS_TICKS] = (xl2[0], xl2[1], yb3[0], yt3[1])
    plot_dict[LEFT_AXIS_LINE] =  (xl3[0], xl3[1], yb3[0], yt3[1])

    plot_dict[TOP_AXIS_TITLE] = (xmin, xmax, yt0[0], yt0[1])
    plot_dict[TOP_AXIS_SCALE] = (xmin, xmax, yt1[0], yt1[1])
    plot_dict[TOP_AXIS_TICKS] = (xl3[0], xr3[1], yt2[0], yt2[1])
    plot_dict[TOP_AXIS_LINE] =  (xl3[0], xr3[1], yt3[0], yt3[1])

    plot_dict[RIGHT_AXIS_TITLE] = (xr0[0], xr0[1], ymin, ymax)
    plot_dict[RIGHT_AXIS_SCALE] = (xr1[0], xr1[1], ymin, ymax)
    plot_dict[RIGHT_AXIS_TICKS] = (xr2[0], xr2[1], yb3[0], yt3[1])
    plot_dict[RIGHT_AXIS_LINE] =  (xr3[0], xr3[1], yb3[0], yt3[1])


    plot_dict[PLOT_AREA] = (xl3[1], xr3[0], yb3[1], yt3[0])

def get_image_and_shape(image):
    """store image array and its size in plot_dict"""
    import numpy as np

    plot_dict[IMAGE] = image
    image_array = np.array(image)
    plot_dict[IMAGE_ARRAY] = image_array
    xmin = 0
    plot_dict[XMIN] = xmin
    xmax = image_array.shape[1]
    plot_dict[XMAX] = xmax
    ymin = 0
    plot_dict[YMIN] = ymin
    ymax = image_array.shape[0]
    plot_dict[YMAX] = ymax

    return image_array, xmin, xmax, ymin, ymax

def plot_box(title):
    from image import make_image_from_xy
    from PIL import Image

    image_array = plot_dict.get(IMAGE_ARRAY)
    ymax = plot_dict.get(YMAX)
    box = plot_dict.get(title)
    print("box", box, title, ymax)
    img = make_image_from_xy(image_array, box[0], box[1], ymax - box[2], ymax - box[3])
    if debug:
        Image.fromarray(img).show()
    # save image for tesseract
    try:
        dir = os.path.join(PHYSCHEM, "temp")
        os.makedirs(dir, exist_ok=True)
        file = os.path.join(dir, title +".png")
        Image.fromarray(img).save(file)
        print("saved ", file)
#        file.close()
        osd = get_osd(file)
        print("osd", osd)
    except Exception as e:
        print ("TESSERACT ERROR ", e)
#    temp_filename, image_filename = save(img)
#    print("f ", temp_filename, image_filename)
#    textboxes = get_tesseract_textboxes(image_filename)
#    get_tesseract_textboxes(img)
#    print("tb ", textboxes)
    return img

def xscale(image):

    plot_box(BOT_AXIS_TITLE)
    plot_box(BOT_AXIS_SCALE)
    plot_box(BOT_AXIS_TICKS)
    plot_box(BOT_AXIS_LINE)

    plot_box(TOP_AXIS_LINE)

def draw_boxes_round_tesseract_chars(image, imagefile):
    print("do not use draw_boxes_round_tesseract_chars, not tested")
    return
    import cv2
    imagearray = np.array(image)
    img = imagearray
    h, w, c = imagearray.shape
    print(h, w, c)
    boxes = pytesseract.image_to_boxes(imagefile)
    print(boxes[0])
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    cv2.imshow('img', img)
