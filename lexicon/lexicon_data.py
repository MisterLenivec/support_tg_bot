BASE_COMMANDS = ["start", "menu", "operator", "send_feedback", "info", "contacts", "home_assistant", "docs_install"]
LEXICON_ANSWERS: dict[str, str] = {
    "/start": "Добрый день! Чем мы можем вам помочь?(выберите один из пунктов меню)",
    "/menu": "Добрый день! Чем мы можем вам помочь?(выберите один из пунктов меню)",
    "/home_assistant": '<b><a href="https://www.home-assistant.io/docs/">Документация для Home Assistant</a></b>',
    "/docs_install": '<b><a href="https://емеля.рф/instructions/">Инструкция по установке</a></b>',
    "/info": "Выберете из один из пунктов меню.",
    "/operator": "Соединяем с оператором.",
}

LEXICON_MAIN_MENU_COMMANDS: dict[str, str] = {
    "/menu": "Главное меню",
    "/info": "Что умеет Емеля?",
    # '/advantages': 'Преимущества',
    "/contacts": "Контакты",
    "/docs_install": "Инструкция по установке",
    "/home_assistant": "Home Assistant",
    "/operator": "Связь с оператором",
    "/send_feedback": "Отправить форму обратной связи",
}

INFO_BUTTONS: list[str] = ["Возможности", "Функции", "Интерфейс"]

INLINE_BUTTON_COMMANDS: dict[str, str] = {
    "info": "Что умеет Емеля?",
    "advantages": "Преимущества",
    "contacts": "Контакты",
    "opportunities": "Возможности",
    "functionality": "Функции",
    "interface": "Интерфейс",
    # "cancel": "Выйти из заполнения формы",
}

REPLY_BUTTON_COMMANDS: dict[str, str] = {
    "cancel_feedback": "Отменить заполнение формы",
    "cancel_operator": "Завершить диалог с оператором",
}
