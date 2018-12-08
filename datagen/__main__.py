import argparse, json
from datagen import Datagen 

description = "An extensible data generation utility"

parser = argparse.ArgumentParser(description=description)
parser.add_argument('schema', type=str,
                    help='Path to the schema file')
parser.add_argument('-n', dest='n', metavar='N', action='store', type=int,
                    default=1,
                    help='Generate N copies of the schema')
parser.add_argument('-s', dest='schema_literal', action='store', type=str,
                    metavar='schema',
                    help='Pass the schema as an argument instead of a file')
parser.add_argument('-p', '--pretty', action='store_true', dest='pretty',
                    default=False,
                    help='Pretty print the output')

args = parser.parse_args()
with open(args.schema, 'r') as f:
    schema = f.read()
    
dg = Datagen()
if args.pretty:
    schema = json.loads(schema)
    data = dg(schema, args.n, native=True)
    print(json.dumps(data, indent=4))
else:
    print(dg(schema), args.n)
