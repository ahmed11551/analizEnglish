"""Проверка ответов анкеты перед началом теста."""

from __future__ import annotations

INTRO_ANSWER_MAX = 600


def validate_intro_answer(field_key: str, raw: str) -> tuple[bool, str]:
    s = raw.strip()
    if not s:
        return False, "Ответ не может быть пустым. Напиши коротко по смыслу вопроса."
    if len(s) > INTRO_ANSWER_MAX:
        return (
            False,
            f"Слишком длинно (не больше {INTRO_ANSWER_MAX} символов). Сократи ответ.",
        )
    if field_key == "age":
        if not s.isdigit():
            return False, "Напиши возраст одним числом, например: 22"
        n = int(s)
        if n < 6 or n > 120:
            return False, "Введи возраст числом от 6 до 120."
    return True, ""
