import unittest

from .test_arithmetic import *


def main():
    unittest.TextTestRunner(verbosity=5).run(unittest.TestSuite())


if __name__ == "__main__":
    main()

