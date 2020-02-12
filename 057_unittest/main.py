# 057. unittest and doctest
#
# TestCase and docstring examples.
#
# Run: python 057_unittest/main.py

# --- unittest mod ---
import unittest


class T(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)

    def test_raises(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0


suite = unittest.defaultTestLoader.loadTestsFromTestCase(T)
result = unittest.TextTestRunner(verbosity=0).run(suite)
print(result.wasSuccessful())


# --- doctest ---
def add(a, b):
    """
    >>> add(2, 3)
    5
    """
    return a + b


import doctest

print(doctest.testmod(verbose=False).failed)
