def greet(status: str) -> str:
    """Return a short status message for the given status string."""
    return f"Status is {status}."

# Direct call with an explicit argument
m_1 = greet(status="Paid")

# Call using dictionary unpacking (**kwargs)
params = {"status": "Paid"}
m_2 = greet(**params)

print([m_1, m_2])
