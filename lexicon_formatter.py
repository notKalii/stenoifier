import pickle

with open('lexicon', 'r') as f:
    SECTIONS = ['ortho', 'id', 'part', 'pron', 'ertho', 'freq']
    lexicon = []
    for line in f.readlines():
        line = line.split(':')
        entry = {}
        i = 0
        for sect in line:
            entry[SECTIONS[i]] = line[i]
            i += 1
        lexicon.append(entry)

lex = []
for entry in lexicon:
    newEntry = {}
    newEntry['ortho'] = entry['ortho']

    try:
        if not entry['id'][0] == '1':
            continue
    except:
        pass

    part = entry['part']
    parts = part.split('/')
    remove = True
    for p in parts:
        x = False
        for q in p.split('|'):
            if q in ['NNP', 'NNPS', 'FW']:
                x = True
        
        if not x:
            remove = False
    if remove:
        continue

    token = ''
    syl = []
    word = []
    sect = []
    vowel = False
    for char in entry['pron']+'.':
        if char in ['*', '~', '-', '$', '=', '{', '}', '<', '>']:
            continue
        if char == '.':
            syl.append(sect)
            while len(syl) < 3:
                syl.append([])
            word.append(syl)
            syl = []
            sect = []
            vowel = False
            continue
        if char == ' ':
            if token != '':
                if (vowel) != (token[0] in ['a', 'e', 'i', 'o', 'u', '@']):
                    syl.append(sect)
                    sect = []
                    vowel = False if vowel else True
                elif token[-1] == '!':
                    syl.append(sect)
                    syl.append(['@'])
                    sect = []
                    token = token[:-1]
                sect.append(token)
                token = ''
            continue

        token += char
    newEntry['pron'] = word

    token = ''
    affix_open = False
    word = [[], '', []]
    i = 0
    for char in entry['ertho']:
        if char in ['=', '{']:
            continue
        if char in ['<', '>']:
            if affix_open:
                word[i].append(token)
                token = ''
                affix_open = False
            else:
                affix_open = True
            continue
        if char == '}':
            word[1] += token
            token = ''
            i = 2
            continue
        token += char
    newEntry['ertho'] = word

    lex.append(newEntry)

with open('lexicon_f', 'wb') as fp:
    pickle.dump(lex, fp)