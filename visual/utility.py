from PIL import Image
from PIL import ImageChops
from visual import algorithm

def dict_compare(d1, d2):

    # solution from
    # http://stackoverflow.com/questions/4527942/comparing-two-dictionaries-in-python
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified, same

def union(diagram1, diagram2):

    added, removed, modified, same = dict_compare(diagram1, diagram2)
    dic_union = {}

    for key in same:
        dic_union[key] = diagram1[key]

    return dic_union

def get_similarity_metric(a, b, problem):

    if problem.problemType == '3x3':
        added, removed, modified, same = dict_compare(a, b)
        return weighted_score(same)
    else:
        added, removed, modified, same = dict_compare(a, b)
        return weighted_score(same)

def weighted_score(same):

    score = 0
    for key in same:

        score += 1

    return score

def image_union(figure1, figure2):

    image1 = Image.open(figure1.visualFilename)
    image2 = Image.open(figure2.visualFilename)
    blended = ImageChops.darker(image1, image2)

    return blended

def normalize_scores(scores, problem):

    if sum(scores) == 0 and problem.problemType == '3x3':
        out = [.125, .125, .125, .125, .125, .125, .125, .125]
    elif sum(scores) == 0 and problem.problemType == '2x2':
        out = [.16, .16, .16, .16, .16, .16]
    else:
        m_score = max(scores)
        for i, score in enumerate(scores):
            if score != m_score:
                scores[i] = 0

        t = float(sum(scores))
        out = [x / t for x in scores]

    return out

def similarity(source, compare):

    return round(algorithm.calc_rms(source, compare), 0)