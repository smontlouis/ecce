from ecce.constants import ESV_PATH

from base64 import b64decode, b64encode
from collections import namedtuple as Struct
from funcy import first, cat
import json
import logging
from toolz import memoize, pipe, curry
from toolz.curried import filter

Data = Struct('Reference', ['book', 'chapter', 'verse'])

@memoize
def all():
    with open(ESV_PATH) as f:
        data = json.load(f)
        logging.info('Loading ESV references...')
        return list(cat(cat(
            [[[Data(b, int(c), int(v)) for v in data[b][c].keys()]
                                       for c in data[b].keys()]
                                       for b in data.keys()]
        )))

def reference(book, chapter, verse):
    result = pipe(all(), filter(_match((book, chapter, verse))), first)

    if result is None:
        logging.error(f'No reference found: {(book, chapter, verse)}')

    return result

@curry
def _match(components, ref):
    book, chapter, verse = components
    return ref.book == book and ref.chapter == chapter and ref.verse == verse
