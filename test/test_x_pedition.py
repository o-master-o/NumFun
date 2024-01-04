import pytest

from x_pedition import ExpressionGenerator


@pytest.fixture
def random(mocker):
    return mocker.patch('x_pedition.random')


@pytest.fixture
def randint(random):

    def randint_value_mock(randint_values, choice_value):
        random.randint.side_effect = randint_values
        random.choice.return_value = choice_value
        return random

    return randint_value_mock


@pytest.mark.parametrize('result, a, x, expected_expression', [
    (10, 3, 3, 'x + 7 = 10'),
    (1, 1, 0, '1 + x = 1'),
    (50, 10, 50, '10 + 40 = x'),
    (11, 11, 0, '11 + x = 11'),
    (20, 0, 0, 'x + 20 = 20'),
])
def test_expression_generator_generate_sum_returns_correct_expressions(randint, result, a, x, expected_expression):
    randint([result, a], x)
    expression, returned_x = ExpressionGenerator(50).generate_sum()
    assert expected_expression == expression
    assert x == returned_x


@pytest.mark.parametrize('max_number, normalized_max_number', [
    (1001, 1000),
    (2000, 1000),
    (1000, 1000),
    (10, 10),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-10, 1),

])
def test_expression_generator_generate_sum_limits_max_value(random, max_number, normalized_max_number):
    ExpressionGenerator(max_number).generate_sum()
    random.randint.assert_any_call(1, normalized_max_number)
