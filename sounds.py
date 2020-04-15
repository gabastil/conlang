#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# filename: sounds.py
# author: glenn abastillas
# created: 2020-04-10
# description: classes and functions to represent and manipulate phonemes
import numpy as np

# --- Base features used by the Sound class and its descendents ---

# Direction of airflow to produce this sound
AIRWAY = ['ingressive',
          'egressive']

# Part of the airway that air travels through
CAVITY = ['nasal',
          'oral']

# Points of articulation in the oral cavity
PLACE = ['bilabial',
         'labiodental',
         'dental',
         'alveolar',
         'postalveolar',
         'retroflex',
         'palatal',
         'velar',
         'uvular',
         'pharyngeal',
         'glottal']

# Technique used to restrict airflow during articulation
MANNER = ['stop',
          'fricative',
          'approximant',
          'affricate',
          'lateral']

# Usage of vocal chords to produce sound
VOICING = ['unvoiced',
           'voiced']

# Phonemic pitch used with sound
TONE = ['high',
        'mid-high',
        'mid',
        'low-mid',
        'low']

# Supravocal properties like creakiness or breathiness
MODE = ['creaky',
        'breathy']

# Duration of sound during production
TIME = ['fast',
        'medium',
        'slow']

# Tongue placement in the oral cavity
FRONTNESS = ['front',
             'mid',
             'back']

# How open the mouth is
OPENESS = ['open',
           'mid-open',
           'mid',
           'mid-close',
           'close']

# Lip rounding
ROUNDNESS = ['rounded',
             'unrounded']

# Narrow descriptions of sonority of a sound
SONORITY = ['vowel',
            'liquid',
            'nasal',
            'fricative',
            'affricate',
            'voiced-stop',
            'unvoiced-stop']

FEATURE_LABELS = ['place',
                  'manner',
                  'voicing',
                  'tone',
                  'mode',
                  'time',
                  'cavity',
                  'airway',
                  'frontness',
                  'openess',
                  'roundness'
                  'sonority']

FEATURE_ARRAY = [PLACE,
                 MANNER,
                 VOICING,
                 TONE,
                 MODE,
                 TIME,
                 CAVITY,
                 AIRWAY,
                 FRONTNESS,
                 OPENESS,
                 ROUNDNESS,
                 SONORITY]


