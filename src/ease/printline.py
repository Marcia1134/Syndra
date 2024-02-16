def main() -> None:
    import os

    # Get the size of the terminal
    rows, columns = os.popen('stty size', 'r').read().split()

    # Print a line that is the width of the terminal
    print('-' * int(columns))