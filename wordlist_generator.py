import itertools

def case_variants(word):
    return [word, word.upper(), word.capitalize()]

def leetspeak(word):
    replacements = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    return [''.join(replacements.get(c, c) for c in word)]

def generate_wordlist(words, symbols, max_combo=3):
    wordlist = set()
    for i in range(1, max_combo + 1):
        for combo in itertools.permutations(words, i):
            base = ''.join(combo)
            variants = case_variants(base) + leetspeak(base)
            for var in variants:
                wordlist.add(var)
                for sym in symbols:
                    wordlist.add(var + sym)
                    wordlist.add(sym + var)
                    for sym2 in symbols:
                        wordlist.add(sym + var + sym2)
    return wordlist
