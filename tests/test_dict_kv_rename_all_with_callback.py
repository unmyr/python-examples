"""Test dict with unittest."""
import unittest
import datetime
from dict_kv_rename_all_with_callback import recursive


class TestCalc(unittest.TestCase):
    """Test dict_kv_rename_all_obj module."""

    def test_str_num_rename_values(self):
        """Test value."""
        org_str1 = "Hello world"
        chk_str1 = "hello world"
        new_str1 = recursive(
            org_str1,
            value_func=lambda v: v.lower() if isinstance(v, str) else v
        )
        self.assertMultiLineEqual(new_str1, chk_str1)

        org_num1 = 3
        chk_num1 = 3
        new_num1 = recursive(
            org_num1,
            value_func=lambda v: v.lower() if isinstance(v, str) else v
        )
        assert new_num1 == chk_num1

        org_date1 = datetime.date(2017, 11, 12)
        chk_date1 = None
        new_date1 = recursive(
            org_date1
        )
        self.assertEqual(new_date1, chk_date1)

    def test_dict_rename_keys(self):
        """Test dict."""
        org_dict1 = {"Outer": {"Inner": "Value"}}
        chk_dict1 = {"outer": {"inner": "Value"}}
        new_dict1 = recursive(
            org_dict1,
            dict_func=lambda x: {key.lower(): value for key, value in x.items()}
        )
        self.assertDictEqual(new_dict1, chk_dict1)

    def test_dict_rename_values(self):
        """Test dict."""
        org_dict1 = {"Outer": {"Inner": "Value", 'Date': datetime.date(2017, 11, 12)}}
        chk_dict1 = {"Outer": {"Inner": "value", 'Date': None}}
        new_dict1 = recursive(
            org_dict1,
            value_func=lambda v: v.lower() if isinstance(v, str) else v
        )
        self.assertDictEqual(new_dict1, chk_dict1)

        org_dict2 = {"Outer": {"Inner": datetime.date(2017, 11, 12)}}
        chk_dict2 = {"Outer": {"Inner": None}}
        new_dict2 = recursive(
            org_dict2,
            value_func=lambda v: v.lower() if isinstance(v, str) else v
        )
        self.assertDictEqual(new_dict2, chk_dict2)

    def test_list_rename_values(self):
        """Test dict."""
        org_list1 = ['Item1', 'Item2', 'Item3', 3]
        chk_list1 = ['item1', 'item2', 'item3', 3]
        new_list1 = recursive(
            org_list1,
            value_func=lambda v: v.lower() if isinstance(v, str) else v
        )
        self.assertListEqual(new_list1, chk_list1)

    def test_list_dict_rename_keys(self):
        """Test list of dict."""
        org_list1 = [{'None': 'None'}, {'bool': 'False'}, {'int': '0'}, {'str': ''}]
        chk_list1 = [{'none': 'None'}, {'bool': 'False'}, {'int': '0'}, {'str': ''}]
        new_list1 = recursive(
            org_list1,
            dict_func=lambda x: {key.lower(): value for key, value in x.items()}
        )
        self.assertListEqual(new_list1, chk_list1)

    def test_tuple_rename_values(self):
        """Test dict."""
        org_tuple1 = ('Item1', 'Item2', 'Item3', 3)
        chk_tuple1 = ['item1', 'item2', 'item3', 3]
        new_tuple1 = recursive(
            org_tuple1,
            value_func=lambda v: v.lower() if isinstance(v, str) else v
        )
        self.assertListEqual(new_tuple1, chk_tuple1)


if __name__ == '__main__':
    unittest.main()

# EOF
