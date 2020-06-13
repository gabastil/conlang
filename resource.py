# -*- coding: utf-8 -*-
"""
resources.py
Glenn Abastillas
Created on Thu Oct 31 09:48:49 2019 / Modified on May 6, 2020

Load and create a resources object that allows for dot-notation access.

"""
from collections import namedtuple, defaultdict
import yaml


def process_ipa(text, filename):
    import re
    dots = re.compile(r'(.)([:ː])', re.I)
    ipa = re.compile(r'/(.+?)/', re.I)

    text = dots.sub(r'\1\1', text)
    text = ipa.findall(text)

    with open(filename, 'w') as fout:
        text = '\n'.join(text)
        fout.write(text)


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
        
        def get_prob(self, feature, condition=None):
            '''
            Return the probability of a feature in the sounds resource
            
            Parameters
            ----------
                feature (str) : name of feature to check (e.g., voiced, bilabial)
                condition (str) : name of feature to condition the specified feature on
             '''
            freq = self.get_freq()
            feat = self._get_dict(feature, container=freq)
            
            if condition:
                freq = self._get_dict(condition, container=freq)

            return self._sum_dict(feat) / self._sum_dict(freq)
        
        def _get_dict(self, label, container):
            ''' Return a the dictionary that matches the specified label '''
            container_is_a_number = isinstance(container, int) or isinstance(container, float)
            
            if container_is_a_number:
                return container

            if label in container:
                return container[label]
            
            if isinstance(container, tuple):
                return container


            '''
            NEEDS TO BE FIXED SO THAT IT DOESN'T RETURN ANYTHING FOR A NONSENSE label INPUT

            e.g., self._get_dict('asdfadsf', container)

            WILL STILL RETURN SOMETHING
            '''
            if isinstance(container, dict):
                item = None

                for k, v in container.items():
                    if label in v:
                        return v[label]

                    item = self._get_dict(label, v)

                    if item:
                        return item

        def _div_dict(self, divisor, container):
            # print(divisor, container)
            if isinstance(container, int) or isinstance(container, float):
                # print(container / divisor)
                return container / divisor
            
            if isinstance(container, tuple):
                left, right = container
                left /= divisor
                
                right = self._div_dict(divisor, right)
                return left, right
        
            for k, v in container.items():
                container[k] = self._div_dict(divisor, v)
            
            return container

        def _sum_dict(self, container):
            ''' 
            Return the sum of all items below the level of this label 
            
            Parameters
            ----------
                container (dict, tuple, int) : dictionary with values to sum.
                    if tuple, function checks for integer value and other dicts.
                    if integer, function returns it.
            '''
            total = 0

            if isinstance(container, int) or isinstance(container, float):
                return container
            
            elif isinstance(container, tuple):
                total += container[0]
                container = container[1]

            for k, v in container.items():
                total += self._sum_dict(v)
                
            return total


        def get_freq(self):
            container = {}
            for resource in self.resource:
                sample = resource.name.split()
                self._conditional_frequency(sample, container)
            return container
        
        def _conditional_frequency(self, array, container):
            first = array[0]
            if len(array) == 1:
                if isinstance(container, dict):
                    container.setdefault(first, 0)
                    container[first] += 1
                elif isinstance(container, int):
                    container = (container, {})
                    container[1].setdefault(first, 0)
                    container[1][first] += 1
                else:
                    container[1].setdefault(first, 0)
                    container[1][first] += 1
            elif isinstance(container, int):
                container = (container, {})
                container[1] = self._conditional_frequency(array[1:], container[1][first])
            elif isinstance(container, tuple):
                container[1] = self._conditional_frequency(array[1:], container[1][first])
            else:
                container.setdefault(first, {})
                container[first] = self._conditional_frequency(array[1:], container[first])
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
    # s = Sounds()
    # print(p.phonology)
    # print(s.sounds)

    sr = SoundsResource()
    d = sr.c.get_freq()
    r = sr.c._sum_dict(d)
    print(r)
    k = d['voiced']
    r = sr.c._sum_dict(d['voiced'])
    print(k)
    sr.c._div_dict(r, k)
    print(r)
    # print(k)
    # print(k['bilabial']['stop'])
    # print(sr.c._sum_dict(k['bilabial']))

    print("Check")
    print(sr.c._get_dict('stop', d))
    print(sr.c._sum_dict(sr.c._get_dict('stop', d)))

    print("-" * 10)
    print(sr.c.get_prob('stop', 'voiceless'))
    print(sr.c.get_prob('asdf', 'voiceless'))
    print(d)
    print(sr.c._get_dict('asdfasdf', d))

    p = [(k, sr.c._sum_dict(v)) for k, v in k.items()]

    import pprint
    pprint.pprint(sorted(p, key=lambda x: x[-1]))

    # print(sr.c._sum_dict(x))


# def loop(a, d={}):
#     if len(a) == 1:
#         d.setdefault(a[0], 0)
#         d[a[0]] += 1
#     else:
#         d.setdefault(a[0], {})
#         d[a[0]] = loop(a[1:], d[a[0]])
#     return d
