import requests

API_KEY = '198d1aad-a4c8-418b-b224-2b58db12e0eb'
URL = (
    'https://www.dictionaryapi.com/'
    'api/v3/references/spanish/json/{word}?key={key}'
)

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
    query_url = URL.format(word=word, key=API_KEY)
    print(f'Querying: {query_url}')
    r = requests.get(query_url)
    if r.status_code != 200:
        raise Exception('Error fetching definition for {}'.format(word))
    entry = r.json()[0]
    if len(entry['shortdef']) == 0:
        return None
    defn = entry['shortdef'][0]

    conjugations = {}
    if 'suppl' in entry and 'cjts' in entry['suppl']:
        conjugations = _parse_conjugations(entry['suppl']['cjts'])

    example_raw = entry['def'][0]['sseq'][0][0][1]['dt'][1][1][0]
    example = (example_raw['t'], example_raw['tr'])
    return DictEntry(
        word=word,
        definition=defn,
        example=example,
        conjugations=conjugations,
    )