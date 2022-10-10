from abc import abstractmethod, ABC
from dataclasses import dataclass

from pydice.roll_result_builder import RollResultBuilder


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
