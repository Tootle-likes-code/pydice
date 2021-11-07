from dataclasses import dataclass

from die import Die


@dataclass
class RollResult:
    die: Die
    roll: int

