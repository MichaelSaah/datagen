from datagen.jsongen import JsonGen

jg = JsonGen()

inp = """
{
    "first" : "firstName",
    "last" : "lastName",
    "children" : {
        "_n" : 4,
        "obj" : {
            "first" : "firstName",
            "last" : "lastName"
        }
    }
}
"""

outp = jg(inp)
print(outp)
