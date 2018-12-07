import datagen.datagen as datagen
from datagen.datagen import Generate
from datagen.generators.utilities import WeightedSampler
import string
import pytest

gen = Generate()


def test_generators():
    # case: general sampler test
    t = gen('_tester')
    assert t in gen._db['_tester'].values

    # case: WeightedSampler
    wb = WeightedSampler(['a', 'b', 'c'], [0.4, 0.6, 0])
    for _ in range(100):
        assert wb() in ['a', 'b']

    # case: not found:
    with pytest.raises(ValueError):
        nf = gen('not found, leave me be')

    # MOVE TO TEST_GENERATE
    # case: array
    #values = gen('array|5|_tester')
    #for v in values:
    #    assert v in gen._db['_tester'].values

    # MOVE TO TEST_GENERATE
    # case: array with bad n
    #bad_args = ['array|2.3|_tester', 'array|-3|_tester', 'array|n|_tester']
    #for a in bad_args:
    #    with pytest.raises(ValueError):
    #        gen(a)

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
    dg = datagen()

    # case: general
    test_dict = {
        "name" : {"first": "_tester", "last": "_tester"},
        "age" : "_tester",
        "children" : ["_tester", "_tester", "_tester" ]
    }

    test_dict = dg.generate(test_dict)
    assert test_dict["name"]["first"] in gen._db["_tester"].values
    assert test_dict["name"]["last"] in gen._db["_tester"].values
    assert test_dict["age"] in gen._db["_tester"].values
    for f in test_dict["children"]:
        assert f in gen._db["_tester"].values

    # case: working array
    test_dict = {
        '_n' : 10,
        'obj' : {'name' : '_tester'}
    }

    test_dict = dg.generate(test_dict)
    assert len(test_dict) == 10
    for i in range(10):
        assert test_dict[i]['name'] in gen._db['_tester'].values

    # case: array with bad _n
    test_dict = {
        '_n' : 'foo',
        'obj' : {'name' : '_tester'}
    }

    with pytest.raises(ValueError):
        test_dict = dg.generate(test_dict)

    # case: array with no obj
    test_dict = {
        '_n' : 'foo',
    }

    with pytest.raises(ValueError):
        test_dict = dg.generate(test_dict)
    
    # case: nested lists
    test_dict = {
        "people" : [["_tester", "_tester"], ["_tester", "_tester"]]
    }

    test_dict = dg.generate(test_dict)
    for f,l in test_dict["people"]:
        assert f in gen._db["_tester"].values
        assert l in gen._db["_tester"].values

    # case: non-(string,list,dict) values
    test_dict = {
        "int" : 3, "float" : 2.07, "bool" : True, "null" : None
    }
    test_dict = dg.generate(test_dict)
    assert test_dict['int'] == 3
    assert test_dict['float'] == 2.07
    assert test_dict['bool'] == True
    assert test_dict['null'] == None

    # case: list
    test_list = ["_tester", "_tester"]
    test_list = dg.generate(test_list)
    assert test_list[0] in gen._db["_tester"].values
    assert test_list[1] in gen._db["_tester"].values

    # case: naked value
    test_val = "_tester"
    test_val = dg.generate(test_val)
    assert test_val in gen._db["_tester"].values

