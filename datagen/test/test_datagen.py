from ..datagen import Datagen, Generate
from ..generators.utilities import WeightedSampler
import string
import tempfile, shutil
import pytest
import os

test_gens = os.path.dirname(os.path.abspath(__file__)) + '/generators'

def test_generators():
    gen = Generate(generator_paths=[test_gens])
    
    # case: general sampler test
    t = gen('_sampler_tester')
    assert t in gen._db['_sampler_tester'].values

    # case: WeightedSampler
    wb = WeightedSampler(['a', 'b', 'c'], [0.4, 0.6, 0])
    for _ in range(100):
        assert wb() in ['a', 'b']

    # case: not found:
    with pytest.raises(ValueError):
        nf = gen('not found, leave me be')

    # case: eMail
    em = gen('eMail')
    usr, dom = em.split('@')
    assert usr.isalnum()
    subd, tld = dom.split('.')
    assert subd
    assert tld

    # case: time_formatter
    # TODO

    # case: numberInt - this case covers IntegerBetween
    for _ in range(100):
        assert -100 <= gen('numberInt|-100|100') <= 100

    # case: numberFloat - this case covers FloatBetween
    for _ in range(100):
        n = gen('numberFloat|-100|100|3') 
        assert -100 <= n <= 100
        assert len(str(n).split('.')[1]) <= 3
        
    # case: randomString - this case covers RandomChar
    assert 10 <= len(gen('randomString')) <= 100
    assert len(gen('randomString|10')) == 10
    chars = string.ascii_letters + string.digits
    for c in gen('randomString'):
        assert c in chars

    # case: zipCode
    for _ in range(1000):
        zc = gen('zipCode')
        assert 0 <= int(zc) <= 99999
        assert len(zc) == 5


def test_datagen():
    dg = Datagen(generator_paths=[test_gens])
    gen = dg.gen

    # case: general
    test_dict = {
        "name" : {"first": "_sampler_tester", "last": "_sampler_tester"},
        "age" : "_sampler_tester",
        "children" : ["_sampler_tester", "_sampler_tester", "_sampler_tester" ]
    }

    test_dict = dg(test_dict, native=True)
    assert test_dict["name"]["first"] in gen._db["_sampler_tester"].values
    assert test_dict["name"]["last"] in gen._db["_sampler_tester"].values
    assert test_dict["age"] in gen._db["_sampler_tester"].values
    for f in test_dict["children"]:
        assert f in gen._db["_sampler_tester"].values

    # case: working array
    test_dict = {
        '_n' : 10,
        'obj' : {'name' : '_sampler_tester'}
    }

    test_dict = dg(test_dict, native=True)
    assert len(test_dict) == 10
    for i in range(10):
        assert test_dict[i]['name'] in gen._db['_sampler_tester'].values

    # case: array with bad _n
    test_dict = {
        '_n' : 'foo',
        'obj' : {'name' : '_sampler_tester'}
    }

    with pytest.raises(ValueError):
        test_dict = dg(test_dict, native=True)

    # case: array with no obj
    test_dict = {
        '_n' : 'foo',
    }

    with pytest.raises(ValueError):
        test_dict = dg(test_dict, native=True)
    
    # case: nested lists
    test_dict = {
        "people" : [["_sampler_tester", "_sampler_tester"], ["_sampler_tester", "_sampler_tester"]]
    }

    test_dict = dg(test_dict, native=True)
    for f,l in test_dict["people"]:
        assert f in gen._db["_sampler_tester"].values
        assert l in gen._db["_sampler_tester"].values

    # case: non-(string,list,dict) values
    test_dict = {
        "int" : 3, "float" : 2.07, "bool" : True, "null" : None
    }
    test_dict = dg(test_dict, native=True)
    assert test_dict['int'] == 3
    assert test_dict['float'] == 2.07
    assert test_dict['bool'] == True
    assert test_dict['null'] == None

    # case: list
    test_list = ["_sampler_tester", "_sampler_tester"]
    test_list = dg(test_list, native=True)
    assert test_list[0] in gen._db["_sampler_tester"].values
    assert test_list[1] in gen._db["_sampler_tester"].values

    # case: naked value
    test_val = "_sampler_tester"
    test_val = dg(test_val, native=True)
    assert test_val in gen._db["_sampler_tester"].values


def test_custom_generator_loading():
    t_dir = tempfile.mkdtemp()
    shutil.copy(test_gens + '/_tester.py', t_dir)
    paths = [t_dir]
    gen = Generate(generator_paths=paths)

    assert '_tester' in gen._db

    shutil.rmtree(t_dir)
