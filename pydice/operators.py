from abc import abstractmethod, ABC
from dataclasses import dataclass

from pydice.dice_result_builder import DiceResultBuilder


@dataclass
class Operator(ABC):
    accepted_operators = [
        "+"
    ]

    @abstractmethod
    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        pass


@dataclass
class AddOperator(Operator):
    value: int

    def add(self, dice_result_builder: DiceResultBuilder) -> DiceResultBuilder:
        return dice_result_builder.with_add_modifier(self.value)


class OperatorFactory:
    @staticmethod
    def get_operator(operator: str, value: int) -> Operator | None:
        if operator not in Operator.accepted_operators:
            return

        if operator == "+":
            return AddOperator(value)
