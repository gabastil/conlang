from resource import SoundsResource
from sounds import Sound, Consonant, Vowel

SNDS = SoundsResource()


class Mora():

    def __init__(self):
        self.weight = 1

    def add(self):
        self.weight += 1

    def remove(self):
        if self.weight > -1:
            self.weight -= 1


class Syllable(Sound, Mora):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._parse(*args, **kwargs)

    def __repr__(self):
        syllable = [__.type for __ in self.syllable]
        return f"Syllable( {''.join(syllable)} )"

    def __getitem__(self, index):
        return self.syllable[index]

    def _parse(self, *args, **kwargs):
        ''' Parse and detect the sound types that structure this syllable '''

        nucleus = 'v'
        if args:
            if len(args) == 1:
                syllable = args[0].lower()

            else:
                syllable = ''.join(args).lower()

            nucleus *= syllable.count(nucleus)

            if not nucleus:
                error = (
                    'Unable to determine nucleus. No vowel nucleus detected. Define '
                    'this syllable with a vowel nucleus `v` or using keyword arguments '
                    'like `onset`, `nucleus`, and `coda` instead (e.g., Syllable(onset'
                    '="cc", nucleus="c") if the nucleus is a consonant.'
                )
                raise ValueError(error)

            onset, *_, coda = syllable.split(nucleus)
        
        elif kwargs:
            onset = kwargs.get('onset', '').lower()
            nucleus = kwargs.get('nucleus', 'v').lower()
            coda = kwargs.get('coda', '').lower()

        sound_type = lambda L : [Consonant() 
                                 if __.startswith('c') else Vowel()
                                 for __ in L]
    
        self.onset = sound_type(onset)
        self.nucleus = sound_type(nucleus)
        self.coda = sound_type(coda)

        self.body = self.onset + self.nucleus
        self.rhyme = self.nucleus + self.coda
        self.syllable = self.body + self.coda

    def random_representation(self):
        ''' IN DEVELOPMENT USE WITH SOUNDS.YAML '''

        if self.syllable:
            representation = []
            for syllable in self.syllable:
                syllable.randomize()
                representation.append(syllable.orthography())
            return ''.join(representation)

if __name__ == "__main__":
    syl = Syllable('cvc')
    print(syl)