# -*- coding: utf-8 -*-
"""
resources.py
Glenn Abastillas
Created on Thu Oct 31 09:48:49 2019 / Modified on May 6, 2020

Load and create a resources object that allows for dot-notation access.

"""
from collections import namedtuple
import yaml


class Resource():

    def __init__(self, resource='phonology'):
        self.__initialize(f'resources/{resource}.yaml')


    def __initialize(self, file):
        with open(file) as file_in:
            resource = yaml.load(file_in, yaml.Loader)

            for key, val in resource.items():
                attribute = self.__attribute(key, val)
                setattr(self, key, attribute)
    

    def __attribute(self, key, value):
        attrs = []
        if isinstance(value, dict):
            for k, v in value.items():
                attr = self.__attribute(k, v)
                attrs.append(attr)

            container = namedtuple(key, value.keys())
            return container(*attrs)

        elif isinstance(value, list):
            no_dict = not any([isinstance(__, dict) for __ in value])

            if no_dict:
                return value
            else:
                for item in value:
                    if isinstance(item, dict):
                        sub_attrs = []
                        container = namedtuple(key, item.keys())
                        for k, v in item.items():
                            attr = self.__attribute(k, v)
                            sub_attrs.append(attr)
                        
                        attrs.append(container(*sub_attrs))
            return attrs
        return value


    # def __attribute(self, key, value):
    #     """ Build a namedtuple data structure """
    #     if not isinstance(value, dict):
    #         if isinstance(value, list):
    #             has_dict = any([isinstance(v, dict) for v in value])

    #             if not has_dict:
    #                 return value

    #             values_ = []
    #             for value_ in value:
    #                 if isinstance(value_, dict):
    #                     for key_, val_ in value_.items():
    #                         attribute = self.__attribute(key_, val_)
    #                         values_.append(attribute)
    #             return values_
    #         return value

    #     # One of the values in value had a dict
    #     values_ = []

    #     for key_, val_ in value.items():
    #         attribute = self.__attribute(key_, val_)
    #         values_.append(attribute)

    #     container = namedtuple(key, value.keys())
    #     return container(*values_)


class Phonology(Resource):

    def __init__(self):
        super().__init__('phonology')

class Sounds(Resource):

    def __init__(self):
        super().__init__('sounds')


if __name__ == "__main__":
    # p = Phonology()
    s = Sounds()
    # print(p.phonology)
    print(s.sounds)

