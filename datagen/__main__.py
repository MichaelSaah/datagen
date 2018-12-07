import argparse

description = "An extensible data generation utility"

parser = argparse.ArgumentParser(description=description)
parser.add_argument('schema', type=str, nargs=1,
                    help='Path to the schema file')
parser.add_argument('-n', dest='n', metavar='N', action='store', type=int,
                    help='Generate N copies of the schema')
parser.add_argument('-s', dest='schema_literal', action='store', type=str,
                    metavar='schema',
                    help='Pass the schema as an argument instead of a file')

args = parser.parse_args()
print(args.schema)
