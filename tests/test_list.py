"""Test list with unittest."""
import unittest


class TestList(unittest.TestCase):
    """Test list module."""

    def test_sort(self):
        """Test sorted."""
        list_of_dict = [
            {"name": "a", "value": 0.1},
            {"name": "b", "value": 1.1},
            {"name": "c", "value": 0.5},
        ]

        sorted_new_list = sorted(list_of_dict, key=lambda k: k["value"], reverse=True)

        self.assertListEqual(
            sorted_new_list,
            [
                {"name": "b", "value": 1.1},
                {"name": "c", "value": 0.5},
                {"name": "a", "value": 0.1},
            ],
        )
