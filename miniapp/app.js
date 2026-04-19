const QUESTIONS = [
  {
    id: 1,
    text: "She ___ to the gym every day.",
    options: { a: "go", b: "goes", c: "going" },
    topic: "Present Simple",
    correct: "b",
  },
  {
    id: 2,
    text: "They ___ dinner right now.",
    options: { a: "have", b: "are having", c: "having" },
    topic: "Present Continuous",
    correct: "b",
  },
  {
    id: 3,
    text: "I ___ my keys yesterday.",
    options: { a: "lose", b: "lost", c: "have lost" },
    topic: "Past Simple",
    correct: "b",
  },
  {
    id: 4,
    text: "She ___ already finished her homework.",
    options: { a: "did", b: "has", c: "have" },
    topic: "Present Perfect",
    correct: "b",
  },
  {
    id: 5,
    text: "We ___ in this city since 2010.",
    options: { a: "live", b: "lived", c: "have lived" },
    topic: "Present Perfect",
    correct: "c",
  },
  {
    id: 6,
    text: "If I ___ rich, I would travel the world.",
    options: { a: "am", b: "were", c: "would be" },
    topic: "Second Conditional (form focus)",
    correct: "b",
  },
  {
    id: 7,
    text: "He ___ to London next week.",
    options: { a: "goes", b: "is going", c: "go" },
    topic: "Future (plans)",
    correct: "b",
  },
  {
    id: 8,
    text: "There isn’t ___ milk in the fridge.",
    options: { a: "some", b: "any", c: "a" },
    topic: "Quantifiers",
    correct: "b",
  },
  {
    id: 9,
    text: "I have ___ friends in this city.",
    options: { a: "much", b: "many", c: "little" },
    topic: "Countable nouns",
    correct: "b",
  },
  {
    id: 10,
    text: "There is ___ water left.",
    options: { a: "few", b: "little", c: "many" },
    topic: "Uncountable nouns",
    correct: "b",
  },
  {
    id: 11,
    text: "He ___ play the piano when he was a child.",
    options: { a: "can", b: "could", c: "must" },
    topic: "Past ability",
    correct: "b",
  },
  {
    id: 12,
    text: "You ___ wear a seatbelt. It’s the law.",
    options: { a: "can", b: "must", c: "may" },
    topic: "Obligation",
    correct: "b",
  },
  {
    id: 13,
    text: "She asked me where I ___.",
    options: { a: "live", b: "lived", c: "am living" },
    topic: "Reported Speech",
    correct: "b",
  },
  {
    id: 14,
    text: "He ___ go to the party if he finishes work.",
    options: { a: "might", b: "must", c: "should" },
    topic: "Possibility",
    correct: "a",
  },
  {
    id: 15,
    text: "If it rains, we ___.",
    options: { a: "stay", b: "will stay", c: "stayed" },
    topic: "First Conditional",
    correct: "b",
  },
  {
    id: 16,
    text: "If I had more money, I ___ a car.",
    options: { a: "buy", b: "would buy", c: "will buy" },
    topic: "Second Conditional",
    correct: "b",
  },
  {
    id: 17,
    text: "I saw ___ interesting film yesterday.",
    options: { a: "a", b: "an", c: "the" },
    topic: "Articles",
    correct: "b",
  },
  {
    id: 18,
    text: "___ sun rises in the east.",
    options: { a: "A", b: "The", c: "—" },
    topic: "Articles",
    correct: "b",
  },
  {
    id: 19,
    text: "He ___ me that he was tired.",
    options: { a: "said", b: "told", c: "spoke" },
    topic: "Tell vs Say",
    correct: "b",
  },
  {
    id: 20,
    text: "Please ___ at the board.",
    options: { a: "see", b: "watch", c: "look" },
    topic: "Look vs See",
    correct: "c",
  },
  {
    id: 21,
    text: "I’m not interested ___ politics.",
    options: { a: "on", b: "in", c: "at" },
    topic: "Prepositions",
    correct: "b",
  },
];

const LEVEL_BANDS = [
  { lo: 0, hi: 3, label: "Pre-A1" },
  { lo: 4, hi: 7, label: "A1" },
  { lo: 8, hi: 12, label: "A2" },
  { lo: 13, hi: 16, label: "B1" },
  { lo: 17, hi: 19, label: "B2" },
  { lo: 20, hi: 21, label: "B2+" },
];

