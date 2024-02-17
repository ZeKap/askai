import argparse

def parse()->argparse.Namespace:
    """verify arguments from user"""
    parser = argparse.ArgumentParser(description='Ask AI to create a command for you')
    parser.add_argument('-a', '--api-point', help='Where to send the query')
    parser.add_argument('message', metavar='Message', help='Query send to AI')
    return parser.parse_args()


if __name__ == "__main__":
    args:argparse.Namespace = parse()
    print(args)
