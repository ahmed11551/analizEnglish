# Тест B2 Grammar — вопросы, ключ и тексты уровней.

QUESTIONS = [
    {
        "id": 1,
        "part": "Часть 1. Основная грамматика",
        "text": "She ___ to the gym every day.",
        "options": {"a": "go", "b": "goes", "c": "going"},
        "topic": "Present Simple",
        "correct": "b",
    },
    {
        "id": 2,
        "part": None,
        "text": "They ___ dinner right now.",
        "options": {"a": "have", "b": "are having", "c": "having"},
        "topic": "Present Continuous",
        "correct": "b",
    },
    {
        "id": 3,
        "part": None,
        "text": "I ___ my keys yesterday.",
        "options": {"a": "lose", "b": "lost", "c": "have lost"},
        "topic": "Past Simple",
        "correct": "b",
    },
    {
        "id": 4,
        "part": None,
        "text": "She ___ already finished her homework.",
        "options": {"a": "did", "b": "has", "c": "have"},
        "topic": "Present Perfect",
        "correct": "b",
    },
    {
        "id": 5,
        "part": None,
        "text": "We ___ in this city since 2010.",
        "options": {"a": "live", "b": "lived", "c": "have lived"},
        "topic": "Present Perfect",
        "correct": "c",
    },
    {
        "id": 6,
        "part": None,
        "text": "If I ___ rich, I would travel the world.",
        "options": {"a": "am", "b": "were", "c": "would be"},
        "topic": "Second Conditional (form focus)",
        "correct": "b",
    },
    {
        "id": 7,
        "part": None,
        "text": "He ___ to London next week.",
        "options": {"a": "goes", "b": "is going", "c": "go"},
        "topic": "Future (plans)",
        "correct": "b",
    },
    {
        "id": 8,
        "part": "Часть 2. Quantifiers",
        "text": "There isn’t ___ milk in the fridge.",
        "options": {"a": "some", "b": "any", "c": "a"},
        "topic": "Quantifiers",
        "correct": "b",
    },
    {
        "id": 9,
        "part": None,
        "text": "I have ___ friends in this city.",
        "options": {"a": "much", "b": "many", "c": "little"},
        "topic": "Countable nouns",
        "correct": "b",
    },
    {
        "id": 10,
        "part": None,
        "text": "There is ___ water left.",
        "options": {"a": "few", "b": "little", "c": "many"},
        "topic": "Uncountable nouns",
        "correct": "b",
    },
    {
        "id": 11,
        "part": "Часть 3. Modal verbs & Reported speech",
        "text": "He ___ play the piano when he was a child.",
        "options": {"a": "can", "b": "could", "c": "must"},
        "topic": "Past ability",
        "correct": "b",
    },
    {
        "id": 12,
        "part": None,
        "text": "You ___ wear a seatbelt. It’s the law.",
        "options": {"a": "can", "b": "must", "c": "may"},
        "topic": "Obligation",
        "correct": "b",
    },
    {
        "id": 13,
        "part": None,
        "text": "She asked me where I ___.",
        "options": {"a": "live", "b": "lived", "c": "am living"},
        "topic": "Reported Speech",
        "correct": "b",
    },
    {
        "id": 14,
        "part": None,
        "text": "He ___ go to the party if he finishes work.",
        "options": {"a": "might", "b": "must", "c": "should"},
        "topic": "Possibility",
        "correct": "a",
    },
    {
        "id": 15,
        "part": "Часть 4. Conditionals",
        "text": "If it rains, we ___.",
        "options": {"a": "stay", "b": "will stay", "c": "stayed"},
        "topic": "First Conditional",
        "correct": "b",
    },
    {
        "id": 16,
        "part": None,
        "text": "If I had more money, I ___ a car.",
        "options": {"a": "buy", "b": "would buy", "c": "will buy"},
        "topic": "Second Conditional",
        "correct": "b",
    },
    {
        "id": 17,
        "part": "Часть 5. Articles",
        "text": "I saw ___ interesting film yesterday.",
        "options": {"a": "a", "b": "an", "c": "the"},
        "topic": "Articles",
        "correct": "b",
    },
    {
        "id": 18,
        "part": None,
        "text": "___ sun rises in the east.",
        "options": {"a": "A", "b": "The", "c": "—"},
        "topic": "Articles",
        "correct": "b",
    },
    {
        "id": 19,
        "part": "Часть 6. Vocabulary",
        "text": "He ___ me that he was tired.",
        "options": {"a": "said", "b": "told", "c": "spoke"},
        "topic": "Tell vs Say",
        "correct": "b",
    },
    {
        "id": 20,
        "part": None,
        "text": "Please ___ at the board.",
        "options": {"a": "see", "b": "watch", "c": "look"},
        "topic": "Look vs See",
        "correct": "c",
    },
    {
        "id": 21,
        "part": "Часть 7. Prepositions & patterns",
        "text": "I’m not interested ___ politics.",
        "options": {"a": "on", "b": "in", "c": "at"},
        "topic": "Prepositions",
        "correct": "b",
    },
]

