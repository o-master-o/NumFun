import pytest

from num_fun.games.x_pedition import ExpressionGenerator


@pytest.fixture
def random(mocker):
    return mocker.patch('num_fun.games.x_pedition.random')


@pytest.fixture
def randint(random):

    def randint_value_mock(randint_values, choice_value):
        random.randint.side_effect = randint_values
        random.choice.return_value = choice_value
        return random

    return randint_value_mock


@pytest.fixture
def sut():
    return ExpressionGenerator()


@pytest.fixture
def sut_max_50(sut):
    sut.max_number = 50
    return sut


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
def test_expression_generator_generate_sum_limits_max_value(sut, random, max_number, normalized_max_number):
    sut.max_number = max_number
    assert normalized_max_number == sut.max_number


@pytest.mark.parametrize('result, a, x_position, expected_expression, x', [
    (10, 3, 'a', 'x + 7 = 10', 3),
    (1, 1, 'b', '1 + x = 1', 0),
    (50, 10, 'result', '10 + 40 = x', 50),
    (11, 11, 'b', '11 + x = 11', 0),
    (20, 0, 'a', 'x + 20 = 20', 0),
])
def test_expression_generator_generate_sum_returns_correct_expressions(sut_max_50, randint, result, a, x_position, expected_expression, x):
    randint([result, a], x_position)
    expression, returned_x = sut_max_50.generate_sum()
    assert expected_expression == expression
    assert x == returned_x


@pytest.mark.parametrize('a, b, x_position, expected_expression, x', [
    (10, 3, 'a', 'x - 3 = 7', 10),
    (1, 1, 'b', '1 - x = 0', 1),
    (50, 40, 'result', '50 - 40 = x', 10),
    (11, 0, 'b', '11 - x = 11', 0),
])
def test_expression_generator_generate_subtraction_returns_correct_expressions(sut_max_50, randint, a, b, x_position, expected_expression, x):
    randint([a, b], x_position)
    expression, returned_x = sut_max_50.generate_subtraction()
    assert expected_expression == expression
    assert x == returned_x


@pytest.mark.parametrize('a, b, x_position, expected_expression, x', [
    (10, 3, 'a', 'x * 3 = 30', 10),
    (1, 1, 'b', '1 * x = 1', 1),
    (5, 10, 'result', '5 * 10 = x', 50),
    (11, 0, 'b', '11 * x = 0', 0),
])
def test_expression_generator_generate_multiplication_returns_correct_expressions(sut_max_50, randint, a, b, x_position, expected_expression, x):
    randint([a, b], x_position)
    expression, returned_x = sut_max_50.generate_multiplication()
    assert expected_expression == expression
    assert x == returned_x


@pytest.mark.parametrize('result, b, x_position, expected_expression, x', [
    (3, 5, 'a', 'x / 5 = 3', 15),
    (1, 1, 'b', '1 / x = 1', 1),
    (5, 5, 'result', '25 / 5 = x', 5),
])
def test_expression_generator_generate_division_returns_correct_expressions(sut_max_50, randint, result, b, x_position, expected_expression, x):
    randint([result, b], x_position)
    expression, returned_x = sut_max_50.generate_division()
    assert expected_expression == expression
    assert x == returned_x
