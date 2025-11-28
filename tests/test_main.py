from unittest.mock import MagicMock


def test_parse_number_integers(main_module):
    assert main_module._parse_number("1 2 3") == [1, 2, 3]
    assert main_module._parse_number("10 100 500") == [10, 100, 500]


def test_parse_number_with_commas(main_module):
    assert main_module._parse_number("1,2,3") == [1, 2, 3]
    assert main_module._parse_number("1, 2, 3") == [1, 2, 3]


def test_parse_number_mixed_text(main_module):
    assert main_module._parse_number("test 10 check 5") == [10, 5]
    assert main_module._parse_number("/sum 123 456") == [123, 456]


def test_parse_number_negatives(main_module):
    assert main_module._parse_number("-5 -10 3") == [-5, -10, 3]
    assert main_module._parse_number("-1") == [-1]


def test_parse_number_empty(main_module):
    assert main_module._parse_number("") == []
    assert main_module._parse_number("hello world") == []
    assert main_module._parse_number("one two three") == []


def test_parse_number_logging(main_module, monkeypatch):
    mock_logger = MagicMock()
    monkeypatch.setattr(main_module, 'logger', mock_logger)

    main_module._parse_number("1 2")

    assert mock_logger.debug.called
    args, _ = mock_logger.debug.call_args
    assert "Parsing numbers" in args[0]


def test_sum_process_valid(main_module):
    assert main_module._sum_process("1 2 3") == "Сумма: 6"
    assert main_module._sum_process("10 -5") == "Сумма: 5"


def test_sum_process_single(main_module):
    assert main_module._sum_process("100") == "Сумма: 100"


def test_sum_process_empty(main_module):
    expected_msg = 'В сообщении нет цифр.\nПример использования команды: /sum 2 3 10'
    assert main_module._sum_process("abc") == expected_msg
    assert main_module._sum_process("") == expected_msg


def test_sum_process_logging(main_module, monkeypatch):
    mock_logger = MagicMock()
    monkeypatch.setattr(main_module, 'logger', mock_logger)

    main_module._sum_process("5 5")

    assert mock_logger.debug.called
    args, _ = mock_logger.debug.call_args
    assert "Summation of numbers" in args[0]


def test_max_process_valid(main_module):
    assert main_module._max_process("1 5 2") == "Максимум: 5"
    assert main_module._max_process("10 100 1") == "Максимум: 100"


def test_max_process_negatives(main_module):
    assert main_module._max_process("-10 -5 -20") == "Максимум: -5"


def test_max_process_mixed_signs(main_module):
    assert main_module._max_process("-10 5 -20") == "Максимум: 5"


def test_max_process_empty(main_module):
    expected_msg = 'В сообщении нет цифр.\nПример использования команды: /max 1 3 7'
    assert main_module._max_process("no numbers") == expected_msg


def test_max_process_logging(main_module, monkeypatch):
    mock_logger = MagicMock()
    monkeypatch.setattr(main_module, 'logger', mock_logger)

    main_module._max_process("1 2")

    assert mock_logger.debug.called
    args, _ = mock_logger.debug.call_args
    assert "Maximum numbers" in args[0]