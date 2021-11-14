"""Gets the UNICODE code point."""
import struct


def get_unicode_code_point_nm(character: str) -> int:
    """Get unicode code point"""
    bytes_utf16be = character.encode('utf-16be')
    return struct.unpack('>H', bytes_utf16be)[0]


def get_unicode_code_point_sp(character: str) -> int:
    """Get unicode code point of surrogate pair."""
    bytes_utf16be = character.encode('utf-16be', 'surrogatepass')
    hi, lo = struct.unpack('>HH', bytes_utf16be)
    x = (hi & ((1 << 6) - 1)) << 10 | lo & ((1 << 10) - 1)
    w = (hi >> 6) & (1 << 5) - 1
    u = w + 1
    return x | u << 16


def main() -> None:
    """Run main."""
    zz_char = 'ℤ'
    code_point = get_unicode_code_point_nm(zz_char)
    zz_bytes_sg = zz_char.encode('utf-16be')
    assert code_point == 8484
    print(f"{zz_char}({len(zz_bytes_sg)}): U+{code_point:04X}, &#{code_point:d};")

    # surrogate pair
    # https://www.unicode.org/faq/utf_bom.html#utf16-2
    ff_char = "𝔽"  # MATHEMATICAL DOUBLE-STRUCK CAPITAL F
    ff_bytes_sg = ff_char.encode('utf-16be', 'surrogatepass')
    code_point = get_unicode_code_point_sp(ff_char)
    print(f"{ff_char}({len(ff_bytes_sg)}) = U+{code_point:X}, &#{code_point:d};")
    assert code_point == 120125


if __name__ == '__main__':
    main()

# EOF
