names = ["John", "Paul", "George", "Ringo"]
print(f"names={names}")

a = names[0:2]
b = names[1:3]
print(f"names[1:2]={a} names[2:3]={b}")

print("names[2:3][1]=XXX")
b[1] = "XXX"
print(f"names[1:2]={a} names[2:3]={b}")
print(f"names={names}")
