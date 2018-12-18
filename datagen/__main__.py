import argparse, json, sys
from datagen import Datagen 

def main():
    description = "An extensible data generation utility"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('schema', type=str,
                        help='Path to the schema file, or the schema itself if -s is passed')
    parser.add_argument('-n', dest='n', metavar='N', action='store', type=int,
                        default=1,
                        help='Generate N copies of the schema')
    parser.add_argument('-s', dest='schema_literal', action='store_true', default=False,
                        help='If present, tells datagen to treat the input string as a schema literal, instead of as a file path.')
    parser.add_argument('-p', '--pretty', action='store_true', dest='pretty',
                        default=False,
                        help='Pretty print the output')
    args = parser.parse_args()

    if args.schema_literal:
        schema = args.schema
    else:
        with open(args.schema, 'r') as f:
            schema = f.read()
        
    dg = Datagen()
    if args.pretty:
        schema = json.loads(schema)
        data = dg(schema, args.n, native=True)
        print(json.dumps(data, indent=4))
    else:
        print(dg(schema, args.n))

if __name__ == '__main__':
    main()
