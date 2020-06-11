title = __import__('sys').argv[1]

prtags = []
with open('prtags.txt') as f:
    for line in f.readlines():
        try:
            tag, desc = line.strip().split()
        except IndexError:
            pass
        prtags.append(tag)

if not title.startswith('['):
    raise Exception(f'PR tltle does not starts with any tag: {title}')

for x in title.split(']')[1:]:
    if x[0] != ' ':
        raise Exception(f'No space before: {x}')
    if x[1] == ' ':
        raise Exception(f'Extra space before: {x[2:]}')

x = title.split(']')[-1].strip()
if x[0].islower():
    raise Exception(f'PR title content should be uppercase at: {x}')

for x in title.split('] ')[:-1]:
    if x[0] != '[':
        raise Exception(f'No starting [ for tag: {x}]')
    if x[1:].lower() not in prtags:
        raise Exception(f'Unrecognized PR tag: [{x[1:]}]')
