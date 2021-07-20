"""Test dict with unittest."""
import unittest
import math
from dict_kv_rename_all_obj import rename_dict_keys_all


class TestCalc(unittest.TestCase):
    """Test dict_kv_rename_all_obj module."""

    def test_dict_no_child(self):
        """Test dict."""
        new_dict = rename_dict_keys_all({'Str-Key': 'Val:Str'})
        self.assertDictEqual(
            new_dict,
            {'str-key': 'VAL:STR'}
        )

    def test_dict_child(self):
        """Test dict."""
        new_dict = rename_dict_keys_all(
            {'Str-Key': {'CHILD-KEY': 'child-val'}}
        )
        self.assertDictEqual(
            new_dict,
            {'str-key': {'child-key': 'CHILD-VAL'}}
        )

    def test_dict_child_tuple(self):
        """Test dict."""
        org_dict = {
            'Tuple-Key': ('t1', 't2', {'FOO': 'bar'})
        }
        new_dict = rename_dict_keys_all(org_dict)
        self.assertDictEqual(
            new_dict,
            {'tuple-key': ('T1', 'T2', {'foo': 'BAR'})}
        )

    def test_list_no_child(self):
        """Test list."""
        org_list1 = ['foo', True, False, None, float('inf'), ('foo', 'bar')]
        new_list1 = rename_dict_keys_all(org_list1)
        chk_list1 = ['FOO', True, False, None, float('inf'), ('FOO', 'BAR')]
        self.assertListEqual(new_list1, chk_list1)

        # Note: float('nan') == float('nan') -> False
        org_list2 = [float('nan')]
        new_list2 = rename_dict_keys_all(org_list2)
        assert math.isnan(new_list2[0])

    def test_tuple_no_child(self):
        """Test tuple."""
        org_tuple1 = ('Foo', 'Bar', ('Apple', 150))
        new_tuple1 = rename_dict_keys_all(org_tuple1)
        chk_tuple1 = ('FOO', 'BAR', ('APPLE', 150))
        self.assertTupleEqual(new_tuple1, chk_tuple1)


if __name__ == '__main__':
    unittest.main()

# EOF
