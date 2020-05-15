from functools import reduce
from collections import defaultdict


def generate_codebook(data, size_codebook, epsilon=0.00001):
    data_size = len(data)

    codebook = []

    c0 = avg_vec_of_vecs(data)
    codebook.append(c0)

    avg_dist = avg_distortion_c0(c0, data, data_size)

    while len(codebook) < size_codebook:
        codebook, avg_dist = split_codebook(data, codebook, epsilon, avg_dist)

    return codebook


def split_codebook(data, codebook, epsilon, initial_avg_dist):
    data_size = len(data)

    new_codevectors = []
    for c in codebook:
        c1 = new_codevector(c, epsilon)
        c2 = new_codevector(c, -epsilon)
        new_codevectors.extend((c1, c2))

    codebook = new_codevectors
    len_codebook = len(codebook)

    print("Splitting", len_codebook)

    avg_dist = 0
    err = epsilon + 1
    num_iter = 0
    while err > epsilon:
        closest_c_list = [None] * data_size
        vecs_near_c = defaultdict(list)
        vec_idxs_near_c = defaultdict(list)
        for i, vec in enumerate(data):
            min_dist = None
            closest_c_index = None
            for i_c, c in enumerate(codebook):
                d = euclid_squared(vec, c)
                if min_dist is None or d < min_dist:
                    min_dist = d
                    closest_c_list[i] = c
                    closest_c_index = i_c
            vecs_near_c[closest_c_index].append(vec)
            vec_idxs_near_c[closest_c_index].append(i)

        for i_c in range(len_codebook):
            vecs = vecs_near_c.get(i_c) or []
            num_vecs_near_c = len(vecs)
            if num_vecs_near_c > 0:
                new_c = avg_vec_of_vecs(vecs)
                codebook[i_c] = new_c
                for i in vec_idxs_near_c[i_c]:
                    closest_c_list[i] = new_c

        prev_avg_dist = avg_dist if avg_dist > 0 else initial_avg_dist
        avg_dist = avg_distortion_c_list(closest_c_list, data, data_size)

        err = (prev_avg_dist - avg_dist) / prev_avg_dist

        num_iter += 1

    return codebook, avg_dist


def avg_vec_of_vecs(vecs):
    size = len(vecs)
    avg_vec = [0.0] * 3
    for vec in vecs:
        for i, x in enumerate(vec):
            avg_vec[i] += x / size

    return avg_vec


def new_codevector(c, e):
    return [x * (1.0 + e) for x in c]


def avg_distortion_c0(c0, data, size):
    return reduce(
        lambda s, d: s + d / size, (euclid_squared(c0, vec) for vec in data), 0.0
    )


def avg_distortion_c_list(c_list, data, size):
    return reduce(
        lambda s, d: s + d / size,
        (euclid_squared(c_i, data[i]) for i, c_i in enumerate(c_list)),
        0.0,
    )


def euclid_squared(a, b):
    return sum((x_a - x_b) ** 2 for x_a, x_b in zip(a, b))
