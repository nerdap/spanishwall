import requests
from . import config

class Conjugation(object):
    def __init__(self, yo, tu, el, nosotros, ellos):
        self.yo = yo
        self.tu = tu
        self.el = el
        self.nosotros = nosotros
        self.ellos = ellos

    def as_dict(self):
        return {
            'yo': self.yo,
            'tu': self.tu,
            'el': self.el,
            'nosotros': self.nosotros,
            'ellos': self.ellos,
        }

    def __str__(self):
        return str(self.as_dict())


class DictEntry(object):
    def __init__(
        self,
        word,
        definition,
        example,
        conjugations,
        ):
        self.word = word
        self.definition = definition
        self.example = example
        self.conjugations = conjugations

    def __str__(self):
        conjs_str = {
            id: str(conj)
            for id, conj in self.conjugations
        }
        return f'''
            Word: {self.word}
            Definition: {self.definition}
            Example: {self.example}
            Conjugations: {conjs_str}
        '''


def _parse_conjugation(conj_raw):
    # API documentation: https://dictionaryapi.com/products/json#sec-7.cjts
    forms = conj_raw['cjfs']
    conj = Conjugation(
        yo=forms[0],
        tu=forms[1],
        el=forms[2],
        nosotros=forms[3],
        ellos=forms[5],
    )
    return conj


def _parse_conjugations(conjs_raw):
    CONJ_ID_NAME_MAP = {
        'pind': 'presente',
        'futr': 'futuro',
        'pret': 'pret. imperfecto',
        'ppci': 'pret. perfecto',
    }
    CONJ_ID_ORDERING = ['pind', 'futr', 'pret', 'ppci']

    conjs_raw_map = {
        conj_raw['cjid']: conj_raw
        for conj_raw in conjs_raw
    }
    return [
        (CONJ_ID_NAME_MAP[conj_id], _parse_conjugation(conjs_raw_map[conj_id]))
        for conj_id in CONJ_ID_ORDERING
    ]

def get_entry(word):
    query_url = config.URL.format(word=word, key=config.API_KEY)
    print(f'Querying: {query_url}')
    r = requests.get(query_url)
    if r.status_code != 200:
        raise Exception('Error fetching definition for {}'.format(word))
    if len(r.json()) == 0:
        return None
    entry = r.json()[0]
    if 'shortdef' not in entry or len(entry['shortdef']) == 0:
        return None
    defn = entry['shortdef'][0]

    conjugations = {}
    if 'suppl' in entry and 'cjts' in entry['suppl']:
        conjugations = _parse_conjugations(entry['suppl']['cjts'])

    def_raw = entry['def'][0]
    print(f'Parsing definition: {def_raw}')
    sense_seqs = def_raw['sseq'][0]
    print(f'Parsing sseq: {sense_seqs}')
    first_sense = sense_seqs[0][1]
    print(f'Parsing first sense: {first_sense}')
    defining_text = first_sense['dt']
    print(f'Parsing defining text: {defining_text}')
    visual_illustrations = [
        element[1]
        for element in defining_text
        if element[0] == 'vis'
    ]
    print(f'Parsing visual illustrations: {visual_illustrations}')
    example = None
    if len(visual_illustrations) > 0:
        example_raw = visual_illustrations[0][0]
        example = (example_raw['t'], example_raw['tr'])
    return DictEntry(
        word=word,
        definition=defn,
        example=example,
        conjugations=conjugations,
    )