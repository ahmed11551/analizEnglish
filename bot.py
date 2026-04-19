"""
Telegram-бот: тест English Grammar & Usage (B2), уровень и темы для повторения.
Запуск из каталога проекта: python bot.py
"""

from __future__ import annotations

import logging
import re
import sys
from typing import Any

from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.constants import ChatAction
from telegram.error import BadRequest, NetworkError, TimedOut
from telegram.request import HTTPXRequest
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import (
    BOT_TOKEN,
    BRAND_SUBTITLE,
    BRAND_TITLE,
    LOG_LEVEL,
    MINI_APP_URL,
    TELEGRAM_PROXY,
    WEBSITE_URL,
)
from leads import append_lead, build_lead_record
from questions_data import (
    CTA_TEXT,
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


def _session_summary(ud: dict[str, Any]) -> tuple[int, str, list[str]]:
    answers = ud.get("answers", [])
    score = sum(1 for a in answers if a["is_correct"])
    level_label, _ = score_to_level(score)
    wrong = sorted({a["topic"] for a in answers if not a["is_correct"]})
    return score, level_label, wrong


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


def build_cta_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("Перейти на сайт", url=WEBSITE_URL)],
    ]
    if MINI_APP_URL:
        buttons.append(
            [InlineKeyboardButton("Открыть мини-приложение", web_app=WebAppInfo(url=MINI_APP_URL))]
        )
    return InlineKeyboardMarkup(buttons)


def format_question_message(q: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"{q['id']}. {q['text']}")
    opts = q["options"]
    lines.append(f"a) {opts['a']}")
    lines.append(f"b) {opts['b']}")
    lines.append(f"c) {opts['c']}")
    lines.append("")
    lines.append(f"Вопрос {q['id']} из {len(QUESTIONS)}")
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
            BotCommand("miniapp", "Открыть мини-приложение"),
            BotCommand("help", "Справка и команды"),
            BotCommand("cancel", "Прервать тест"),
            BotCommand("skip", "Пропустить шаг с контактом"),
        ]
    )
    me = await application.bot.get_me()
    logger.info("Бот @%s запущен (id=%s)", me.username, me.id)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    err = context.error
    if isinstance(err, (TimedOut, NetworkError)):
        logger.warning("Сеть Telegram: %s", err)
        return
    if isinstance(err, BadRequest):
        msg = str(err).lower()
        if "query is too old" in msg or "message is not modified" in msg:
            logger.info("BadRequest (ожидаемо): %s", err)
            return
    logger.exception("Ошибка при обработке update: %s", err)
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
    ud["phase"] = "quiz"
    ud["q_index"] = 0
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
        "Этот тест покажет твой уровень и какие темы стоит повторить."
    )
    q = QUESTIONS[0]
    await update.effective_message.reply_text(title)
    await update.effective_message.reply_text(
        format_question_message(q),
        reply_markup=build_question_keyboard(q["id"]),
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    text = (
        f"{BRAND_TITLE}\n\n"
        "• /start — пройти тест с начала (текущий прогресс сбросится)\n"
        "• /miniapp — открыть mini app с тестом (web/mobile)\n"
        "• /cancel — прервать тест\n"
        "• /skip — после результатов пропустить отправку контакта менеджерам\n\n"
        "Если чат Telegram работает нестабильно, пройди тест в mini app."
    )
    await update.effective_message.reply_text(text)


async def open_miniapp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    if MINI_APP_URL:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Открыть мини-приложение",
                        web_app=WebAppInfo(url=MINI_APP_URL),
                    )
                ],
                [InlineKeyboardButton("Перейти на сайт", url=WEBSITE_URL)],
            ]
        )
        await update.effective_message.reply_text(
            "Мини-приложение готово. Пройди тест в удобном формате (web/mobile).",
            reply_markup=keyboard,
        )
        return

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Перейти на сайт", url=WEBSITE_URL)]]
    )
    await update.effective_message.reply_text(
        "Ссылка на mini app ещё не настроена. Пока можешь пройти тест на сайте.",
        reply_markup=keyboard,
    )


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

    if phase == "lead":
        ud["lead_contact"] = text
        ud["phase"] = "done"
        await update.message.reply_text(
            "Спасибо! Менеджер свяжется с тобой в Telegram.",
        )
        u = update.effective_user
        score, level_label, wrong = _session_summary(ud)
        try:
            append_lead(
                build_lead_record(
                    user_id=u.id if u else None,
                    username=u.username if u else None,
                    first_name=u.first_name if u else None,
                    contact=text.strip(),
                    skipped=False,
                    intro={},
                    score=score,
                    level_label=level_label,
                    wrong_topics=wrong,
                )
            )
        except OSError:
            logger.exception("Не удалось записать лид в файл")
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


