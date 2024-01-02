#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The way to have a here document, without newlines at the top and bottom."""

OPTION = '<script src="app.js"></script>'

print(
    """
<!DOCTYPE html>
<html>
<head>
  <title>Test</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {option}
</head>
<body>
</body>
</html>
""".format(option=OPTION).strip()
)
