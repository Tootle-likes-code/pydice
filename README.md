# pydice

Code Repository for dice rollers of all kinds.

# Rollables

The package uses 'Rollables' to randomly determine numbers.  `Rollable` itself is an abstract class with one
method, `roll` and two properties, `min` and `max`. The two implmentations are `Die` and `Dice`.

When rolling a `Rollable`, a `list` of `int` is returned, representing the numbers rolled.

## Die

`Die` is a representation of a single Polyhedral dice. In that the die it represents goes from `min` to `max` in a
linear fashion. As such, if no `minimum_roll` is defined on initialisation it will default to `1`.

### FATE Die

`FateDie` is a specific implementation of `Die` for the FATE system (Evil Hat Games). It represents this by using
a `Die` with `-1` to `1` as the number.

## Dice

The other base `Rollable`. This represents a group of multiple related `Die` objects.

The `roll()` result of `Dice` represents a single `Die` result.

# Roll Results

A `RollResult` is a helper class to better handle the results of a `Rollable.roll()`. It has the `die_rolls` property
which, representing the base roll of each `Die`, and there is a `result()` method that gives a total of the rolled die.

There is an implementation of the abstract `RollResult` for both `Die` and `Dice`.

# Roll Result Decorators

These are modifiers that can be applied to a `RollResult` allowing for modifications to be applied to the `RollResult`
modifying the `result()` method to allow it to account for various things.  

The decorators do not apply any die-application logic beyond calling the `result()` method of the nested `RollResult`, 
as per decorator pattern.

## Decorators
Here is a list of available decorators:

### AddToRollResultDecorator
Adds a `modifier` int to `result()`.

### SubtractFromRollResultDecorator
Subtracts a `modifier` int from `result()`.

### MultiplyRollResultDecorator
Multiplies the `result()` by a `modifier` int.

### DivideByRollResultDecorator
Divides the `result()` by a modifier int.

### ExplodeDiceForTargetDecorator
A decorator for exploding dice.

> Exploding Dice: When a die hits a particular number, then roll another and add it to the running total.

Goes through the `RollResults.die_rolls` and any result that is the same as the `target_number`, it will roll another 
die.  This will explode near infinitely.