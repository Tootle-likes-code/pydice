# pydice

Code Repository for dice rollers of all kinds.  The sections are:

* How to use the String Parser - Which details how to get pydice to parse dice strings.  This is a how-to section to use the 
String Parser.
* Rollables - Explains pydice's abstractions of dice to work in a digital form.
* Roll Results - Explains the mechanism for handling the rolled Rollable.
* Roll Result Decorators - Explains the decorators that can be applied to the Roll Results to transform the initial
Roll Result based on the decorators.

# How to use the String Parser

The dice roller can be interacted with using a dice string to create a `RollResult`.  The best way to do that is through
the `dice_string_interpreter.interpret(string)` method.  You can run `main.py` with a dice string as an
argument to return the `RollResult.result()`.

## Using the String Parser
All dice strings start off with a string representing the die or dice you want to roll.  These need to be the first
part of the dice string, else it won't work.  The simplest way to represent the dice is:

`[number of dice]d[size of dice]`

Where `[number of dice]` and `[size of dice]` are replaced by whole numbers.  `[number of dice]` is optional, where it 
omitted, the parser  assumes only `1`die is to be rolled.  Some example dice strings are:

```
1d20
10d10
6d6
1d100
d6
d20
```

## Supported Operators
The operators below work when following a dice string and mutate the result of the dice that are rolled to provide
different results.  There are loads of potential mutations required by users.  These mutations are handled by pydice
through Operators.  There are various Operators that fit into broad 'types' of operations.  These are explained below.

**NOTE:** Operations occur from right to left.  So the die/dice are rolled and then the Operators are applied in order.
This means that some combination of operators don't work.  For example, `10d10+7>=7`, the `+7` will be ignored by the
`=7` modifier, as it's a Counter Operator (see below for details).

### Result Operators
Each of these operators will look at the mathematical result of the string being parsed, and then modify that
accordingly.

#### `+`
When followed by a number, adds the number to the result.

For Example:

```
1d20+5
```

Assuming the 1d20 rolled `15`, the final result will be `20`.

#### `-`
When followed by a number, subtracts the number from the result.

For Example:

```
1d20-5
```

Assuming the 1d20 rolled `15`, the final result will be `10`.

#### `*` or `x`
When followed by a number, multiplies the result by the number.

For Example:

```
1d20*5
Is the same as:
1d20x5
```

Assuming the 1d20 rolled `5`, the final result will be `25`.

#### `/`
When followed by a number, divides the result by the number.

For Example:

```
1d20/5
```

Assuming the 1d20 rolled `15`, the final result will be `3`.

### Die Roll Based
These operators look at the dice rolled instead of the results of the dice.

#### `e`
When followed by a number, looks through the die rolls, and if the die rolled the given number, rolls it again, adding
it to the rolled dice.

For Example:

```
5d10e10
```

Assuming the 10d10 rolled `[10, 1, 5, 6, 7]` initially, another `d10` would be rolled, assuming this was another `10`,
that would roll another `d10`, which in this case results in a `2`.  That gives us a final result of `41` 
(`10+1+5+6+7+10+2=41`).

#### Counter Operators
All of these operators are Dice Based will count values of results on the die_rolls.  They can be chained with each other, 
but will ignore other none die roll based 

##### `=`
When followed by a number, looks through the die rolls and returns the number of die that rolled the target number.

For Example:

```
5d10=10
```

Assuming the 10d10 rolled `[10, 1, 5, 6, 7]`, the final result would be `1`.

##### `!=` or `=/=`
When followed by a number, looks through the die rolls and returns the number of die that didn't roll the target number.

For Example:

```
5d10!=10
Is the same as:
5d10=/=10
```

Assuming the 10d10 rolled `[10, 1, 5, 6, 7]`, the final result would be `4`.

##### `>`
When followed by a number, looks through the die rolls and returns the number of die that rolled greater than the 
target number.

For Example:

```
5d10>7
```

Assuming the 10d10 rolled `[10, 1, 5, 6, 7]`, the final result would be `1`.

##### `>=`
When followed by a number, looks through the die rolls and returns the number of die that rolled the target number 
or greater.

For Example:

```
5d10>=7
```

Assuming the 10d10 rolled `[10, 1, 5, 6, 7]`, the final result would be `2`.

##### `<`
When followed by a number, looks through the die rolls and returns the number of die that rolled less than the 
target number.

For Example:

```
5d10<5
```

Assuming the 10d10 rolled `[10, 1, 5, 6, 7]`, the final result would be `1`.

##### `<=`
When followed by a number, looks through the die rolls and returns the number of die that rolled the target number 
or less.

For Example:

```
5d10<=5
```

Assuming the 10d10 rolled `[10, 1, 5, 6, 7]`, the final result would be `2`.

### Special Dice Rolls
When the parser receives this, it triggers a pre-defined shortcut.  All of these can use the above `Operators`.

#### `df`
Shortcut to use FATE dice.

#### `st`
Shortcut for Storyteller system dice.  Specifically, any roll of 7 or more is a success with a 10 counting for 2,
successes.  No successes, results in a botch.

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

### CounterRollResultDecorators
These decorators all read the `roll_result.die_rolls` to count out values.  Therefore, they ignore the result value of
all preceding `RollResult` objects in the chain and set them to the result of the count unless the preceding 
`RollResult` is an instance of `CounterRollResultDecorator`.

#### CountValuesEqualToDecorator
Counts the number of dice that roll the target number.

#### CountValuesNotEqualToDecorator
Counts the number of dice that roll anything but the target number.

#### CountValuesGreaterThanDecorator
Counts the number of dice that roll greater than the target number.

#### CountValuesLessThanDecorator
Counts the number of dice that roll less than~~~~ the target number.

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
