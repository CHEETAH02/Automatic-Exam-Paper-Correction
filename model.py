import numpy as np
from numpy.linalg import norm
from autocorrect import Speller
from expression_trial import express_trialdef
import requests


def evaluateMCQ(studentAnswer, referenceAnswer, marksWeight):
    total = []

    for i in range(len(studentAnswer)):
        if studentAnswer[i] == referenceAnswer[i]:
            total.append(marksWeight)
        else:
            total.append(0)

    return total


def evaluateFillBlanks(studentAnswer, referenceAnswer, marksWeight):
    spell = Speller(lang="en", only_replacements=True)
    total = []

    for i in range(len(studentAnswer)):
        if spell(studentAnswer[i]) == spell(referenceAnswer[i]):
            total.append(marksWeight)
        else:
            total.append(0)

    return total


def evaluateEquations(studentAnswer, referenceAnswer, marksWeight, questions):
    total = []

    for i in range(len(studentAnswer)):
        lines = studentAnswer[i].split("\n")
        length = len(lines)
        temp = express_trialdef(
            lines[length - 1], referenceAnswer[i], questions[i])
        temp = int(np.round(temp / 5 * marksWeight))
        total.append(temp)

    return total


def evaluateBrief(studentAnswer, referenceAnswer, marksWeight):
    total = []

    url = "http://127.0.0.1:8080/sentences"
    data = {"s1": studentAnswer, "s2": referenceAnswer}
    response = requests.post(url, json=data).json()
    sentence_vector_1 = response['sentence_vector_1']
    sentence_vector_2 = response['sentence_vector_2']

    for i in range(len(sentence_vector_1)):
        similarity = get_cosine_similarity(
            sentence_vector_1[i], sentence_vector_2[i])
        marks = max(
            0, min(np.round(similarity * (1 / 0.80 * marksWeight)), marksWeight))
        total.append(marks)

    return total


def get_cosine_similarity(sentence_embedding1, sentence_embedding2):
    cosine_similarity = np.dot(sentence_embedding1, sentence_embedding2) / \
        (norm(sentence_embedding1) * norm(sentence_embedding2))
    return cosine_similarity
