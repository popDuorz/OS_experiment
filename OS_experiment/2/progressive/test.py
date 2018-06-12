from examples import tree, simple
from progressive.exceptions import LengthOverflowError


class TestExamples(object):

    def test_tree_example(self):
        try:
            tree()
        except LengthOverflowError as e:
            print("{}: {}".format(type(e), e))

    def test_simple_example(self):
        simple()


if __name__ == '__main__':
    test = TestExamples()
    test.test_tree_example()