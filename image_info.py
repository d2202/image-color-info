import numpy as np
from matplotlib import colors
from scipy.spatial import cKDTree as KDTree
from PIL import Image


def make_colors_list():
    use_colors = colors.cnames
    # translate hexstring to RGB tuple
    named_colors = {k: tuple(map(int, (v[1:3], v[3:5], v[5:7]), 3*(16,)))
                    for k, v in use_colors.items()}
    ncol = len(named_colors)
    no_match = named_colors['purple']

    # make an array containing the RGB values
    color_tuples = list(named_colors.values())
    color_tuples.append(no_match)
    color_tuples = np.array(color_tuples)

    color_names = list(named_colors)
    color_names.append('no match')
    return color_names, color_tuples


def open_picture():
    # get example picture
    # TODO: открыть картинку из поля формы.
    racoon = Image.open("coon.jpeg")
    img = np.asarray(racoon)


def build_colors_dict(color_names, color_tuples, img):
    # build tree
    tree = KDTree(color_tuples[:-1])
    # tolerance for color match `inf` means use best match no matter how
    # bad it may be
    tolerance = np.inf
    # find closest color in tree for each pixel in picture
    dist, idx = tree.query(img, distance_upper_bound=tolerance)
    # count and reattach names
    counts = dict(zip(color_names, np.bincount(idx.ravel(), None, ncol+1)))
    # sort dict by highest value
    sorted_counts = {key: value for key, value in sorted(counts.items(), key=lambda item: item[1], reverse=True)}
    return sorted_counts


def make_top_10_colors_list(colors):
    top_10 = []
    # get top 10 most common colors in image
    keys = list(colors.keys())
    for i in range(10):
        key = keys[i]
        value = colors[key]
        item = {
            "color": key,
            "appears": value
        }
        top_10.append(item)
    return top_10

# Опционально поиграем с процентиками
# print(top_10)
# all_pixels = 0
# for value in sorted_counts.values():
#     all_pixels += value
# print(all_pixels)
#
# for item in top_10:
#     percent = round(item.get('appears') / all_pixels * 100, 2)
#     print(f"{item.get('color')}, {item.get('appears')} ~ {percent}%")
