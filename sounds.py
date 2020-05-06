#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# filename: sounds.py
# author: glenn abastillas
# created: 2020-04-10
# description: classes and functions to represent and manipulate phonemes
import numpy as np
import yaml

# Implement loading data via yaml

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
          'affricate',
          'fricative',
          'approximant',
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
OPENNESS = ['open',
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
                  'openness',
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
                 OPENNESS,
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
        self._character = kwargs.get('character')

    @property
    def ipa(self):
        ''' Return this sound's ipa value '''
        return self._ipa

    @ipa.setter
    def ipa(self, ipa):
        self._ipa = ipa

    @property
    def character(self):
        ''' Return this sound's character value '''
        return self._character

    @character.setter
    def character(self, character):
        self._character = character

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

    def __get_index_array(self, feature):
        ''' Return an index and array associated with this feature '''
        idx = self.encode(feature)
        return idx, self._features[idx]

    def __get_argmax_array(self, idx, array, direction):
        '''
        Return the argmax for the input array and a zero array

        Parameters
        ----------
            idx (int) : Feature index
            array (np.array) : feature array
            direction (int) : Positive (weaken) or negative (strengthen) one.

        Returns
        -------
            Tuple containing the new position and an empty array.
        '''
        argmax, array = array.argmax() + direction, np.zeros(array.size)
        maxlength = len(FEATURE_ARRAY[idx])
        if argmax >= maxlength:
            argmax = maxlength - 1
        elif argmax < 0:
            argmax = 0
        return argmax, array

    def __update_feature(self, idx, argmax, array):
        '''
        Update the specified features array with an argmax

        Parameters
        ----------
            idx (int) : Feature index
            argmax (int) : New feature to set
            array (np.array) : Array of feature values
        '''
        array[argmax] = 1
        self._features[idx] = array

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

    def weaken(self, feature):
        '''
        Weaken the specified feature by moving the feature away from zero.

        Parameters
        ----------
            feature (str) : Name of feature to weaken
        '''
        idx, array = self.__get_index_array(feature)
        argmax, array = self.__get_argmax_array(idx, array, 1)
        self.__update_feature(idx, argmax, array)

    def strengthen(self, feature):
        '''
        Strengthen the specified feature by move the feature closer to zero.

        Parameters
        ----------
            feature (str) : Name of feature to weaken
        '''
        idx, array = self.__get_index_array(feature)
        argmax, array = self.__get_argmax_array(idx, array, -1)
        self.__update_feature(idx, argmax, array)


class Consonant(Sound):

    def __init__(self, *features, **kwargs):
        super().__init__('unvoiced stop', *features, **kwargs)

    def __repr__(self):
        voicing = VOICING[self.voicing] if self.voicing is not None else None
        place = PLACE[self.place] if self.place is not None else None
        manner = MANNER[self.manner] if self.manner is not None else None

        description = ''

        for feature in [voicing, place, manner]:
            if feature:
                description += f' {feature}'

        if self.character:
            description += f" written as '{self.character}'"

        return description.strip()

    @property
    def type(self):
        ''' Return Sound type of consonant '''
        return 'C'

    def weaken(self):
        '''
        Weaken this consonant like when a consonant undergoes lenition

        Notes
        -----
            Features changes:

            Place: Front -> Back
            Manner: Stop -> Fricative
            Voicing: Voiced -> Unvoiced
        '''
        if self.voicing:
            super().weaken('voicing')
        else:
            super().weaken('manner')

    def strengthen(self):
        '''
        Strengthen this consonant like when a consonant undergoes lenition

        Notes
        -----
            Features changes:

            Place: Back -> Front
            Manner: Fricative -> Stop
            Voicing: Unvoiced -> Voiced
        '''
        if self.voicing:
            super().strengthen('voicing')
        else:
            super().strengthen('manner')


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
    cons = Consonant(character='kh')
    print(cons)
    cons.strengthen()
    cons.strengthen()
    cons.strengthen()
    cons.strengthen()
    print(cons)
    cons.weaken()
    print(cons)
    cons.weaken()
    print(cons)

    # s = Sound()
    # # print(s.ATTRIBUTES)
    # # print(s[1])
    # # print(s['voicing'])
    # s.manner = 'affricate'
    # s.place = 2
    # print(s.manner)
    # print(s.place)
    # # print(s[1][s.manner])
    # print(s.encode('manner'))
    # print(s.decode(1))

    # q = Sound('voiced alveolar stop')
    # p = Sound('voiced', 'glottal', 'stop')
    # print(q._features)
    # print(p._features)
    # print(p._features.shape)

    # print(p.place)
    # p.place = 'dental'
    # print(p.place)
    # p.place = 8

    # print(p.manner)
    # print(p.voicing)
    # print(p.place)

    # print(p.encode('manner', 'fricative'))
    # print(p.encode('airway'))
    # print(p.decode(3, 1))
    # print(p.decode(2))