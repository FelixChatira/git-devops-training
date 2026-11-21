
from calculator import add, subtract, multiply, divide


def main():
    print("================================")
    print("   BitSec Docker Calculator")
    print("================================")

    a = 10
    b = 5

    print(f"Addition:       {a} + {b} = {add(a, b)}")
    print(f"Subtraction:    {a} - {b} = {subtract(a, b)}")
    print(f"Multiplication: {a} * {b} = {multiply(a, b)}")
    print(f"Division:       {a} / {b} = {divide(a, b)}")

    print("================================")
    print("Application executed successfully!")


if __name__ == "__main__":
    main()
