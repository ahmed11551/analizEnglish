"""
Telegram-бот: тест English Grammar & Usage (B2), анкета, уровень и темы для повторения.
Запуск из каталога проекта: python bot.py
"""

from __future__ import annotations

import logging
import re
import sys
from typing import Any

from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN, BRAND_SUBTITLE, BRAND_TITLE, LOG_LEVEL
from questions_data import (
    CTA_TEXT,
    INTRO_FIELDS,
    INTRO_LABELS_RU,
    LEVEL_BANDS,
    LEVEL_TEXTS,
    QUESTIONS,
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=getattr(logging, LOG_LEVEL, logging.INFO),
)
logger = logging.getLogger(__name__)

TELEGRAM_TEXT_LIMIT = 4000


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


def split_telegram_chunks(text: str, max_len: int = TELEGRAM_TEXT_LIMIT) -> list[str]:
    """Дробит текст по абзацам, чтобы не резать посередине смысла, если возможно."""
    if len(text) <= max_len:
        return [text]
    chunks: list[str] = []
    buf = ""
    for para in text.split("\n\n"):
        candidate = para if not buf else f"{buf}\n\n{para}"
        if len(candidate) <= max_len:
            buf = candidate
            continue
        if buf:
            chunks.append(buf)
            buf = ""
        if len(para) <= max_len:
            buf = para
            continue
        start = 0
        while start < len(para):
            piece = para[start : start + max_len]
            chunks.append(piece)
            start += max_len
    if buf:
        chunks.append(buf)
    return chunks


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Начать тест"),
            BotCommand("help", "Справка и команды"),
            BotCommand("cancel", "Прервать тест"),
            BotCommand("skip", "Пропустить шаг с контактом"),
        ]
    )
    me = await application.bot.get_me()
    logger.info("Бот @%s запущен (id=%s)", me.username, me.id)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Ошибка при обработке update: %s", context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "Произошла техническая ошибка. Попробуй ещё раз или напиши /start."
            )
        except Exception:
            logger.exception("Не удалось отправить сообщение об ошибке")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    ud = context.user_data
    ud.clear()
    ud["phase"] = "intro"
    ud["intro_step"] = 0
    ud["intro_answers"] = {}
    ud["answers"] = []

    user = update.effective_user
    if user:
        logger.info(
            "Старт теста: user_id=%s username=%s",
            user.id,
            user.username or "",
        )

    title = (
        f"📘 {BRAND_TITLE}\n"
        f"{BRAND_SUBTITLE}\n\n"
        "Этот тест покажет твой уровень и какие темы стоит повторить.\n\n"
        "Пару слов о себе перед началом теста:"
    )
    _, prompt = INTRO_FIELDS[0]
    await update.effective_message.reply_text(f"{title}\n\n{prompt}")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    text = (
        f"{BRAND_TITLE}\n\n"
        "• /start — пройти тест с начала (текущий прогресс сбросится)\n"
        "• /cancel — прервать тест\n"
        "• /skip — после результатов пропустить отправку контакта менеджерам\n\n"
        "Вопросы с вариантами a, b, c — нажми кнопку под сообщением."
    )
    await update.effective_message.reply_text(text)


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    context.user_data.clear()
    await update.effective_message.reply_text(
        "Тест прерван. Чтобы начать заново, отправь /start."
    )


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

    if phase == "quiz":
        await update.message.reply_text(
            "Сейчас нужно выбрать ответ кнопкой a, b или c под вопросом."
        )
        return

    await update.message.reply_text(
        "Чтобы пройти тест, отправь /start."
    )


async def on_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    ud = context.user_data

    if ud.get("phase") != "quiz":
        await query.answer(
            "Сессия сброшена или тест уже завершён. Нажми /start.",
            show_alert=True,
        )
        return

    await query.answer()

    m = re.match(r"^q:(\d+):([abc])$", query.data)
    if not m:
        return
    qid = int(m.group(1))
    chosen = m.group(2)
    q = QUESTIONS[ud.get("q_index", 0)]
    if q["id"] != qid:
        await query.answer("Это устаревший вопрос. Нажми /start.", show_alert=True)
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
            logger.debug("Не удалось убрать клавиатуру у сообщения", exc_info=True)
        await query.message.reply_text(
            format_question_message(nq),
            reply_markup=build_question_keyboard(nq["id"]),
        )
        return

    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        logger.debug("Не удалось убрать клавиатуру у сообщения", exc_info=True)

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

    for chunk in split_telegram_chunks(result_text):
        await query.message.reply_text(chunk)

    cta = (
        f"{CTA_TEXT}\n\n"
        "Напиши одним сообщением свой @username в Telegram (или номер), "
        "если хочешь, чтобы с тобой связались. Или отправь /skip."
    )
    await query.message.reply_text(cta)
    ud["phase"] = "lead"

    logger.info(
        "Тест завершён: user_id=%s score=%s/%s level=%s wrong_topics=%s",
        query.from_user.id if query.from_user else None,
        score,
        len(QUESTIONS),
        level_label,
        wrong_topics,
    )


async def skip_lead(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    ud = context.user_data
    if ud.get("phase") == "lead":
        ud["phase"] = "done"
        await update.effective_message.reply_text("Хорошо, без контакта.")


def main() -> None:
    if not BOT_TOKEN:
        logger.error("Не задан BOT_TOKEN. Создай файл .env по образцу .env.example.")
        sys.exit(1)

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("cancel", cmd_cancel))
    app.add_handler(CommandHandler("skip", skip_lead))
    app.add_handler(CallbackQueryHandler(on_quiz_answer, pattern=r"^q:\d+:[abc]$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    logger.info("Polling…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
