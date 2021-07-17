#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python for Loop explained with examples."""
makers = ['Toyota', 'Nissan', 'Honda']
for maker_name in makers:
    print(maker_name)

for i, maker_name in enumerate(makers):
    print(f'{i}: {maker_name}')

for i in range(5):
    print(i)
