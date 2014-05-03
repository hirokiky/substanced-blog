""" A module to provide feature extraction.
"""
from guess_language import guessLanguage
from igo.tagger import Tagger

from substanced.util import get_current_registry


def get_features(text):
    """ Getting features (lpist of string) from text.
    """
    mapping = {
        'ja': get_japanese_features,
        'zh': get_japanese_features,  # guess_language sometimes mis-recognises ja as zh.
    }
    return mapping.get(guessLanguage(text), get_english_features)(text)


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
