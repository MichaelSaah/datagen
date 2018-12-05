from datagen.jsongen import JsonGen

jg = JsonGen()

inp = '["firstName", "lastName", "personAge"]'

outp = jg(inp, 100000)
#print(outp)
