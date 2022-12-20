conversions = {
    '&': 'and',
    'assn': 'association',
    'inc.': 'incorporation',
    'inc': 'incorporation',
    'inc,': 'incorporation',
    'ltd.': 'limited',
    'ltd.,': 'limited',
    'ltd': 'limited',
    'pharma': 'pharmaceuticals',
    'tech': 'technologies',
    'no.': 'number',
    'co.': 'corporation',
    'co': 'corporation',
    'corp': 'corporation',
    'corp.': 'corporation',
    'const': 'construction',
    'lp': 'limited partnership',
    'l.p.': 'limited partnership',
    'lp.,': 'limited partnership',
    'ltd./': 'limited'
}

stop_words_ctx = set(['and', 'tech','company' 'number', 'service','services','incorporated', 'Incorporated', 'corporation', 'limited', 'association', 'incorporation', 'a', 'and', 'ao', 'oa','co','of', 'to', 'the','by','o', 'partnership'])

ignore_words= set(['as','avs','ags','cs','crs','es','gs','gds','hs','hbs','js','ks','lbs','ls','ms','ncs','os','rands','sos','ss'])
