#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# filename: sounds.py
# author: glenn abastillas
# created: 2020-04-10
# description: classes and functions to represent and manipulate phonemes
import numpy as np
from resource import SoundsResource, PhonologyResource
import math, random

PHON = PhonologyResource()
SNDS = SoundsResource()

VSF, CSF = PHON.vowel_specific_features, PHON.consonant_specific_features

KEYS = [[(b, a) for a, b in enumerate(__)] for __ in PHON.features]
KEYR = [enumerate(__) for __ in PHON.features]
ATTRIBUTES = {a: dict(b) for a, b in zip(PHON.labels, KEYS)}
ATTRIBUTER = {a: dict(b) for a, b in zip(PHON.labels, KEYR)}

def analyze_sound_probabilities():
    from nltk import ConditionalFreqDist, ConditionalProbDist, ELEProbDist
    from nltk import bigrams
    cfd = ConditionalFreqDist()
    data = [gram for __ in SNDS.consonant for gram in bigrams(__.name.split())]
    for gram in data:
        cfd[gram[0]][gram[1]] += 1
    return ConditionalProbDist(cfd, ELEProbDist)


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
        voicing : Voicing for this sound (e.g., voiceless)

    '''

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
        self.rows, self.columns = self.__get_rows_and_columns()
        self._features = np.zeros((self.rows, self.columns))

        if features:
            self._parse(*features)

        # [TO BE DEVELOPED]
        # If class instantiated with letter, match with existing SNDS resource
        if kwargs.get('letter'):
            kind, letter = kwargs.get('kind'), kwargs.get('letter')
            self._parse_letter(kind, letter)

        self._ipa = kwargs.get('ipa')
        self._character = kwargs.get('character')

        if kwargs.get('random', False):
            self.randomize(kwargs.get('kind'))

    def __repr__(self, label="Sound"):
        features = [getattr(self, __) for __ in PHON.labels]
        features = enumerate(features)

        __ = ATTRIBUTER
        features = [__[PHON.labels[i]][j] for i, j in features if j is not None]

        attributes = ', '.join(features)

        return "{}({})".format(label, attributes)

    def __add__(self, sound):
        ''' Order of addition: voiced > voiceless, stop + fricative == affricate '''

        average = lambda x, y : math.floor(0.5 * (x + y))

        is_stop = lambda x, y : x < 3 or y < 3
        is_fric = lambda x, y : x > 2 or y > 2
        both_present = lambda x, y : is_stop(x, y) and is_fric(x, y)

        voicing = min(sound.voicing, self.voicing)
        place = average(sound.place, self.place)
        manner = 3 if both_present else self.manner


        # is_stop = sound.manner in stop or self.manner in stop
        # is_fricative = sound.manner in fricative or self.manner in fricative

        # if is_stop and is_fricative:
        #     manner = 3

        # [TO BE DEVELOPED] Add code to adopt other sound attrs from current
        basic = ['voicing', 'place', 'manner']
        labels = list(filter(lambda x : x not in basic, PHON.labels))

        other_features = [(__, getattr(self, __)) for __ in labels if __ ]

        return Sound(ATTRIBUTER['voicing'][voicing],
                     ATTRIBUTER['place'][place],
                     ATTRIBUTER['manner'][manner])

    def __get_rows_and_columns(self):
        return len(PHON.features), max([len(__) for __ in PHON.features])

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
        return self._get_feature('place')

    @place.setter
    def place(self, place):
        self._set_feature('place', place)

    @property
    def manner(self):
        ''' Return this sound's manner value '''
        return self._get_feature('manner')

    @manner.setter
    def manner(self, manner):
        self._set_feature('manner', manner)

    @property
    def voicing(self):
        ''' Return this sound's voicing value '''
        return self._get_feature('voicing')

    @voicing.setter
    def voicing(self, voicing):
        self._set_feature('voicing', voicing)

    @property
    def cavity(self):
        ''' Return this sound's cavity value '''
        return self._get_feature('cavity')

    @cavity.setter
    def cavity(self, cavity):
        self._set_feature('cavity', cavity)

    @property
    def airway(self):
        ''' Return this sound's airway value '''
        return self._get_feature('airway')

    @airway.setter
    def airway(self, airway):
        self._set_feature('airway', airway)

    @property
    def sonority(self):
        ''' Return this sound's sonority value '''
        return self._get_feature('sonority')

    @sonority.setter
    def sonority(self, sonority):
        self._set_feature('sonority', sonority)

    @property
    def mode(self):
        ''' Return this sound's mode value '''
        return self._get_feature('mode')

    @mode.setter
    def mode(self, mode):
        self._set_feature('mode', mode)

    @property
    def tone(self):
        ''' Return this sound's tone value '''
        return self._get_feature('tone')

    @tone.setter
    def tone(self, tone):
        self._set_feature('tone', tone)

    @property
    def speed(self):
        ''' Return this sound's speed value '''
        return self._get_feature('speed')

    @speed.setter
    def speed(self, speed):
        self._set_feature('speed', speed)

    @property
    def frontness(self):
        ''' Return this sound's frontness value '''
        return self._get_feature('frontness')

    @frontness.setter
    def frontness(self, frontness):
        self._set_feature('frontness', frontness)

    @property
    def openness(self):
        ''' Return this sound's openness value '''
        return self._get_feature('openness')

    @openness.setter
    def openness(self, openness):
        self._set_feature('openness', openness)

    @property
    def roundness(self):
        ''' Return this sound's roundness value '''
        return self._get_feature('roundness')

    @roundness.setter
    def roundness(self, roundness):
        self._set_feature('roundness', roundness)

    def _reset_feature(self, feature=None):
        ''' Set feature matrix or specified feature values to zero 
        
        Parameters
        ----------
            feature (str) : Feature name to reset
        '''
        if feature:
            idx = self._get_feature(feature)
            self._features[idx] = np.zeros((self.columns, ))
        else:
            self._features = np.zeros((self.rows, self.columns))

    def _get_feature(self, feature):
        ''' Return the index value of a specfied feature

        Parameters
        ----------
            feature (str) : Feature name to retrieve values for

        Returns
        -------
            Integer of property if exists, else None
        '''
        idx = self._feature_to_index(feature)
        arr = self._features[idx]

        if arr.sum() == 0:
            return None
        return arr.argmax()

    def _set_feature(self, feature, value):
        '''
        Assign a feature a certain value

        Parameters
        ----------
            feature (str) : Name of feature
            value (str, int) : Feature value
        '''
        idx = self._feature_to_index(feature)
        arr = self._features[idx]

        if isinstance(value, str):
            features = PHON.features[idx]
            value = features.index(value.lower())

        if isinstance(value, int) and value < arr.shape[-1]:
            arr = np.zeros(arr.size)
            arr[value] = 1

        self._features[idx] = arr

    def _feature_to_index(self, attribute):
        '''
        Return the feature index for an attribute

        Parameters
        ----------
            attribute (str, int) : Name or index of an attribute
        '''
        if not isinstance(attribute, str):
            return int(attribute)
        return PHON.labels.index(attribute)
    
    def _value_to_index(self, values, feature):
        '''
        Return the value index for a string value and attribute

        Parameters
        ----------
            values (dict) : Mapping of feature names to indices
            feature (str, int) : Feature to index
        '''
        return list(values.keys()).index(feature)

    def _normalize(self, features):
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

    def _parse(self, *features, return_=False):
        '''
        Configure this sound's feature matrix with specified input features

        Parameters
        ----------
            features (list): Positional arguments corresponding to features
            return_ (boolean): Return features if True, else set to class attributes
        '''
        # Preprocess if feature is a single, space-separated string (e.g., 'voiced dental fricative')
        if isinstance(features, tuple) and len(features) == 1:
            features = features[0].split()

            # [TO BE DEVELOPED]
            # Parse input as a consonant letter by default
            if len(features) < 2 and len(features[0]) < 3:
                self._parse_letter('c', features[0])
        
        matrix = self._features
        if return_:
            matrix = np.zeros((self.rows, self.columns))

        for feature in self._normalize(features):
            for feature_, values in ATTRIBUTES.items():
                feature_match = feature in values

                if feature_match:
                    __f = self.encode(feature_)
                    __v = self.encode(feature_, feature)

                    matrix[__f][__v] = 1
                    break
        
        if return_:
            return matrix

    def _parse_letter(self, character):
        '''
        Set this sounds properties from the phonology file's set of sounds.

        Parameters
        ----------
            # kind (str) : Whether or not the character is a vowel or consonant
            character (str) : Sound defined in phonology.yaml
        '''
        current = SNDS.character(character)[0]

        if current:
            self._parse(*current.name.split())
        
        else:
            readme = 'https://github.com/gabastil/conlang'
            message = (
                f'Character not found and properties not set.\n'
                f'For a full set of available characters, please reference {readme} '
                f'or the sounds.yaml resource file.'
            )

            raise Warning(message)

        return None

    def _get_index_array(self, feature):
        ''' Return an index and array associated with this feature '''
        idx = self.encode(feature)
        return idx, self._features[idx]

    def _get_argmax_array(self, idx, array, direction):
        '''
        Return the argmax for the input array and a zero array. Used for mutat-
        ing the properties of this Sound's sound matrix.

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
        maxlength = len(PHON.features[idx])
        if argmax >= maxlength:
            argmax = maxlength - 1
        elif argmax < 0:
            argmax = 0
        return argmax, array

    def _update_feature(self, idx, argmax, array):
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
        index = self._feature_to_index(feature)
        if value:
            return PHON.features[index].index(value)
        return index

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
            features = PHON.features[feature]
            return features[value]
        return PHON.labels[feature]

    def weaken(self, feature):
        '''
        Weaken the specified feature by moving the feature away from zero.

        Parameters
        ----------
            feature (str) : Name of feature to weaken
        '''
        idx, array = self._get_index_array(feature)
        argmax, array = self._get_argmax_array(idx, array, 1)
        self._update_feature(idx, argmax, array)

    def strengthen(self, feature):
        '''
        Strengthen the specified feature by move the feature closer to zero.

        Parameters
        ----------
            feature (str) : Name of feature to weaken
        '''
        idx, array = self._get_index_array(feature)
        argmax, array = self._get_argmax_array(idx, array, -1)
        self._update_feature(idx, argmax, array)

    def randomize(self, kind='c', data=None):
        '''
        Generate a random configuration of settings 
        
        Parameters
        ----------
            kind (str) : c for consonant or v for vowel
            data (str) : path to distribution data for phonemes
        
        Notes
        -----
            Default probability distribution is uniform, which is unrealistic.

            Use phonetic data (e.g., counts.pkl) to derive probabilities.

            Will need to process all sounds from all languages to get probabilities for each feature.
        '''

        def voicing():
            raise NotImplementedError()
            

        ignore = random.choice([VSF, CSF])

        if isinstance(kind, str):
            if kind.startswith('v'):
                ignore = CSF

            elif kind.startswith('c'):
                ignore = VSF

        for i, feature in enumerate(PHON.labels[:-1]):
            if feature not in ignore:
                value = random.choice(PHON.features[i])
                self._set_feature(feature, value)
        
        self._set_feature('airway', 'egressive')
    
    def orthography(self, kind='c'):
        ''' 
        Return an orthographical representation of this sound. 
        
        Parameters
        ----------
            kind (str) : c for consonant or v for vowel
        '''

        attr = [self.encode(__) for __ in CSF]

        if kind.lower().startswith('v'):
            *__, [attr] = [self.encode(__) for __ in VSF]
        
        this = self._features[attr]

        for consonant in SNDS.consonant:
            features = self._parse(consonant.name, return_=True)[attr]

            if (this == features).all():
                return consonant.character
        else:
            return ' '


class Consonant(Sound):

    def __init__(self, *features, **kwargs):
        super().__init__(*features, **kwargs, kind='c')

        if not features and not kwargs:
            self.__default()

    def __repr__(self):
        return super().__repr__('Consonant')
    
    def __eq__(self, sound):
        return (self.place == sound.place and
                self.manner == sound.manner and
                self.voicing == sound.voicing)

    def __default(self):
        ''' Set the default basic properties of a consonant if none exist '''
        default = 'fast oral egressive voiced alveolar stop'.split()
        labels = ['speed', 'cavity', 'airway', 'voicing', 'place', 'manner']

        for i, attr in enumerate(labels):
            current = getattr(self, attr)

            if current is None:
                setattr(self, attr, default[i])

    @property
    def type(self):
        ''' Return Sound type of consonant '''
        return 'C'

    def set(self, *features, **kwargs):
        self.__init__(*features, **kwargs)

    def weaken(self, intensify=False):
        '''
        Weaken this consonant like when a consonant undergoes lenition

        Notes
        -----
            Features changes:

            Place: Front -> Back
            Manner: Stop -> Fricative
            Voicing: Voiced -> Unvoiced
        '''
        if self.voicing == 0:
            super().weaken('voicing')
        elif self.manner < 2 or intensify:
            super().weaken('manner')
        else:
            super().weaken('place')

        self.__default()

    def strengthen(self, intensify=False):
        '''
        Strengthen this consonant like when a consonant undergoes lenition

        Notes
        -----
            Features changes:

            Place: Back -> Front
            Manner: Fricative -> Stop
            Voicing: Unvoiced -> Voiced
        '''
        if self.voicing > 0:
            super().strengthen('voicing')
        elif self.manner > 0 or intensify:
            super().strengthen('manner')
        else:
            super().strengthen('place')

        self.__default()


class Vowel(Sound):

    def __init__(self, *features, **kwargs):
        super().__init__('voiced', *features, **kwargs)
        self.__default()

    def __repr__(self):
        return super().__repr__('Vowel')
    
    def __eq__(self, sound):
        return (self.tone == sound.tone and
                self.mode == sound.mode and
                self.frontness == sound.frontness and
                self.openness == sound.openness and
                self.roundness == sound.roundness)

    def __default(self):
        default = 'medium oral egressive open voiced mid unrounded'.split()
        labels = ['speed', 'cavity', 'airway',
                  'openness', 'voicing', 'frontness', 'roundness']

        for i, attr in enumerate(labels):
            current = getattr(self, attr)

            if current is None:
                setattr(self, attr, default[i])


    @property
    def type(self):
        return 'V'

    def set(self, *features, **kwargs):
        self.__init__(*features, **kwargs)



if __name__ == '__main__':
    c = Sound('sh')
    print(c)

    k = Consonant('k')
    print(k)
    print(c + k)

    ll = Consonant('z')
    m = Consonant('s')
    print(ll, m)
    print(ll.manner, m.manner)
    print(ll + m)
    # cons = Consonant('velar', 'voiceless', 'fricative', character='kh')
    # print(cons)
    # cons.strengthen()
    # print(cons)
    # cons.strengthen()
    # print(cons)
    # cons.strengthen()
    # print(cons)
    # cons.weaken()
    # print(cons)
    # cons.weaken()
    # print(cons)
    # cons.weaken()
    # print(cons)
    # cons.weaken()
    # print(cons)
    # print(Phonology().orthography)

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