import cmd
import random


class DiceRollInterface(cmd.Cmd):
    intro = "Roll simulated dice like a pro. Type 'help' for help."

    def do_stats(self, _):
        """Do stat rolls (4d6-drop 1 six times)."""
        d = Die()
        for _ in range(6):
            print((d(6)*4).drop(1))

    def do_shell(self, roll):
        """Do a general roll, as specified by a string.

        The syntax, in EBNF, is:
        roll = num of rolls, "d", num of sides, ["-drop", num to drop], ["*", num of times] ;
        num of rolls = INTEGER ;
        num of sides = INTEGER ;
        num to drop = INTEGER ;
        num of times = INTEGER ;

        For example, the stat rolls would be the command !4d6-drop1*6.
        """

        line_len = len(roll)
        # A recursive descent parser will be used for simplicity
        def parse_roll():
            num_of_rolls = parse_num_of_rolls()

            if not roll.startswith("d"):
                error()
            consume(1)
            num_of_sides = parse_num_of_sides()

            num_to_drop = 0
            if roll.startswith("-drop"):
                consume(5)
                num_to_drop = parse_num_to_drop()

            num_of_times = 1
            if roll.startswith("*"):
                consume(1)
                num_of_times = parse_num_of_times()

            if roll: # should be empty at end
                error()

            # Execute the roll
            d = Die()
            for _ in range(num_of_times):
                print((d(num_of_sides)*num_of_rolls).drop(num_to_drop))

        def parse_num_of_rolls():
            return lex_INTEGER()

        def parse_num_of_sides():
            return lex_INTEGER()

        def parse_num_to_drop():
            return lex_INTEGER()

        def parse_num_of_times():
            return lex_INTEGER()

        def lex_INTEGER():
            index = 1
            while True:
                if not roll[:index].isdecimal() or index > len(roll):
                    break
                index += 1
            if index == 1: error()
            integer = int(roll[:index - 1])
            consume(index - 1)
            return integer

        def consume(chars):
            nonlocal roll
            roll = roll[chars:]

        def error():
            # Syntax error!
            raise Exception(f"Syntax error at column {line_len - len(roll) + 2}!")

        try:
            parse_roll()
        except Exception as e:
            print(e)


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
        for _ in range(len(self._rolls)*(rolls - 1)):
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


random.seed()
interface = DiceRollInterface()
interface.cmdloop()
