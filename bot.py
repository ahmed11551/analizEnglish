"""
Telegram-бот: тест English Grammar & Usage (B2), анкета, подсчёт уровня и тем для повторения.
Запуск: set BOT_TOKEN, затем python bot.py
"""

from __future__ import annotations

import logging
import os
import re

from dotenv import load_dotenv
from typing import Any

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from questions_data import (
    CTA_TEXT,
    INTRO_FIELDS,
    INTRO_LABELS_RU,
    LEVEL_BANDS,
    LEVEL_TEXTS,
    QUESTIONS,
)

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def score_to_level(score: int) -> tuple[str, str]:
    for lo, hi, label, key in LEVEL_BANDS:
        if lo <= score <= hi:
            return label, key
    return LEVEL_BANDS[-1][2], LEVEL_BANDS[-1][3]


def build_question_keyboard(qid: int) -> InlineKeyboardMarkup:
    row = [
        InlineKeyboardButton("a", callback_data=f"q:{qid}:a"),
        InlineKeyboardButton("b", callback_data=f"q:{qid}:b"),
        InlineKeyboardButton("c", callback_data=f"q:{qid}:c"),
    ]
    return InlineKeyboardMarkup([row])


def format_question_message(q: dict[str, Any]) -> str:
    lines: list[str] = []
    if q.get("part"):
        lines.append(q["part"])
        lines.append("")
    lines.append(f"{q['id']}. {q['text']}")
    opts = q["options"]
    lines.append(f"a) {opts['a']}")
    lines.append(f"b) {opts['b']}")
    lines.append(f"c) {opts['c']}")
    lines.append("")
    lines.append(f"Тема: {q['topic']}")
    return "\n".join(lines)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ud = context.user_data
    ud.clear()
    ud["phase"] = "intro"
    ud["intro_step"] = 0
    ud["intro_answers"] = {}
    ud["answers"] = []

    title = (
        "📘 English Grammar & Usage Test (B2)\n\n"
        "Этот тест покажет твой уровень и какие темы стоит повторить.\n\n"
        "Пару слов о себе перед началом теста:"
    )
    _, prompt = INTRO_FIELDS[0]
    await update.effective_message.reply_text(f"{title}\n\n{prompt}")


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    await update.effective_message.reply_text("Тест прерван. Начни снова: /start")


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    ud = context.user_data
    phase = ud.get("phase")
    text = update.message.text.strip()

    if phase == "intro":
        step = ud.get("intro_step", 0)
        key, _ = INTRO_FIELDS[step]
        ud["intro_answers"][key] = text
        step += 1
        ud["intro_step"] = step
        if step < len(INTRO_FIELDS):
            _, prompt = INTRO_FIELDS[step]
            await update.message.reply_text(prompt)
            return
        ud["phase"] = "quiz"
        ud["q_index"] = 0
        q = QUESTIONS[0]
        await update.message.reply_text(
            format_question_message(q),
            reply_markup=build_question_keyboard(q["id"]),
        )
        return

    if phase == "lead":
        ud["lead_contact"] = text
        ud["phase"] = "done"
        await update.message.reply_text(
            "Спасибо! Менеджер свяжется с тобой в Telegram.",
        )
        logger.info(
            "Lead: user_id=%s contact=%s",
            update.effective_user.id if update.effective_user else None,
            text,
        )
        return


async def on_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()
    ud = context.user_data
    if ud.get("phase") != "quiz":
        return

    m = re.match(r"^q:(\d+):([abc])$", query.data)
    if not m:
        return
    qid = int(m.group(1))
    chosen = m.group(2)
    q = QUESTIONS[ud.get("q_index", 0)]
    if q["id"] != qid:
        return

    is_correct = chosen == q["correct"]
    ud.setdefault("answers", []).append(
        {
            "question_id": qid,
            "topic": q["topic"],
            "chosen": chosen,
            "correct": q["correct"],
            "is_correct": is_correct,
        }
    )

    idx = ud.get("q_index", 0) + 1
    ud["q_index"] = idx
    if idx < len(QUESTIONS):
        nq = QUESTIONS[idx]
        try:
            await query.edit_message_reply_markup(reply_markup=None)
        except Exception:
            pass
        await query.message.reply_text(
            format_question_message(nq),
            reply_markup=build_question_keyboard(nq["id"]),
        )
        return

    # Finished all questions
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    answers = ud.get("answers", [])
    score = sum(1 for a in answers if a["is_correct"])
    level_label, level_key = score_to_level(score)
    wrong_topics = sorted({a["topic"] for a in answers if not a["is_correct"]})
    intro = ud.get("intro_answers", {})

    if wrong_topics:
        wrong_block = "Темы для повторения (по ошибкам):\n" + "\n".join(
            f"• {t}" for t in wrong_topics
        )
    else:
        wrong_block = "Темы для повторения по ошибкам: нечего — все ответы верные."

    intro_lines = "\n".join(
        f"• {INTRO_LABELS_RU.get(k, k)}: {v}" for k, v in intro.items()
    )

    result_text = (
        "📊 Результаты теста\n\n"
        f"Правильных ответов: {score} из {len(QUESTIONS)}\n"
        f"Уровень по шкале теста: {level_label}\n\n"
        f"{wrong_block}\n\n"
        "Твои ответы в начале:\n"
        f"{intro_lines}\n\n"
        f"{LEVEL_TEXTS[level_key]}"
    )

    for chunk in _split_telegram_text(result_text, 4000):
        await query.message.reply_text(chunk)

    cta = (
        f"{CTA_TEXT}\n\n"
        "Напиши одним сообщением свой @username в Telegram (или номер), "
        "если хочешь, чтобы с тобой связались. Или отправь /skip."
    )
    await query.message.reply_text(cta)
    ud["phase"] = "lead"


def _split_telegram_text(s: str, max_len: int) -> list[str]:
    if len(s) <= max_len:
        return [s]
    parts: list[str] = []
    rest = s
    while rest:
        parts.append(rest[:max_len])
        rest = rest[max_len:]
    return parts


async def skip_lead(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ud = context.user_data
    if ud.get("phase") == "lead":
        ud["phase"] = "done"
        await update.effective_message.reply_text("Хорошо, без контакта.")


def main() -> None:
    load_dotenv()
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise SystemExit("Задайте переменную окружения BOT_TOKEN")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cmd_cancel))
    app.add_handler(CommandHandler("skip", skip_lead))
    app.add_handler(CallbackQueryHandler(on_quiz_answer, pattern=r"^q:\d+:[abc]$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    logger.info("Бот запущен")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
