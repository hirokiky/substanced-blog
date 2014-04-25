""" A module to provide feature extraction.
"""
from substanced.util import get_current_registry

from igo.tagger import Tagger


def get_features(text):
    """ Getting features (list of string) from text.
    """
    return []


def get_english_features(text):
    return list(filter(lambda term: len(term) >= 4, text.split()))


def get_japanese_features(text):
    feature_terms = [
        u"名詞",
        u"動詞",
        u"形容詞",
        u"形容動詞",
    ]
    ipadic = get_current_registry().settings['blog.ipadic']
    tagger = Tagger(ipadic)

    features = []
    for m in tagger.parse(text):
        if m.feature.split(',')[0] in feature_terms:
            features.append(m.surface)
    return features
