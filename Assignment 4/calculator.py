print("Calculator")
print("\n")

num1=float(input())
sign=input()
num2=float(input())

def add(a,b):
    return a+b

def divide(a,b):
    return a/b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

result=0
match sign:
    case "+":
        result=add(num1,num2)
    case "-":
        result=subtract(num1, num2)
    case "*" | "x":
        result=multiply(num1,num2)
    case "/":
        result=divide(num1, num2)
    case _:
        print(f"invalid operation{result} ")


print(result)