from datagen.jsongen import JsonGen
#import json

jg = JsonGen()

inp = '["firstName", "lastName", "personAge"]'

outp = jg(inp, 100000)
#print(outp)
