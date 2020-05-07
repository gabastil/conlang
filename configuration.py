# -*- coding: utf-8 -*-
"""
resources.py
Glenn Abastillas
Created on Thu Oct 31 09:48:49 2019 / Modified on May 6, 2020

Load and create a resources object that allows for dot-notation access.

"""
from collections import namedtuple
import yaml
import re
import os

class Resource():

    def __init__(self, resource='phonology'):
        self.__initialize(f'resources/{resource}.yaml')


    def __load(self, file):
        with open(file) as file_in:
            return yaml.load(file_in, yaml.Loader)


    def __initialize(self, file):
        configuration = self.__load(file)

        for k, v in configuration.items():
            attribute = self.__attribute(k, v)
            setattr(self, k, attribute)


    def __attribute(self, key, value):
        """ Build a namedtuple data structure """
        if not isinstance(value, dict):
            if isinstance(value, list):
                dict_found = [isinstance(v, dict) for v in value]

                if not any(dict_found):
                    return value

                else:
                    values_ = []
                    for value_ in value:
                        if isinstance(value_, dict):
                            for k, v in value_.items():
                                aor = self.__attribute(k, v)
                                values_.append(aor)
                    return values_
            else:
                return value

        # One of the values in value had a dict
        values_ = []

        for k, v in value.items():
            values_.append(self.__attribute(k, v))

        container = namedtuple(key, value.keys())
        return container(*values_)

class Phonology(Resource):

    def __init__(self):
        super().__init__('phonology')

if __name__ == "__main__":
    p = Phonology()
    print(p.phonology)