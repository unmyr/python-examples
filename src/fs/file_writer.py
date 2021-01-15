#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

def main():
  with open(sys.argv[1], 'w') as file_handle:
    file_handle.write("Pythonでファイルに書き込みました！")

if __name__ == "__main__":
  main()

# EOF
