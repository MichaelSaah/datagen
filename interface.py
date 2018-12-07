from datagen.jsongen import JsonGen
import json 

jg = JsonGen()

inp = """
{
        "teacher_name": "fullName",
	"room_number": "numberInt|100|200",
        "students": {
		"_n": 10,
                "obj": ["firstName", "lastName"]
    } 
}
"""

outp = json.loads(jg(inp))
print(json.dumps(outp, indent=4, sort_keys=False))
