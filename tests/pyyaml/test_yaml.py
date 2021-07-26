"""Test yaml."""
import unittest
import datetime

import yaml


class TestYaml(unittest.TestCase):
    """Test dict_kv_rename_all_obj module."""

    def test_yaml_numbers(self):
        """Test number formats."""
        new_dict: dict = yaml.safe_load('binary: 0b1010_0111_0100_1010_1110')
        self.assertDictEqual(
            new_dict,
            {'binary': 685230}
        )

        new_dict: dict = yaml.safe_load('decimal: +685_230')
        self.assertDictEqual(
            new_dict,
            {'decimal': 685230}
        )

        new_dict: dict = yaml.safe_load('octal: 02472256')
        self.assertDictEqual(
            new_dict,
            {'octal': 0o2472256}
        )

        new_dict: dict = yaml.safe_load('hexadecimal: 0x_0A_74_AE')
        self.assertDictEqual(
            new_dict,
            {'hexadecimal': 0x0a74ae}
        )

        base60_str: str = '190:20:30'
        hh, mm, ss = list(map(int, base60_str.split(':')))
        new_dict = yaml.safe_load(f'base 60: {base60_str}')
        self.assertDictEqual(
            new_dict,
            {'base 60': hh * 60 * 60 + mm * 60 + ss}
        )

    def test_yaml_dict(self):
        """Test datetime."""
        yaml_str: str = """
- # Explicit keys
  x: 1
  y: 2
  r: 10
  label: center/big""".strip()

        new_dict = yaml.safe_load(yaml_str)
        self.assertListEqual(
            new_dict,
            [{'x': 1, 'y': 2, 'r': 10, 'label': 'center/big'}]
        )

    def test_yaml_null(self):
        """Test datetime."""
        tests = [
            'canonical: ~',
            'english: null',
            '~: null key'
        ]
        new_dict = yaml.safe_load('\n'.join(tests))
        self.assertDictEqual(
            new_dict,
            {
                'canonical': None,
                'english': None,
                None: 'null key'
            }
        )

    def test_yaml_datetime(self):
        """Test datetime."""
        d = yaml.safe_load('2001-12-15T02:59:43.999999Z')
        self.assertEqual(d, datetime.datetime(2001, 12, 15, 2, 59, 43, 999999, tzinfo=datetime.timezone.utc))
