1. Make sure you have the latest version of PyPA’s build installed:

```
python3 -m pip install --upgrade build
```

2. Now run this command from the same directory where pyproject.toml is located:

```
python3 -m build
```

2. Test package

```python
>>> from example_package import calc
>>> calc.add_one(2)
3
>>>
```
