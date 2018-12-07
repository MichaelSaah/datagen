import json, os
from importlib import import_module

class Generate:
    holder = """_db = {
        # tester
        '_tester' : _tester(),

        # names
        'firstName' : firstName(), # random gender
        'lastName' : lastName(),
        'middleInit': middleInit(),
        'fullName': fullName(), # matching random gender
        'prefix' : prefix(), # random gender
        'suffix' : suffix(), # generally male

        # person
        'personAge' : personAge(),
        'personSex' : personSex(),

        # email
        'eMail' : eMail(),

        # phone
        'localNumber': localNumber(),
        'internationalCode': internationalCode(),
        'areaCode': areaCode(),
        'phoneExtension': phoneExtension(),
        'internationalNumber': internationalNumber(),

        # time
        'timeZone' : timeZone(),
        'timeNow' : timeNow(),
        'timeUnix' : timeUnix(),
        'timeRandom' : timeRandom(),

        # numbers
        'numberInt' : numberInt(),
        'numberFloat' : numberFloat(),

        # random strings
        'randomString' : randomString(),

        # addresses
        'streetName' : streetName(),
        'cityName' : cityName(),
        'stateCode' : stateCode(),
        'zipCode' : zipCode(),
        'streetNum' : streetNum(),
        'fullAddress' : fullAddress(),
    }"""

    def __init__(self):
        self._db = {}
        
        #os.chdir(os.path.dirname(os.path.realpath(__file__)))
        for module in os.listdir(os.path.dirname(__file__) + '/generators'):
            if module == '__init__.py' or module[-3:] != '.py':
                continue
            generator = module[:-3]
            try:            
                module = import_module('.generators.' + generator, 'datagen') # change anchor to load from setup.py or something
                self._db[generator] = getattr(module, generator)()
            except AttributeError:
                continue


    def parse_args(self, args_str):
        args_out = dict() 
        args = args_str.split('|')

        # validate call and call args
        if args[0] not in self._db:
            msg = f"Invalid data type given: {args[0]}"
            raise ValueError(msg)
        args_out['call'] = args[0]

        if len(args) > 1:
            # test extra args with a test call
            # if the args are bad, responsibility to raise
            # exception is on called function
            self._db[args[0]](*args[1:])
            args_out['args'] = args[1:]
        else:
            args_out['args'] = []

        return args_out
    

    def __call__(self, args_str):
        args = self.parse_args(args_str)
        return self._db[args['call']](*args['args'])


class datagen:
    gen = Generate()

    def __call__(self, jsn, n=1):
        d = json.loads(jsn)
        data = self.generate(d, n)
        return json.dumps(data)

    def generate(self, d, n=1):
        if n > 1:
            d = {'_n' : n, 'obj' : d}
        return self.replace_values(d)

    def replace_values(self, d):
        if isinstance(d, list):
            return list(map(self.replace_values, d))
        elif isinstance(d, dict):
            if '_n' in d:
                try:
                    n = int(d['_n'])
                except ValueError:
                    msg = f"Value given for `_n` not valid: {d['_n']} must be integer"
                    raise ValueError(msg)
                if 'obj' in d:
                    obj = d['obj']
                else:
                    msg = f"`_n` found, but `obj` not found"
                    raise ValueError(msg)
                return self.replace_values([obj for _ in range(n)])
            else:
                return {k: self.replace_values(v) for k,v in d.items()}
        elif isinstance(d, str):
            return self.gen(d)
        else:
            return d
