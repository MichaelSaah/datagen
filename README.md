# Datagen 

Datagen is a command line utility and python library for generating data from arbitrary json schemas.
Use it to populate a test database, benchmark parsers, mock-up a frontend, etc.

Use it as follows:

```
$ datagen schema.json > output.json
```

## Schemas
A schema is just a json string that uses special tags to specify what should be filled in. You can think of it like a GraphQL query.

For example, let's say you want to fill in a table of users. For simplicity's sake, say each user has a first name, a last name, an email, and an age. We could write a schema like this:

```json
{
	"first" : "firstName",
	"last" : "lastName",
	"email" : "eMail",
	"age" : "personAge"
}
```

Passing this string to datagen will result in something like this:

```json
{
	"first": "Stanley",
	"last": "Brocious",
	"email": "Justin640@verizon.net",
	"age": 32
}
```

Alternatively, you could pass

```["firstName", "lastName", "eMail", "personAge"]```

and get back

```["Stanley", "Brocious", "Justin640@verizon.net", 32]```

### Generators
In the last example, `"firstName"`, `"lastName"`, `"eMail"`, and `"personAge"` are all example of what we call generators. In their simplest form generators are passed as just a name. However, some generators can take arguments.

For example, there is a `numberInt` generator that when passed without arguments produces a random signed 32 bit integer. However, let's say we wanted a three digit positive integer for a schema. All we need to do to get one of these is `numberInt|100|999`.

As you can see, we use the `|` char to seperate arguments in generators.

Generators are very easy to write, so if you need something custom, don't be afraid to write it!

### Multiple Records
Of course, producing one record isn't much fun. Datagen provides two  ways to produce multiple records.

#### The `-n` flag
The first and simplest way is to pass the `-n` flag followed by a positive integer. For example, saving the previous schema to `schema.json` and doing `$ datagen schema.json -n 5` produces

```
[
	["Barbara", "Bogue", "Erik728@comcast.net", 51],
	["Angie", "Bogue", "Faith352@hotmail.com", 26],
	["Leon", "Kriz", "Jenny971@gmail.com", 49],
	["Simon", "Gressett", "Lula258@hotmail.com", 33],
	["Annette", "Kellough", "Cody423@hotmail.com", 76]
]
```
This is handy, but not very flexible.

#### The `_n` key
The second method is much more powerful. Let's say we want our schema to represent a grade school class. We could write this:

```
{
	"teacher_name": "fullName",
	"room_number": "numberInt|100|200",
	"students": {
		"_n": 10,
		"obj": ["firstName", "lastName"]
	} 
}
```
What we did here was wrap our `students` object with another object that specified an `_n` and an `obj`. Whenever Datagen sees an object of this form, it will expand it into a list of length `_n` of `obj`'s. Here's what we get back:

```
{
    "teacher_name": "Ms. Angelica Elsa Then",
    "room_number": 162,
    "students": [
        ["Dorothy", "Kardos"],
        ["Carlton", "Brodt"],
        ["Harriet", "Kriz"],
        ["Elsa", "Jerkins"],
        ["Della", "Bombardier"],
        ["Clayton", "Bissette"],
        ["Johnnie", "Witherite"],
        ["Morris", "Strayhorn"],
        ["Susie", "Pullin"],
        ["Laurence", "Geise"]
    ]
}
```
Internally, Datagen wraps the top-level object like this when the `-n` flag is passed.


## Options
#### `-n`
This flag with an integer allows you to generate n records derived from the schema

```
$ datagen schema.json -n 10
```

#### `-p` or `--pretty`
Passing this flag pretty prints the output.

#### `-s`
Passing this flag tells Datagen to interperet the path string as the schema itself. For example, one could do

```
$ datagen '["firstName", "lastName"]' -s
```

## Writing Extensions