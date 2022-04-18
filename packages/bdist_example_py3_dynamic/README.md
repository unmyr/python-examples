
1. Build package

```
python3 setup.py sdist bdist_wheel
```

2. Test package

```python
>>> from example_package import calc
>>> calc.add_one(2)
3
>>>
```