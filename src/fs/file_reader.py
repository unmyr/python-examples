import sys

def main():
  with open(sys.argv[1]) as file_handle:
    for line_with_line_break in file_handle:
      line = line_with_line_break.rstrip()
      print(line)

if __name__ == "__main__":
  main()

  # EOF
  