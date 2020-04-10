#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# filename: sounds.py
# author: glenn abastillas
# created: 2020-04-10
# description: classes and functions to represent and manipulate phonemes


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
        route : Oral or nasal sounds
        sonority : How 'open' or sonorous a sound is
        place : Place of articulation for this sound (e.g., bilabial)
        manner : Manner of articulation for this sound (e.g., fricative)
        voicing : Voicing for this sound (e.g., unvoiced)

    '''

    _AIRWAY = 'ingressive egressive'.split()
    _ROUTE = 'nasal oral'.split()
    _VOICING = 'unvoiced voiced'.split()
    _MANNER = 'stop fricative approximant affricate lateral'.split()
    _PLACE = ('bilabial labiodental dental alveolar ' +
              'postalveolar retroflex palatal velar glottal').split()

    SONORITY_HIGH_LEVEL = 'vowel sonorant obstruent'.split()
    SONORITY_LOW_LEVEL = ('vowel liquid nasal fricative ' +
                          'affricate voiced-stop unvoiced-stop').split()

    _ATTRIBUTE_LABELS = 'place manner voicing route airway'.split()
    _ATTRIBUTE_ARRAY = [_PLACE, _MANNER, _VOICING, _ROUTE, _AIRWAY]

    _INT_KEYS = [[(a, b) for a, b in enumerate(_)] for _ in _ATTRIBUTE_ARRAY]
    _STR_KEYS = [[(b, a) for a, b in enumerate(_)] for _ in _ATTRIBUTE_ARRAY]

    _ATTRIBUTES = {a: dict(b) for a, b in zip(_ATTRIBUTE_LABELS, _INT_KEYS)}
    _ATTRIBUTESR = {a: dict(b) for a, b in zip(_ATTRIBUTE_LABELS, _STR_KEYS)}

    def __init__(self):
        pass

    def __getitem__(self, i):
        '''
        Return the mapping dictionarys {int : str} or {str : int} for the
        articulation type i

        Parameters
        ----------
            i (str, int) : articulation type to return the dictionary for

        Returns
        -------
            Mapping for encoding or decoding an articulation type as a dict.
        '''
        is_string, is_int = isinstance(i, str), isinstance(i, int)

        if not (is_string or is_int):
            raise ValueError('Indices must be strings or integers')

        if is_string:
            i = i.lower()
            attributes = self._ATTRIBUTESR
        else:
            i = self._ATTRIBUTE_LABELS[i]
            attributes = self._ATTRIBUTES
        return attributes[i]

    @property
    def ipa(self):
        return self._ipa

    @ipa.setter
    def ipa(self, ipa):
        self._ipa = ipa

    @property
    def phoneme(self):
        return self._phoneme

    @phoneme.setter
    def phoneme(self, phoneme):
        self._phoneme = phoneme

    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, route):
        if isinstance(route, int) and route < len(self._ROUTE):
            self._route = route
        elif isinstance(route, str):
            self._route = self._ROUTE.index(route.lower())

    @property
    def airway(self):
        return self._airway

    @airway.setter
    def airway(self, airway):
        if isinstance(airway, int) and airway < len(self._AIRWAY):
            self._airway = airway
        elif isinstance(airway, str):
            self._airway = self._AIRWAY.index(airway.lower())

    @property
    def sonority(self):
        return self._sonority

    @sonority.setter
    def sonority(self, sonority):
        if isinstance(sonority, int) and sonority < len(self._SONORITY):
            self._sonority = sonority
        elif isinstance(sonority, str):
            self._sonority = self._SONORITY.index(sonority.lower())

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, place):
        if isinstance(place, int) and place < len(self._PLACE):
            self._place = place
        elif isinstance(place, str):
            self._place = self._PLACE.index(place.lower())

    @property
    def manner(self):
        return self._manner

    @manner.setter
    def manner(self, manner):
        if isinstance(manner, int) and manner < len(self._MANNER):
            self._manner = manner
        elif isinstance(manner, str):
            self._manner = self._MANNER.index(manner.lower())

    @property
    def voicing(self):
        return self._voicing

    @voicing.setter
    def voicing(self, voicing):
        if isinstance(voicing, int) and voicing < len(self._VOICING):
            self._voicing = voicing
        elif isinstance(voicing, str):
            self._voicing = self._VOICING.index(voicing.lower())

    def encode_articulation(self, articulation):
        '''
        Convert an articulation string into an integer

        Properties
        ----------
            articulation (str) : Type of articulation (e.g., place, manner)

        Returns
        -------
            Integer representation of the articulation type
        '''
        return self._ATTRIBUTE_LABELS.index(articulation)

    def decode_articulation(self, articulation):
        '''
        Convert an integer into an articulation string

        Properties
        ----------
            articulation (int) : Type of articulation as an integer

        Returns
        -------
            String representation of the articulation type
        '''
        return self._ATTRIBUTE_LABELS[articulation]


class Consonant(Sound):

    def __init__(self):
        super().__init__()

    @property
    def type(self):
        return 'C'


class Vowel(Sound):

    def __init__(self):
        super().__init__()

    @property
    def type(self):
        return 'V'


class Syllable(Sound):
    pass


if __name__ == '__main__':
    s = Sound()
    # print(s._ATTRIBUTES)
    print(s[1])
    print(s['voicing'])
    s.manner = 'affricate'
    s.place = 2
    print(s.manner)
    print(s.place)
    print(s[1][s.manner])
    print(s.encode_articulation('manner'))
    print(s.decode_articulation(1))