class Sound(object):
    '''

    The Sound class contains properties and auxiliary functions for encoding
    and decoding sound properties like articulation (manner, place, voicing)
    and airway types (e.g., pulmonic). This class serves as the parent class
    for the Consonant and Vowel classes.

    Attributes
    ----------
        ipa : International Phonetic Alphabet (IPA) symbol as unicode
        phoneme : Simple representation of this with ASCII characters
        airway : How air moves to make this sound
        cavity : Oral or nasal sounds
        sonority : How 'open' or sonorous a sound is
        place : Place of articulation for this sound (e.g., bilabial)
        manner : Manner of articulation for this sound (e.g., fricative)
        voicing : Voicing for this sound (e.g., unvoiced)

    '''
    STR_KEYS = [[(b, a) for a, b in enumerate(__)] for __ in FEATURE_ARRAY]
    ATTRIBUTES = {a: dict(b) for a, b in zip(FEATURE_LABELS, STR_KEYS)}

    def __init__(self, *features, **kwargs):
        """
        Initialize this sound class with positional arguments describing the
        sound and any orthographical elements as keyword arguments.

        Parameters
        ----------
            features (list) : Positional arguments for sound features.
            kwargs (dict) : Keyword arguments for orthographical elements.

        Notes
        -----
            Features
                Include values related to:
                    1. Place of articulation
                    2. Manner of articulation
                    3. Voicing
                    4. Cavity
                    5. Airway
                    6. Sonority (low fidelity)
                    7. Sonority (high fidelity)

            Kwargs
                Include orthographical values like: IPA character and phoneme

        """
        self.rows = len(FEATURE_ARRAY)
        self.columns = max([len(__) for __ in FEATURE_ARRAY])

        self._features = np.zeros((self.rows, self.columns))

        if features:
            self.__parse_features(*features)

        self._ipa = kwargs.get('ipa')
        self._phoneme = kwargs.get('phoneme')

    @property
    def ipa(self):
        ''' Return this sound's ipa value '''
        return self._ipa

    @ipa.setter
    def ipa(self, ipa):
        self._ipa = ipa

    @property
    def phoneme(self):
        ''' Return this sound's phoneme value '''
        return self._phoneme

    @phoneme.setter
    def phoneme(self, phoneme):
        self._phoneme = phoneme

    @property
    def place(self):
        ''' Return this sound's place value '''
        return self.__get_feature('place')

    @place.setter
    def place(self, place):
        self.__set_feature('place', place)

    @property
    def manner(self):
        ''' Return this sound's manner value '''
        return self.__get_feature('manner')

    @manner.setter
    def manner(self, manner):
        self.__set_feature('manner', manner)

    @property
    def voicing(self):
        ''' Return this sound's voicing value '''
        return self.__get_feature('voicing')

    @voicing.setter
    def voicing(self, voicing):
        self.__set_feature('voicing', voicing)

    @property
    def cavity(self):
        ''' Return this sound's cavity value '''
        return self.__get_feature('cavity')

    @cavity.setter
    def cavity(self, cavity):
        self.__set_feature('cavity', cavity)

    @property
    def airway(self):
        ''' Return this sound's airway value '''
        return self.__get_feature('airway')

    @airway.setter
    def airway(self, airway):
        self.__set_feature('airway', airway)

    @property
    def sonority(self):
        ''' Return this sound's sonority value '''
        return self.__get_feature('sonority')

    @sonority.setter
    def sonority(self, sonority):
        self.__set_feature('sonority', sonority)

    def __get_feature(self, feature):
        '''
        Return the index value of a specfied feature

        Parameters
        ----------
            feature (str) : Feature name to retrieve values for

        Returns
        -------
            Integer of property if exists, else None
        '''
        idx = self.__feature_index(feature)
        arr = self._features[idx]

        if arr.sum() == 0:
            return None
        return arr.argmax()

    def __set_feature(self, feature, value):
        '''
        Assign a feature a certain value

        Parameters
        ----------
            feature (str) : Name of feature to set
            value (str, int) : Feature value to set
        '''
        idx = self.__feature_index(feature)
        arr = self._features[idx]

        if isinstance(value, str):
            features = FEATURE_ARRAY[idx]
            value = features.index(value.lower())

        if isinstance(value, int) and value < arr.shape[-1]:
            arr = np.zeros(arr.size)
            arr[value] = 1

        self._features[idx] = arr

    def __feature_index(self, attribute):
        '''
        Return the feature index for an attribute

        Parameters
        ----------
            attribute (str, int) : Name or index of an attribute
        '''

        if not isinstance(attribute, str):
            return int(attribute)
        return FEATURE_LABELS.index(attribute)

    def __normalize_features(self, features):
        '''
        [TO BE DEVELOPED]
        Create regular expressions to identify variations of similar
        feature names

        Parameters
        ----------
            features (list) : List of features for normalization

        Notes
        -----
            Currently, this function just returns the current list of features
        '''
        return features

    def __parse_features(self, *features):
        '''
        Configure this sound's feature matrix with specified input features

        Parameters
        ----------
            features (list): Positional arguments corresponding to features
        '''
        if isinstance(features, tuple) and len(features) == 1:
            features = features[0].split()

        features = self.__normalize_features(features)

        for feature in features:
            for feature_, values in self.ATTRIBUTES.items():
                feature_match = feature in values

                if feature_match:
                    feature_index = self.__feature_index(feature_)
                    value_index = list(values.keys()).index(feature)

                    self._features[feature_index][value_index] = 1
                    break

    def encode(self, feature, value=None):
        '''
        Convert a string to its corresponding integer value. If value is indic-
        ated, return that encoding. Otherwise, return feature's high-level
        encoding.

        Parameters
        ----------
            feature (str) : High-level feature name (e.g., place, manner)
            value (str) : feature value (e.g., for place, dental)

        Notes
        -----
            If no value is supplied, the feature name will be encoded.
        '''
        idx = self.__feature_index(feature)
        if value:
            return FEATURE_ARRAY[idx].index(value)
        return idx

    def decode(self, feature, value=None):
        '''
        Convert an integer to its corresponding string value. If value is
        indicated, return that decoding. Otherwise, return feature's high-level
        decoding.

        Parameters
        ----------
            feature (str) : High-level feature name (e.g., place, manner)
            value (str) : feature value (e.g., for place, dental)

        Notes
        -----
            If no value is supplied, the feature name will be decoded.
        '''
        if value:
            features = FEATURE_ARRAY[feature]
            return features[value]
        return FEATURE_LABELS[feature]


class Consonant(Sound):

    def __init__(self):
        super().__init__('voiceless stop')

    @property
    def type(self):
        return 'C'


class Vowel(Sound):


    def __init__(self):
        super().__init__('voiced')

    @property
    def type(self):
        return 'V'


class Syllable(Sound):

    def __init__(self):
        pass


if __name__ == '__main__':
    s = Sound()
    # print(s.ATTRIBUTES)
    # print(s[1])
    # print(s['voicing'])
    s.manner = 'affricate'
    s.place = 2
    print(s.manner)
    print(s.place)
    # print(s[1][s.manner])
    print(s.encode('manner'))
    print(s.decode(1))

    q = Sound('voiced alveolar stop')
    p = Sound('voiced', 'glottal', 'stop')
    print(q._features)
    print(p._features)
    print(p._features.shape)

    print(p.place)
    p.place = 'dental'
    print(p.place)
    p.place = 8

    print(p.manner)
    print(p.voicing)
    print(p.place)

    print(p.encode('manner', 'fricative'))
    print(p.encode('airway'))
    print(p.decode(3, 1))
    print(p.decode(2))