async def on_quiz_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
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

    m = re.match(r"^q:(\d+):([abc])$", query.data)
    if not m:
        await query.answer()
        return

    qid = int(m.group(1))
    chosen = m.group(2)
    q = QUESTIONS[ud.get("q_index", 0)]
    if q["id"] != qid:
        await query.answer(
            "Это не текущий вопрос. Нажми /start.",
            show_alert=True,
        )
        return

    await query.answer()

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

    if wrong_topics:
        mistakes_block = "Темы, где были ошибки:\n" + "\n".join(f"• {t}" for t in wrong_topics)
        revise_block = "Какие темы повторить:\n" + "\n".join(f"• {t}" for t in wrong_topics)
    else:
        mistakes_block = "Темы, где были ошибки:\n• Ошибок нет — отличный результат."
        revise_block = "Какие темы повторить:\n• Можно переходить к более сложным темам (B2+/C1)."

    result_text = (
        "📊 Результаты теста\n\n"
        f"Правильных ответов: {score} из {len(QUESTIONS)}\n"
        f"Твой уровень: {level_label}\n\n"
        f"{mistakes_block}\n\n"
        f"{revise_block}\n\n"
        f"{LEVEL_TEXTS[level_key]}"
    )

    try:
        await context.bot.send_chat_action(
            chat_id=query.message.chat_id,
            action=ChatAction.TYPING,
        )
    except Exception:
        logger.debug("send_chat_action failed", exc_info=True)

    for chunk in split_telegram_chunks(result_text):
        await query.message.reply_text(chunk)

    await query.message.reply_text(CTA_TEXT, reply_markup=build_cta_keyboard())
    await query.message.reply_text(
        "Если хочешь, чтобы с тобой связались, напиши одним сообщением свой "
        "@username в Telegram (или номер). Или отправь /skip."
    )
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
        u = update.effective_user
        score, level_label, wrong = _session_summary(ud)
        try:
            append_lead(
                build_lead_record(
                    user_id=u.id if u else None,
                    username=u.username if u else None,
                    first_name=u.first_name if u else None,
                    contact=None,
                    skipped=True,
                    intro={},
                    score=score,
                    level_label=level_label,
                    wrong_topics=wrong,
                )
            )
        except OSError:
            logger.exception("Не удалось записать лид (skip) в файл")
        logger.info(
            "Lead skipped: user_id=%s",
            u.id if u else None,
        )
    else:
        await update.effective_message.reply_text(
            "/skip доступна после результатов, когда бот просит оставить контакт."
        )


def create_application() -> Application:
    """Сборка Application для polling (локально или на VPS)."""
    if not BOT_TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN. Создай `.env` в корне проекта (см. `.env.example`).")

    req_kw: dict[str, Any] = {
        "connect_timeout": 45.0,
        "read_timeout": 45.0,
        "write_timeout": 45.0,
        "pool_timeout": 15.0,
    }
    if TELEGRAM_PROXY:
        req_kw["proxy"] = TELEGRAM_PROXY
        logger.info("Используется TELEGRAM_PROXY для запросов к Telegram API")
    request = HTTPXRequest(**req_kw)

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)
        .post_init(post_init)
        .build()
    )
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("miniapp", open_miniapp))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("cancel", cmd_cancel))
    app.add_handler(CommandHandler("skip", skip_lead))
    app.add_handler(CallbackQueryHandler(on_quiz_answer, pattern=r"^q:\d+:[abc]$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    return app


def main() -> None:
    try:
        app = create_application()
    except RuntimeError as e:
        logger.error("%s", e)
        sys.exit(1)

    logger.info("Polling… (при обрыве сети бот будет повторять подключение)")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        bootstrap_retries=-1,
    )


if __name__ == "__main__":
    main()
