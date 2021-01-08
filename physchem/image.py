def create_image_with_margins(image_file):
    """https://stackoverflow.com/questions/11142851/adding-borders-to-an-image-using-python"""
    import cv2

    image = cv2.imread(image_file)
    # cv2 uses BGR, so convert
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    # color = [101, 52, 152] # 'cause purple!
    color = [255, 255, 255]

    # may need to remember these dimensions
    top_border, bottom_border, left_border, right_border = [100]*4

    img_with_border = cv2.copyMakeBorder(img_rgb, top_border, bottom_border,
                    left_border, right_border, cv2.BORDER_CONSTANT, value=color)
    return Image.fromarray(img_with_border)


from contextlib import contextmanager
@contextmanager
def save(image):
    from tempfile import NamedTemporaryFile
    """NOT YET WORKING"""
    try:
        with NamedTemporaryFile(prefix='tess_', delete=False) as f:
            if isinstance(image, str):
                yield f.name, realpath(normpath(normcase(image)))
                return

            image, extension = prepare(image)
            input_file_name = f.name + extsep + extension
            image.save(input_file_name, format=image.format)
            yield f.name, input_file_name
    finally:
        cleanup(f.name)

def make_image_from_xy(image_array, xlo, xhi, ylo, yhi):
    # NOTE X AND Y ARE REVERSED IN IMAGE ARRAY
    # and coordinates are from image bottom left
    print("new image", (xlo, xhi), (yhi, ylo))
#    return image_array[ylo:yhi, xlo:xhi]
    return image_array[yhi:ylo, xlo:xhi]
