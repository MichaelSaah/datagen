# Datagen 

Datagen is a command line utility and python library for generating data from arbitrary json schemas.
Use it to populate a test database, benchmark parsers, mock-up a frontend, etc.

Use it as follows:

```
$ datagen schema.json > output.json
```

### Other options
The `-n` flag allows you to generate n records derived from the schema

```
$ datagen schema.json -n 10 > output.json

```
For example, 

