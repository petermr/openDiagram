import numpy as np

def make_rgb_vector():
    R = .692
    G = .582
    B = .140

    # why fourth power?
    vector = [R, G, B]
    vector = vector / vector.sum()
    vector = np.pow(vector, 4)
    return vector


def save_rgb_as_uint8_file(imgIn, fileout):
    vector = make_rgb_vector()
    imgOut = imgIn * vector
    io.imsave(
        fileout,
        imgOut.astype(np.uint8))


def more_uint8_stuff(img):
    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # make color channels
    red = gray.copy()
    green = gray.copy()
    blue = gray.copy()

    # set weights
    R = .642
    G = .532
    B = .44

    # get sum of weights and normalize them by the sum

    sum = R ** 4 + G ** 4 + B ** 4
    R = R / sum
    G = G / sum
    B = B / sum
    print(R, G, B)

    # combine channels with weights
    red = (R * red)
    green = (G * green)
    blue = (B * blue)
    result = cv2.merge([red, green, blue])

    # scale by ratio of 255/max to increase to fully dynamic range
    max = np.amax(result)
    result = ((255 / max) * result).clip(0, 255).astype(np.uint8)

    # write result to disk
    cv2.imwrite("car_colored.png", result)

    # display it
    cv2.imshow("RESULT", result)
    cv2.waitKey(0)

# ====
