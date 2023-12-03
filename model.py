import tensorflow_hub as hub
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
import numpy as np
from numpy.linalg import norm
from autocorrect import Speller

def evaluateMCQ(studentAnswer, referenceAnswer, marksWeight):
    total = []

    for i in range(len(studentAnswer)):
        print(studentAnswer[i], referenceAnswer[i])
        if studentAnswer[i] == referenceAnswer[i]:
            total.append(marksWeight[i])
        else:
            total.append(0)

    return total

def evaluateFillBlanks(studentAnswer, referenceAnswer, marksWeight):
    spell = Speller(lang='en')
    total = []

    for i in range(len(studentAnswer)):
        print(spell(studentAnswer[i]), spell(referenceAnswer[i]))
        if spell(studentAnswer[i]) == spell(referenceAnswer[i]):
            total.append(marksWeight[i])
        else:
            total.append(0)

    return total

def evaluateBrief(studentAnswer, referenceAnswer, marksWeight):
    total = []
    sentence_vector_1 = embed(studentAnswer)
    sentence_vector_2 = embed(referenceAnswer)

    for i in range(len(studentAnswer)):
        similarity = get_cosine_similarity(sentence_vector_1[i], sentence_vector_2[i])
        print(max(0, min(np.round(similarity * (1 / 0.80 * marksWeight[i])), marksWeight[i])))
        marks = max(0, min(np.round(similarity * (1 / 0.80 * marksWeight[i])), marksWeight[i]))
        total.append(marks)

    return total

def get_cosine_similarity(sentence_embedding1, sentence_embedding2):
    cosine_similarity = np.dot(sentence_embedding1, sentence_embedding2) / (norm(sentence_embedding1) * norm(sentence_embedding2))
    return cosine_similarity