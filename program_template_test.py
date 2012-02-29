"""Test cases for program_template

Using the 'unittest' module to test programs thouroughly
"""

# Program information

__authors__ = "Eric Normandeau"
__program_name__ = "program_template"
__version_info__ = ('1', '1', '5')
__version__ = '.'.join(__version_info__)
__copyright__ = "Copyright (c) 2011 Eric Normandeau"
__license__ = "GPLv3"
__revision_date__ = "2011-02-01"


# Importing modules

import program_template
import unittest


# Error Classes

class KnownValues(unittest.TestCase):
    knownValues = ( ("alabama", "alabama"),
                    ("33", "33"))

    def test_fun_1(self):
        """Function fun_1 should give known result with known input"""
        for value, expected in self.knownValues:
            result = program_template.fun_1(value)
            self.assertEqual(expected, result)


class Fun1BadInput(unittest.TestCase):
    """Test different possible bad inputs"""

    def testOneArgument(self):
        """fun_1 should raise error if argument is not a string"""
        for value in [33, ["sdf"], (2, 4), {}]:
            self.assertRaises(program_template.BadInput, program_template.fun_1, value)

    def testOutput(self):
        """fun_1 should output exactly it's input"""
        for value in ["Eric", "asdf", "", "sdfi'fffff'poij"]:
            result = program_template.fun_1(value)
            self.assertEqual(value, result)


if __name__ == "__main__":
    unittest.main()