const LEVEL_TEXTS = {
  "Pre-A1":
    "Сейчас у тебя самый начальный уровень. Начни с базы: to be, простые конструкции и базовый словарь.",
  A1: "Ты уже можешь строить простые фразы, но стоит закрепить времена Present Simple / Present Continuous и артикли.",
  A2: "Ты можешь общаться в простых ситуациях. Рекомендуется усилить Present Perfect и предлоги.",
  B1: "У тебя хороший рабочий уровень. Прокачивай точность: conditionals, reported speech, словоупотребление.",
  B2: "Ты говоришь достаточно свободно. Фокус на естественность: устойчивые выражения и тонкие грамматические нюансы.",
  "B2+": "Очень уверенный уровень. Дальше — выход на C1 через сложные темы, стиль и живой язык.",
};

const WEBSITE_URL = "https://desharschool.ru";
const appRoot = document.getElementById("quiz-card");
const questionTemplate = document.getElementById("question-template");
const resultTemplate = document.getElementById("result-template");

const state = {
  qIndex: 0,
  answers: [],
};

function scoreToLevel(score) {
  return LEVEL_BANDS.find((band) => score >= band.lo && score <= band.hi)?.label ?? "B2+";
}

function answerQuestion(choice) {
  const q = QUESTIONS[state.qIndex];
  state.answers.push({
    questionId: q.id,
    topic: q.topic,
    chosen: choice,
    correct: q.correct,
    isCorrect: choice === q.correct,
  });
  state.qIndex += 1;
}

function resetQuiz() {
  state.qIndex = 0;
  state.answers = [];
  renderQuiz();
}

function renderResult() {
  const node = resultTemplate.content.cloneNode(true);
  const score = state.answers.filter((a) => a.isCorrect).length;
  const level = scoreToLevel(score);
  const wrongTopics = [...new Set(state.answers.filter((a) => !a.isCorrect).map((a) => a.topic))];

  node.getElementById("score-line").textContent = `Правильных ответов: ${score} из ${QUESTIONS.length}`;
  node.getElementById("level-line").textContent = `Твой уровень: ${level}`;
  node.getElementById("level-text").textContent = LEVEL_TEXTS[level];

  const mistakesList = node.getElementById("mistakes-list");
  const reviewList = node.getElementById("review-list");
  if (wrongTopics.length === 0) {
    mistakesList.innerHTML = "<li>Ошибок нет — отличный результат.</li>";
    reviewList.innerHTML = "<li>Можно переходить к более сложным темам (B2+/C1).</li>";
  } else {
    for (const topic of wrongTopics) {
      const liMistake = document.createElement("li");
      liMistake.textContent = topic;
      mistakesList.append(liMistake);

      const liReview = document.createElement("li");
      liReview.textContent = topic;
      reviewList.append(liReview);
    }
  }

  const ctaBtn = node.querySelector(".site-button");
  ctaBtn.href = WEBSITE_URL;

  node.getElementById("restart-btn").addEventListener("click", resetQuiz);
  appRoot.replaceChildren(node);
}

function renderQuiz() {
  if (state.qIndex >= QUESTIONS.length) {
    renderResult();
    return;
  }

  const q = QUESTIONS[state.qIndex];
  const node = questionTemplate.content.cloneNode(true);
  const progressPercent = ((state.qIndex + 1) / QUESTIONS.length) * 100;

  node.getElementById("progress-fill").style.width = `${progressPercent}%`;
  node.getElementById("progress-text").textContent = `Вопрос ${state.qIndex + 1} из ${QUESTIONS.length}`;
  node.getElementById("question-text").textContent = `${q.id}. ${q.text}`;

  const optionsRoot = node.getElementById("options");
  for (const key of ["a", "b", "c"]) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "option-btn";
    btn.textContent = `${key}) ${q.options[key]}`;
    btn.addEventListener("click", () => {
      answerQuestion(key);
      renderQuiz();
    });
    optionsRoot.append(btn);
  }

  appRoot.replaceChildren(node);
}

renderQuiz();