LEVEL_BANDS = [
    (0, 3, "Pre-A1", "pre_a1"),
    (4, 7, "A1", "a1"),
    (8, 12, "A2", "a2"),
    (13, 16, "B1", "b1"),
    (17, 19, "B2", "b2"),
    (20, 21, "B2+", "b2_plus"),
]

LEVEL_TEXTS = {
    "pre_a1": """Pre-A1 (0–3)
Сейчас у тебя самый начальный уровень. Ты можешь узнавать отдельные слова, но строить предложения пока сложно. Грамматика практически не работает — всё на уровне догадок.
Тебе важно начать с базы: глагол to be, простые конструкции (I am, I have), базовые слова и короткие фразы. Это фундамент, без него дальше не пойдёт.""",
    "a1": """A1 (4–7)
Ты уже можешь сказать простые вещи о себе: кто ты, где живёшь, чем занимаешься. Но речь очень ограниченная, и ошибок много.
Чаще всего проблемы с временами, формами глаголов и артиклями.
Тебе нужно закрепить основу: Present Simple, Present Continuous и понять, как работают a / the. Плюс расширять базовый словарь.""",
    "a2": """A2 (8–12)
Ты уже можешь говорить про прошлое и настоящее, объясниться в простых ситуациях. В целом тебя понимают, даже если есть ошибки.
Но пока не хватает точности: путается Present Perfect, предлоги используются неуверенно, сложные конструкции даются тяжело.
Тебе стоит прокачать времена (особенно Present Perfect), предлоги и слова типа much / many / few / little.""",
    "b1": """B1 (13–16)
Ты уже нормально общаешься на бытовые темы. Можешь поддержать разговор, рассказать историю, объяснить свою мысль.
Но речь пока не всегда точная: есть ошибки в условных предложениях, косвенной речи, иногда используешь не совсем подходящие слова.
Тебе нужно работать над точностью: conditionals, reported speech и разница между похожими словами (например, say / tell).""",
    "b2": """B2 (17–19)
Ты говоришь достаточно свободно. Можешь обсуждать разные темы и в целом хорошо понимаешь английскую речь.
Ошибки уже не критичные, но иногда речь звучит «не совсем по-английски» — из-за предлогов, артиклей или выбора слов.
Тебе стоит прокачать естественность: устойчивые выражения, правильные сочетания слов и мелкие грамматические детали.""",
    "b2_plus": """B2+ (20–21)
У тебя уже уверенный уровень. Ты хорошо говоришь, понимаешь английский и редко допускаешь серьёзные ошибки.
Остаются только нюансы: звучать максимально естественно, выбирать правильный стиль и избегать влияния родного языка.
Дальше — это уже движение к C1: больше живого языка, идиом и практики в сложных темах.""",
}

CTA_TEXT = (
    "Если ты хочешь повысить свой уровень и научиться говорить по-английски. Я могу в этом помочь. "
    "Переходи на сайт и оставь заявку. Первый урок бесплатный."
)
