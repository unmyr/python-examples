"""Test string."""
import struct
import unittest


class TestStringEncode(unittest.TestCase):
    """Test string module."""

    def test_encode_utf16be(self):
        """Test encode utf016be."""
        zz_char = 'ℤ'  # Double-Struck Capital Z
        bytes_utf16be = zz_char.encode('utf-16be')
        code_point = struct.unpack('>H', bytes_utf16be)[0]
        assert code_point == 8484

    def test_encode_utf32be(self):
        """Test encode to utf-32be."""
        ff_char = "𝔽"  # MATHEMATICAL DOUBLE-STRUCK CAPITAL F

        bytes_utf32be = ff_char.encode('utf-32be')
        code_point = struct.unpack('>I', bytes_utf32be)[0]
        assert code_point == 120125

        bytes_utf16be = ff_char.encode('utf-16be')
        hi, lo = struct.unpack('>HH', bytes_utf16be)
        x = (hi & ((1 << 6) - 1)) << 10 | lo & ((1 << 10) - 1)
        w = (hi >> 6) & (1 << 5) - 1
        u = w + 1
        code_point = x | u << 16
        assert code_point == 120125

    def test_encode_surrogate_pair(self):
        """Test encode surrogate pair."""
        ff_char = "𝔽"  # MATHEMATICAL DOUBLE-STRUCK CAPITAL F
        assert ff_char == '\ud835\udd3d'.encode('utf-16le', 'surrogatepass').decode('utf-16le')
