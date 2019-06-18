import cmd
import random
from collections import namedtuple


class DiceRollInterface(cmd.Cmd):
    intro = "Roll simulated dice like a pro. Type 'help' for help."

    def do_stats(self, _):
        """Do stat rolls (4d6-drop 1 six times)."""
        d = Die()
        for _ in range(6):
            print((d(6) * 4).drop(1))

    def do_shell(self, roll):
        """Do a general roll, as specified by a string.

        The syntax, in EBNF, is:
        roll = num of rolls, "d", num of sides, ["-drop", num to drop],
            ["*", num of times] ;
        num of rolls = INTEGER ;
        num of sides = INTEGER ;
        num to drop = INTEGER ;
        num of times = INTEGER ;

        For example, the stat rolls would be the command !4d6-drop1*6.
        """

        self._roll = roll
        rollObject = None
        try:
            rollObject = self._parse_roll()
            self._execute_roll(rollObject)
        except DiceException as e:
            print(e)

    def _parse_num_of_rolls(self):
        return self._lex_INTEGER()

    def _parse_num_of_sides(self):
        return self._lex_INTEGER()

    def _parse_num_to_drop(self):
        return self._lex_INTEGER()

    def _parse_num_of_times(self):
        return self._lex_INTEGER()

    def _lex_INTEGER(self):
        index = 1
        while True:
            if not self._roll[:index].isdecimal() or index > len(self._roll):
                break
            index += 1
        if index == 1:
            self._error()
        integer = int(self._roll[:index - 1])
        self._consume(index - 1)
        return integer

    def _consume(self, chars):
        self._roll = self._roll[chars:]

    def _error(self):
        column = self._line_len - len(self._roll) + 2
        raise DiceSyntaxError(f"Syntax error at column {column}!")

    def _parse_roll(self):
        """Parse the roll string self._roll and execute the roll.

        Returns a namedtuple containing properties of the role.

        Implementation detail: the parser is a recursive descent parser.
        """

        self._line_len = len(self._roll)

        num_of_rolls = self._parse_num_of_rolls()

        if not self._roll.startswith("d"):
            self._error()
        self._consume(1)
        num_of_sides = self._parse_num_of_sides()

        num_to_drop = 0
        if self._roll.startswith("-drop"):
            self._consume(5)
            num_to_drop = self._parse_num_to_drop()

        num_of_times = 1
        if self._roll.startswith("*"):
            self._consume(1)
            num_of_times = self._parse_num_of_times()

        self._roll_should_be_empty()

        return Roll(
            num_to_drop=num_to_drop,
            num_of_rolls=num_of_rolls,
            num_of_sides=num_of_sides,
            num_of_times=num_of_times
            )

    def _execute_roll(self, roll):
        # Execute the roll
        d = Die()
        for _ in range(roll.num_of_times):
            completedRoll = (
                d(roll.num_of_sides)
                * roll.num_of_rolls).drop(roll.num_to_drop)
            print(completedRoll)

    def _roll_should_be_empty(self):
        if self._roll:
            self._error()


Roll = namedtuple(
    'Roll', ['num_of_times', 'num_of_sides', 'num_of_rolls', 'num_to_drop'])


class Die:

    def __init__(self, _original=None):
        self._rolls = []
        self._sides = -1
        if _original is not None:
            self._rolls = _original._rolls[:]
            self._sides = _original._sides

    def __call__(self, sides):
        new_die = Die(self)
        new_die._sides = sides
        new_die._roll()
        # print('d({}) => {}'.format(sides, new_die._rolls))
        return new_die

    def __mul__(self, rolls):
        new_die = Die(self)
        for _ in range(len(self._rolls) * (rolls - 1)):
            new_die._roll()
        # print('{}*d => {}'.format(rolls, new_die._rolls))
        return new_die

    def drop(self, num):
        new_die = Die(self)
        new_die._rolls = sorted(new_die._rolls)[num:]
        return new_die

    def __str__(self):
        return str(sum(self._rolls))

    def _roll(self):
        self._rolls.append(random.randint(1, self._sides))


class DiceException(Exception):
    pass


class DiceSyntaxError(SyntaxError, DiceException):
    pass


random.seed()
interface = DiceRollInterface()
interface.cmdloop()
