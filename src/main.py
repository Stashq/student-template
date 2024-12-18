"""Simple example of main.py.
"""


def add(a: int, b: int) -> int:
    return a + b


def get_message(a: int, b: int, sum_: int) -> str:
    return f"Message: {a} + {b} equals {sum_}."


def main(x1: int, x2: int) -> None:
    """Adds provided numbers and prints the message with result.

    Parameters
    ----------
    x1 : int
        First number.
    x2 : int
        Second number.
    """
    sum_ = add(a=x1, b=x2)
    msg = get_message(a=x1, b=x2, sum_=sum_)
    print(msg)


if __name__ == "__main__":  # runs only if this file was invoked from terminal
    main(x1=3, x2=4)
