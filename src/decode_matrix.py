from PIL import Image
from matplotlib import pyplot as plot


def decode_matrix(width):
    light = f"{width}.light.cp"
    original = f"{width}.original.cp"
    image_light = Image.open(light)
    image_original = Image.open(original)
    decode_matrix1 = []
    for j in range(width):
        for i in range(width):
            c1 = image_light.getpixel((i, j))
            c2 = image_original.getpixel((i, j))
            d = c2 / c1
            if d > 1.:
                decode_matrix1.append(d)
            elif d != 0.:
                decode_matrix1.append(1 / d)
            else:
                decode_matrix1.append(0)
    return decode_matrix1
    # plt.plot(decode_matrix1)
    # plt.show()
    # sys.exit()
