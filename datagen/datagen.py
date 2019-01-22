import json, os
import importlib.util
from importlib import import_module


class Generate:
    def __init__(self, generator_paths):
        self._db = {}
        # load package generators
        package_path = os.path.dirname(__file__) + '/generators'
        files = list(map(self.clean_file_name, os.listdir(package_path)))
        modules = [f for f in files if f]
        for module in modules:
            self.load_package_generator(module)
        # load custom generators
        for path in generator_paths:
            try:
                files = list(map(self.clean_file_name, os.listdir(path)))
            except FileNotFoundError:
                print(path + 'is not a valid path')
                continue
            modules = [f for f in files if f]
            for module in modules:
                self.load_custom_generator(path, module)

    def clean_file_name(self, file_name):
        if file_name != '__init__.py' and file_name[-3:] == '.py':
            return file_name[:-3]
        else:
            return ''

    def load_package_generator(self, generator):
        module = import_module('datagen.generators.' + generator)
        try:            
            self._db[generator] = getattr(module, generator)()
        except AttributeError:
            pass

    def load_custom_generator(self, path, generator):
        spec = importlib.util.spec_from_file_location(
            generator, path + '/' + generator + '.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            self._db[generator] = getattr(module, generator)()
        except AttributeError:
            pass

    def __call__(self, args_str):
        args_out = dict() 
        args = args_str.split('|')

        # validate call and call args
        if args[0] not in self._db:
            msg = f"Invalid data type given: {args[0]}"
            raise ValueError(msg)

        if len(args) > 1:
            return self._db[args[0]](*args[1:])
        else:
            return self._db[args[0]]()


class Datagen:
    def __init__(self, generator_paths=[]):
        self.gen = Generate(generator_paths)

    def __call__(self, data, n=1, native=False): 
        if native:
            return self.generate(data, n)
        else:
            data = json.loads(data)
            data = self.generate(data, n)
            return json.dumps(data)

    def generate(self, d, n):
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
