# -*- coding: utf-8 -*-
"""
resources.py
Glenn Abastillas
Created on Thu Oct 31 09:48:49 2019 / Modified on May 6, 2020

Load and create a resources object that allows for dot-notation access.

"""
from collections import namedtuple, defaultdict
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

class PhonologyResource(Resource):

    def __init__(self):
        super().__init__('phonology')

class SoundsResource(Resource):

    class __Sound():
        ''' Subclass for consonant or vowel properties for this syllable '''
        def __init__(self, resource):
            self.resource = resource
            for item in self.resource:
                setattr(self, item.name.replace(" ", "_").replace("-", "_"), item)
        
        def like(self, value):
            return [__ for __ in self.resource if value in __.name]
        
        def name(self, value):
            for resource in self.resource:
                if resource.decimal == value:
                    return resource
        
        def decimal(self, value):
            for resource in self.resource:
                if resource.decimal == value:
                    return resource
        
        def hexadecimal(self, value):
            for resource in self.resource:
                if resource.decimal == value:
                    return resource
        
        def character(self, value):
            for resource in self.resource:
                if resource.character == value:
                    return resource
        
        def get_freq(self):
            container = {}
            for resource in self.resources:
                sample = resource.name.split()
                self.process_name(sample, container)
            return container

        
        def process_name(self, array, container):
            first = array[0]
            if len(array) == 1:
                container.setdefault(first, 0)
                container[first] += 1
            else:
                container.setdefault(first, {})
                container[first] = self.get_freq(array[1:], container[first])
            return container
        
        def probability(self, value):
            ''' Return the probability of a value for a __Sound property '''
            data = [resource.name.split() for resource in self.resource]


        def conditional_probability(self, condition, value):
            ''' Return the probability of value given the condition '''
            raise NotImplementedError()


    def __init__(self):
        super().__init__('sounds')
        self.c = self.__Sound(self.consonant)
        self.v = self.__Sound(self.vowel)
    
    def find(self, value):
        return self.c.like(value) + self.v.like(value)
    
    def like(self, sound):
        ''' 
        Return sound that matches the input Consonant or Vowel 
        
        Properties
        ----------
            sound (Sound, Consonant, Vowel): User input to match to resource
        '''
        raise NotImplementedError()



if __name__ == "__main__":
    # p = Phonology()
    s = Sounds()
    # print(p.phonology)
    print(s.sounds)


# def loop(a, d={}):
#     if len(a) == 1:
#         d.setdefault(a[0], 0)
#         d[a[0]] += 1
#     else:
#         d.setdefault(a[0], {})
#         d[a[0]] = loop(a[1:], d[a[0]])
#     return d
