LANGUAGE_FEATURES = [
    {'id': 1, 'name': 'Cardinal Numbers', 'description': ''},
    {'id': 2, 'name': 'Simple Affirmations & Negations', 'description': ''},
    {'id': 3, 'name': 'Posessive Pronouns', 'description': ''},
    {'id': 4, 'name': 'Subject Pronouns', 'description': ''},
    {'id': 5, 'name': 'Explitive Subjects + Be-verb', 'description': ''},
    {'id': 6, 'name': 'Common Conjunctions', 'description': ''},
    {'id': 7, 'name': 'Pronoun + Abreviated Be-Verb', 'description': ''},
    {'id': 8, 'name': 'Negation Words', 'description': ''},
    {'id': 9, 'name': 'Present / Past Tense Be-verb Not Used in Passive Construction', 'description': ''},
    {'id': 10, 'name': 'Negetive Abbreviation Be-verb not Used in Passive Construction', 'description': ''},
    {'id': 11, 'name': 'Intransitive Present-tense Indicitive', 'description': ''},
    {'id': 12, 'name': 'Intransitive Infinitive Verbs', 'description': ''},
    {'id': 13, 'name': 'Indefinite Article', 'description': ''},
    {'id': 14, 'name': 'Demonstratives', 'description': ''},
    {'id': 15, 'name': 'Intransitive, Progressive Verbs', 'description': ''},
    {'id': 16, 'name': 'Transitive, Progressive Verbs', 'description': ''},
    {'id': 17, 'name': 'Two-argument Transitive Verbs', 'description': ''},
    {'id': 18, 'name': 'Colloquial Words / Phrases', 'description': ''},
    {'id': 19, 'name': 'Questions with Raising Do-verb', 'description': ''},
    {'id': 20, 'name': 'Adjective + Adverb Phrase', 'description': ''},
    {'id': 21, 'name': 'Simple Adjective + Noun Pairs', 'description': ''},
    {'id': 22, 'name': 'Ordinal Numbers', 'description': ''},
    {'id': 23, 'name': 'Scope Words', 'description': ''},
    {'id': 24, 'name': 'Comparitive Words / Structures', 'description': ''},
    {'id': 25, 'name': 'Prepositional Phrases', 'description': ''},
    {'id': 26, 'name': 'Prepositional Verb Phrases', 'description': ''},
    {'id': 27, 'name': 'Past Tense Verbs', 'description': ''},
    {'id': 28, 'name': 'Future Tense Verbs', 'description': ''},
    {'id': 29, 'name': 'Three-argument Transitive Verbs', 'description': ''},
    {'id': 30, 'name': 'Exclamitory Phrases', 'description': ''},
    {'id': 31, 'name': 'Long Distance Dependencies', 'description': ''},
    {'id': 32, 'name': 'Modals', 'description': ''},
    {'id': 33, 'name': 'Reflexives', 'description': ''},
    {'id': 34, 'name': 'Passive Voice', 'description': ''},
    {'id': 35, 'name': 'Perfect Aspect Verbs', 'description': ''},
    {'id': 36, 'name': 'Subjunctive Mood', 'description': ''},
    {'id': 37, 'name': 'Idiomatic Expressions', 'description': ''},
    {'id': 38, 'name': 'Objective Clause', 'description': ''},
    {'id': 39, 'name': 'Preposition Phrase that modifies a noun', 'description': ''},
    {'id': 40, 'name': 'Relative Clauses', 'description': ''},
]

BLEND_LEVELS = {
    0: [],
    50: [1, ],
    75: [1, 2, ],
    100: [1, 2, 3]
}

BLEND_LEVEL_FEATURES = {
    'A': [],
    'B': [1, ],
    'C': [1, 2, 3],
    'D': [1, 2, 3, 4, 5],
    'E': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}

LANGUAGES = ['english', 'spanish', 'french', 'italian', 'russian']
