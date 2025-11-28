def test_build_message_includes_character_and_rules(db_module, main_module, monkeypatch):
    db = db_module
    main = main_module

    uid = 42001
    characters = db.list_characters() if hasattr(db, 'list_characters') else db.list_characters()
    target = characters[0]
    db.set_user_character(uid, target['id'])

    msgs = main._build_messages(uid, 'Что такое API?')
    assert msgs[0]['role'] == 'system'
    sys = msgs[0]['content']

    assert target['name'] in sys
    assert 'Формат' in sys or 'Правила' in sys
    assert msgs[1]['role'] == 'user'
    assert 'Что такое API?' in msgs[1]['content']


def test_build_messages_users_default_character_when_not_set(db_module, main_module):
    db = db_module
    main = main_module

    uid = 50001
    question = 'Расскажи что-нибудь о себе'

    msgs = main._build_messages(uid, question)
    sys_text = msgs[0]['content']

    characters = db.list_characters()
    assert characters, 'Список персонажей пуст - проверить schema в db.py'
    names = {c['name'] for c in characters}

    assert any(name in sys_text for name in names), 'system должен содержать имя хоть какого-то персонажа'

    assert msgs[1]['role'] == 'user'
    assert question in msgs[1]['content']


def test_build_messages_for_character_pure_function(main_module):
    main = main_module

    uid = 65101
    character = {
        'id': 123,
        'name': 'Тестовый персонаж',
        'prompt': 'Отвечай коротко и по делу.',
    }
    question = 'Что такое интеграционный тест?'

    msgs = main._build_messages(uid, question, character)

    assert isinstance(msgs, list)
    assert msgs[0]['role'] == 'system'
    assert 'Тестовый персонаж' in msgs[0]['content']
    assert 'Отвечай коротко и по делу.' in msgs[0]['content']

    assert msgs[1]['role'] == 'user'
    assert question in msgs[1]['content']
