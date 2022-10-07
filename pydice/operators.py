from abc import abstractmethod, ABC
from dataclasses import dataclass

from pydice.dice_result_builder import DiceResultBuilder


@dataclass
class Operator(ABC):
    value: int

    accepted_operators = [
        "+",
        "-",
        "*",
        "x",
        "/",
        "=",
        ">=",
        "e"
    ]

    @abstractmethod
    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        pass


@dataclass
class AddOperator(Operator):
    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        return dice_result_builder.with_add_modifier(self.value)


@dataclass
class SubtractOperator(Operator):
    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        return dice_result_builder.with_subtract_modifier(self.value)


@dataclass
class MultiplyOperator(Operator):
    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        return dice_result_builder.with_multiply_modifier(self.value)


@dataclass
class DivideOperator(Operator):
    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        return dice_result_builder.with_divide_modifier(self.value)


@dataclass
class ExplodingOperator(Operator):
    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        return dice_result_builder.with_exploding_modifier(self.value)


@dataclass
class EqualToOperator(Operator):
    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        return dice_result_builder.with_count_values_equal_to(self.value)


class GreaterThanEqualToOperator(Operator):
    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        return dice_result_builder.with_count_values_greater_than_equal_to(self.value)


class OperatorFactory:
    @staticmethod
    def get_operator(operator: str, value: int) -> Operator | None:
        if operator.lower() not in Operator.accepted_operators:
            return

        if operator == "+":
            return AddOperator(value)
        if operator == "-":
            return SubtractOperator(value)
        if operator == "*" or operator.lower() == "x":
            return MultiplyOperator(value)
        if operator == "/":
            return DivideOperator(value)
        if operator == "=":
            return EqualToOperator(value)
        if operator == ">=":
            return GreaterThanEqualToOperator(value)
        if operator == "e":
            return ExplodingOperator(value)
