import os
import string
from output_validator import validateStudentOutput


def file_to_dict(file):
    d = {}
    with open(file, 'r') as f:
        for line in f:
            if ":" not in line:
                continue
            key, distance_vect = line.split(":")
            distance_d = {}
            distances = distance_vect.split(",")
            for distance in distances:
                i = 0
                while distance[i] in string.ascii_letters:
                    i += 1
                dest, distance = distance[:i], distance[i:].strip()
                distance_d[dest] = distance
            d[key] = distance_d
    return d


def diff_two_dicts(d1, d2):
    def _diff_two_dicts(_d1, _d2, _k):
        set1 = set(_d1.items())
        set2 = set(_d2.items())
        diff = set1 ^ set2
        diff_dict = {}
        for d in diff:
            k, w = d
            if k not in diff_dict:
                diff_dict[k] = [_d1[k], _d2[k]]
                print("There is a difference MyAnswer[{}][{}] = {}, Answer[{}][{}] = {}".format(
                    _k, k, _d1[k], _k, k, _d2[k]
                ))
                return False

    for k1 in d1:
        if k1 not in d2:
            print("Error mis`sing {} from d2".format(k1))
            return False
        _diff_two_dicts(d1[k1], d2[k1], k1)
    return True

def run_validation():
    total_correct = 0
    total = 0
    for f in os.listdir('MyAnswers/'):
        if "." == f[0] or f == "BadTopo.log":
            continue
        total += 1
        print("-"*10, f, "-"*10)
        print("validating student output for format")
        correct = validateStudentOutput('MyAnswers/{}'.format(f))
        if not correct:
            print("Did not validate correctly")
            continue
        print("validating done")
        d1 = file_to_dict('MyAnswers/{}'.format(f))
        d2 = file_to_dict('Logs/{}'.format(f))
        correct = diff_two_dicts(d1, d2)
        total_correct += correct
        if not correct:
            print("Did not validate correctly")
    print("-"*25)
    print("total done", total)
    print("correct =", total_correct, "/", total)
