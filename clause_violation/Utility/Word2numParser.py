numwords = {
    '': (1, 10),
    'and': (1, 0),
    'zero': (1, 0),
    'one': (1, 1),
    'two': (1, 2),
    'three': (1, 3),
    'four': (1, 4),
    'five': (1, 5),
    'six': (1, 6),
    'seven': (1, 7),
    'eight': (1, 8),
    'nine': (1, 9),
    'ten': (1, 10),
    'eleven': (1, 11),
    'twelve': (1, 12),
    'thirteen': (1, 13),
    'fourteen': (1, 14),
    'fifteen': (1, 15),
    'sixteen': (1, 16),
    'seventeen': (1, 17),
    'eighteen': (1, 18),
    'nineteen': (1, 19),
    'twenty': (1, 20),
    'thirty': (1, 30),
    'forty': (1, 40),
    'fifty': (1, 50),
    'sixty': (1, 60),
    'seventy': (1, 70),
    'eighty': (1, 80),
    'ninety': (1, 90),
    'hundred': (100, 0),
    'thousand': (1000, 0),
    'million': (1000000, 0),
    'billion': (1000000000, 0),
    'trillion': (1000000000000, 0),
}


class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def parse_wordnumbers(words):
    number_sets = []
    current_set = []
    for word in words.split():
        if word not in numwords:
            if current_set:
                number_sets.append(' '.join(current_set))
                current_set = []
            continue

        if not current_set and word == 'and':
            continue

        current_set.append(word)
    return number_sets


def words_to_num(words):
    current = result = 0
    for word in words.replace('-', ' ').split():
        if word not in numwords:
            raise NumberException("Unknown number for word: %s" % word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


def num_to_words(words):
    current = result = 0
    for word in words.replace('-', ' ').split():
        if word not in numwords:
            raise NumberException("Unknown number for word: %s" % word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

