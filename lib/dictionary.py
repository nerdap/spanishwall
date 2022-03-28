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
        conjugations,
        ):
        self.word = word
        self.definition = definition
        self.conjugations = conjugations

    def __str__(self):
        conjs_str = {
            id: str(conj)
            for id, conj in self.conjugations.items()
        }
        return f'''
            Word: {self.word}
            Definition: {self.definition}
            Conjugations: {conjs_str}
        '''


def _parse_conjugation(conj_raw):
    # API documentations: https://dictionaryapi.com/products/json#sec-7.cjts
    print(conj_raw)
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
        'pint': 'presente',
        'futr': 'futuro',
        'pret': 'preterito imperfecto',
        'ppci': 'preterito perfecto',
    }
    return {
        CONJ_ID_NAME_MAP[conj_raw['cjid']]: _parse_conjugation(conj_raw)
        for conj_raw in conjs_raw
        if conj_raw['cjid'] in CONJ_ID_NAME_MAP
    }


def get_entry(word):
    query_url = URL.format(word=word, key=API_KEY)
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
    return DictEntry(
        word=word,
        definition=defn,
        conjugations=conjugations,
    )