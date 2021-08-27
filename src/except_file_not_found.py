"""Sample of try-except."""
import traceback


def main():
    """Run main."""
    try:
        with open("not_found.txt", "r") as _handle:
            pass
    except FileNotFoundError as exc:
        print(f"args={exc.args}")
        print(type(exc))
        print('')
        for attr_name in dir(exc):
            try:
                if hasattr(exc, attr_name):
                    attr_obj = getattr(exc, attr_name)
                    print(f"attr={attr_name}, type={type(attr_obj)}, callable={callable(attr_obj)}")
                else:
                    print(f"attr={attr_name}")

            except AttributeError as exc2:
                print(type(exc2))
                print(traceback.format_exc())
                print(f"attr={attr_name}")


if __name__ == "__main__":
    main()
