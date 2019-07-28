with open('db1.txt', 'r') as f:
    c = f.read().replace('further-', '').split(',\n')
d = []

for e in c:
    e = e.replace('(', '').replace(')', '').split(',')
    f = {}
    f['question_number'] = e[1].replace("'", '').strip()
    f['paper'] = e[2].replace("'", '').strip()
    f['question_id'] = e[3].replace("'", '').strip()
    f['video'] = e[4].replace("'", '').strip()
    f['topics'] = [e[5].replace("'", '').replace('-', '_').strip()]

    z = False

    for counter, l in enumerate(d):
        if not z and l['question_id'] == f['question_id']:
            z = True
            if f['topics'][0] not in d[counter]['topics']:
                d[counter]['topics'] += f['topics']


    if not z:
        d += [f]

l = ''

for e in d:
    s = ','
    e['topics'] = s.join(e['topics'])
    l += "db.session.add(Question(marks=4, question_id='" + e['question_id'] + "', question_number='" + e['question_number'] + "', video='" + e['video'] + "', paper='" + e['paper'] + "', topics='" + e['topics'] + "'))\n"

with open('db2.txt', 'w') as f:
    f.write(l)
