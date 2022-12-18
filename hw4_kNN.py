from sklearn import datasets
import matplotlib.pyplot as plt
import random
import math
from collections import Counter

SUBPLOT_FACTOR = 4


def draw_description(text, ax):
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height
    ax.text(0.5 * (left + right),
            0.5 * (bottom + top),
            s=text,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            fontsize=10)


def get_dimension_array(array, dim):
    return [item[dim] for item in array]


def draw_projections(data, lims, point=None):
    fig, axs = plt.subplots(SUBPLOT_FACTOR, SUBPLOT_FACTOR, figsize=(5, 5))
    fig.suptitle('Iris Data (setosa - red, versicolor - green, virginica - blue)',
                 fontsize=10,
                 fontweight='bold')
    fig.subplots_adjust(left=0.08, bottom=0.02, right=0.98, top=0.87, wspace=0.15, hspace=0.15)
    for i in range(0, SUBPLOT_FACTOR):
        for j in range(0, SUBPLOT_FACTOR):
            ax = axs[i, j]
            ax.set_xlim(lims[j])
            ax.set_ylim(lims[i])
            if i == j:
                if i == 0:
                    draw_description('Sepal Length', ax)
                elif i == 1:
                    draw_description('Sepal Width', ax)
                elif i == 2:
                    draw_description('Petal Length', ax)
                elif i == 3:
                    draw_description('Petal Width', ax)
            else:
                alpha = 1 if point is None else 0.3
                ax.scatter(get_dimension_array(data, j), get_dimension_array(data, i),
                           color=get_dimension_array(data, 4), s=1, alpha=alpha)
                if point is not None:
                    ax.scatter(point[j], point[i], color=point[4], s=5)
            if j != 0:
                ax.get_yaxis().set_visible(False)
            if i != 0:
                ax.get_xaxis().set_visible(False)
            else:
                ax.xaxis.tick_top()
    plt.show()
    plt.pause(0.3)


def get_min_max(data, index):
    min_val = min(get_dimension_array(data, index))
    max_val = max(get_dimension_array(data, index))
    return min_val, max_val


def get_bounds(data, index):
    min_val, max_val = get_min_max(data, index)
    diff = (max_val - min_val) * 0.1
    min_val = min_val - diff
    max_val = max_val + diff
    return min_val, max_val


def get_normalized_data(data):
    result = []
    min_max = [get_min_max(data, j) for j in range(4)]
    for measure in data:
        arr = []
        for j in range(len(measure) - 1):
            arr.append((measure[j] - min_max[j][0]) / (min_max[j][1] - min_max[j][0]))
        arr.append(measure[4])
        result.append(arr)
    return result


def get_data_with_color():
    iris = datasets.load_iris()
    colors = list(map(lambda x: 'red' if x == 0 else 'green' if x == 1 else 'blue', iris.target))
    result = []
    dataset = iris.data
    for i in range(len(dataset)):
        result.append([dataset[i][0], dataset[i][1], dataset[i][2], dataset[i][3], colors[i]])
    return result


def get_k(learning_data, base_data):
    temp_k = int(math.sqrt(len(base_data)) / 2)
    max_right = 0

    for i in range(int(math.sqrt(len(base_data)) / 2), 2 * int(math.sqrt(len(base_data))) + 1):
        temp_right_count = 0
        for learn_measures in learning_data:
            cluster_color = get_color_for_point(base_data, learn_measures, i)
            if cluster_color == learn_measures[4]:
                temp_right_count = temp_right_count + 1
        if temp_right_count > max_right:
            max_right = temp_right_count
            temp_k = i

    print(max_right, 'из', len(learning_data))
    print('k:', temp_k)
    return temp_k


def get_color_for_point(normalized, point, k):
    dists = [[math.dist(t[:3], point[:3]), t[4]] for t in normalized]
    dists = sorted(dists, key=lambda x: x[0])
    cluster_color = Counter(list(map(lambda x: x[1], dists[:k]))).most_common(1)[0][0]
    return cluster_color


def draw_new_point_last(normalized, k):
    point = normalized[-1]
    color = get_color_for_point(normalized, point, k)
    point[4] = color
    draw_projections(normalized, [[-0.1, 1.1] for _ in range(4)], point)


if __name__ == "__main__":
    data_with_color = get_data_with_color()
    min_sepal_length, max_sepal_length = get_bounds(data_with_color, 0)
    min_sepal_width, max_sepal_width = get_bounds(data_with_color, 1)
    min_petal_length, max_petal_length = get_bounds(data_with_color, 2)
    min_petal_width, max_petal_width = get_bounds(data_with_color, 3)

    random.shuffle(data_with_color)

    draw_projections(data_with_color,
                     [[min_sepal_length, max_sepal_length], [min_sepal_width, max_sepal_width],
                      [min_petal_length, max_petal_length], [min_petal_width, max_petal_width]])

    normalized_data = get_normalized_data(data_with_color)
    draw_projections(normalized_data, [[-0.1, 1.1] for i in range(4)])

    learning_count = 50
    normalized_base_data = normalized_data[:-learning_count]
    normalized_learning_data = normalized_data[-learning_count:]
    k = get_k(normalized_learning_data, normalized_base_data)

    stop = False
    while not stop:
        print('Введите числа SL, SW, PL, PW через пробел:')
        string = input()
        if not string:
            stop = True
        else:
            base_data_not_normalized = data_with_color.copy()
            values = [float(i) for i in string.split(' ')]
            values.append('')
            base_data_not_normalized.append(values)
            normalized_data = get_normalized_data(base_data_not_normalized)

            draw_new_point_last(normalized_data, k)

            # blue 8 3 6 2
            # red 4 4 1.5 0.5
            # green 6 2 3 1
