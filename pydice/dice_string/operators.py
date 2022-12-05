from abc import abstractmethod, ABC
from dataclasses import dataclass

from pydice.roll_result_operators.roll_result_builder import RollResultBuilder


@dataclass
class Operator(ABC):
    value: int

    @abstractmethod
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        pass


class AddOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_add_modifier(self.value)


class SubtractOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_subtract_modifier(self.value)


class MultiplyOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_multiply_modifier(self.value)


class DivideOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_divide_modifier(self.value)


class ExplodingOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_exploding_modifier(self.value)


class EqualToOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_count_values_equal_to(self.value)


class NotEqualToOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_not_equals_to(self.value)


class GreaterThanOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_count_values_greater_than(self.value)


class GreaterThanEqualToOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_count_values_greater_than_equal_to(self.value)


class LessThanOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_count_values_less_than(self.value)


class LessThanEqualToOperator(Operator):
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        return builder.with_count_values_less_than_equal_to(self.value)


ACCEPTED_OPERATORS: dict[str, type] = {
    "+": AddOperator,
    "-": SubtractOperator,
    "*": MultiplyOperator,
    "x": MultiplyOperator,
    "/": DivideOperator,
    "=": EqualToOperator,
    "!=": NotEqualToOperator,
    "=/=": NotEqualToOperator,
    ">": GreaterThanOperator,
    ">=": GreaterThanEqualToOperator,
    "<": LessThanOperator,
    "<=": LessThanEqualToOperator,
    "e": ExplodingOperator
}


class OperatorFactory:
    @staticmethod
    def get_operator(operator: str, value: int) -> Operator | None:
        if operator.lower() not in ACCEPTED_OPERATORS:
            return

        return ACCEPTED_OPERATORS[operator.lower()](value)

    @staticmethod
    def get_operators(operator_string: str) -> list[Operator]:
        operator = ""
        value = ""
        operators: list[Operator] = []

        for index, character in enumerate(operator_string):
            if not character.isnumeric():
                operator += character
                continue

            if index == len(operator_string):
                break

            next_character = operator_string[index + 1:index + 2]
            if index != len(operator_string) and next_character.isnumeric():
                value = character
                continue
            value += character
            built_operator = OperatorFactory.get_operator(operator, int(value))
            if built_operator is not None:
                operators.append(built_operator)
            operator = ""
            value = ""

        return operators

    @staticmethod
    def get_storyteller_operators() -> list[Operator]:
        return [EqualToOperator(10), GreaterThanEqualToOperator(7)]
