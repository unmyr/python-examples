#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Shows the attributes of the Python module."""

if __name__ == "__main__":
    import os
    script_file_name = os.path.basename(__file__)

    # absolute-path: no empty
    # current directory: ''
    script_dir_name  = os.path.dirname(__file__)

    # splitext[0] is include directory name
    script_basename  = os.path.splitext(os.path.basename(__file__))[0]
    script_extension = os.path.splitext(os.path.basename(__file__))[1]

    print("script file name: '{}'".format(script_file_name))
    print("script dir name: '{}'".format(script_dir_name))
    print("script name(noext): '{}'".format(script_basename))
    print("script extension: '{}'".format(script_extension))

    import mimetypes
    print(u"MIME Type: '{}'".format(mimetypes.guess_type(__file__)[0]))

# EOF
