import importlib
import argparse


parser = argparse.ArgumentParser(description='Test runner arguments')
parser.add_argument('-file', type=str, help='Test Path input')
args = parser.parse_args()


def main():
    """
    Wrapper function for testRunner.py. It is used to call each test as a
    module so that the logging entries are not __main__.
    """
    module = importlib.import_module(args.file)
    module.main()


if __name__ == "__main__":
    main()
