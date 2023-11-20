LEXICON_ANSWERS: dict[str, str] = {
    '/start': 'Добрый день! Чем мы можем вам помочь?(выберите один из пунктов меню)',
    '/menu': 'Добрый день! Чем мы можем вам помочь?(выберите один из пунктов меню)',
    '/home_assistant': '<b><a href="https://www.home-assistant.io/docs/">Документация для Home Assistant</a></b>',
    '/docs_install': '<b><a href="https://емеля.рф/instructions/">Инструкция по установке</a></b>',
    '/info': 'Выберете из один из пунктов меню.',
    '/operator': 'Соединяем с оператором.',
}

LEXICON_MAIN_MENU_COMMANDS: dict[str, str] = {
    '/menu': 'Главное меню',
    '/info': 'Что умеет Емеля?',
    # '/advantages': 'Преимущества',
    '/contacts': 'Контакты',
    '/docs_install': 'Инструкция по установке',
    '/home_assistant': 'Home Assistant',
    '/operator': 'Связь с оператором',
    '/send_feedback': 'Отправить форму обратной связи',
}

INFO_BUTTONS: list[str] = [
    'Возможности',
    'Функции',
    'Интерфейс'
]

INLINE_BUTTON_COMMANDS: dict[str, str] = {
    'info': 'Что умеет Емеля?',
    'advantages': 'Преимущества',
    'contacts': 'Контакты',
    'opportunities': 'Возможности',
    'functionality': 'Функции',
    'interface': 'Интерфейс'
}

LEXICON_ADVANTAGES: dict[str: str, str: list[str]] = {
    'photo': 'pictures/advantages.png',
    'advantages': [
        '<b>НЕЗАВИСИМОСТЬ ОТ БРЕНДОВ</b>\n'
        'Производители ограничивают потребителей оборудованием только из своей экосистемой, '
        'а мы создаём экосистему именно вашего дома, поэтому можем использовать '
        'оборудование от Aqara, Tuya, Sonoff, Rubetek или любого другого бренда.',
        '<b>МАКСИМАЛЬНАЯ ПРОЗРАЧНОСТЬ</b>\n'
        'Вы всегда можете проверить стоимость приобретаемого нами оборудования, '
        'а также наблюдать за ходом проекта.',
        '<b>ОТКРЫТАЯ ПЛАТФОРМА</b>\n'
        'Мы строим экосистему на платформе с открытым исходным кодом — никаких ограничений и санкций.',
        '<b>КОНФИДЕНЦИАЛЬНОСТЬ</b>\n'
        'Сервер расположен у вас дома, а не в чужих облаках, поэтому вы получаете не только самый '
        'быстрый отклик на команды, но и полную конфиденциальность.'
    ]
}

LEXICON_CONTACTS: dict[str: str, str: list[str]] = {
    'photo': 'pictures/logo.png',
    'contacts': 'Мы открыты к диалогу и готовы рассчитать ваш проект.\n\n'
                'Работаем без выходных с 08:00 до 20:00\n\n'
                '8-800-500-48-52 (Звонок по России бесплатный)\n'
                'WhatsApp: +7-999-2200-431\n'
                'E-mail: dom@емеля.рф\n\n'
                'Или свяжитесь с оператором в данном чате.'
}
