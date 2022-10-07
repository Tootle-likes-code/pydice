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

## Dice Pool

Is a collection of `Rollables` that handles all of them together in one place as a single `Rollable`.  The advantage is
that this allows multiple `Dice` objects to be used as a single rollable.

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

**NOTE:** This decorator uses the raw roll values, and ignores other prior `result()` calls.

### CountValuesEqualToDecorator
Counts the number of dice that roll a number.

**NOTE:** This decorator uses the raw roll values, and ignores other prior `result()` calls.

### CountValuesGreaterThanEqualToDecorator
Counts the number of dice that roll the target number or greater.

**NOTE:** This decorator uses the raw roll values, and ignores other prior `result()` calls.

# String Parser

The dice roller can be interacted with using a dice string to create a `RollResult`.  The best way to do that is through
the `dice_string_interpreter.interpret(string)` method.  You can run `dice_string_interpreter.py` with one as an
argument to return the `RollResult.result()`.

## Supported Operators

### `+`
When followed by a number, adds the number to the result.

### `-`
When followed by a number, subtracts the number from the result.

### `*` or `x`
When followed by a number, multiplies the result by the number.

### `/`
When followed by a number, divides the result by the number.

### `e`
When followed by a number, looks through the die rolls, and if the die rolled the given number, rolls it again.

### `=`
When followed by a number, looks through the die rolls and returns the number of die that rolled the target number.

### `>=`
When followed by a number, looks through the die rolls and returns the number of die that rolled the target number 
or greater.

## Special Dice Rolls
When the parser receives this, it triggers a pre-defined shortcut.  All of these can use the above `Operators`.

### `df`
Shortcut for FATE dice.

### `st`
Shortcut for Storyteller system dice.  Specifically, any roll of 7 or more is a success with a 10 counting for 2,
successes.  No successes, results in a botch.