import copy

import numpy as np

from hexrd.utils.decorators import memoize


def test_memoize():

    # This will only be set to true if memoization did not happen
    modified = False

    def was_memoized():
        # Get the state, and reset it
        nonlocal modified
        ret = not modified
        modified = False
        return ret

    @memoize
    def run(*args, **kwargs):
        nonlocal modified
        modified = True

    #### Basic tests #### noqa
    run(1, 3, var=10)
    assert not was_memoized()

    run(1, 3, var=10)
    assert was_memoized()

    run(1, 4, var=10)
    assert not was_memoized()

    run(1, 3, var=11)
    assert not was_memoized()

    run(1, 3, var=10)
    assert was_memoized()

    run(3, 1, var=10)
    assert not was_memoized()

    run(1, var1=3, var2=5)
    assert not was_memoized()

    run(1, var1=3, var2=5)
    assert was_memoized()

    run(1, var2=5, var1=3)
    assert was_memoized()

    run(1, var1=3, var2=6)
    assert not was_memoized()

    #### Test numpy arrays #### noqa
    array1 = np.arange(6).reshape(2, 3)
    array2 = copy.deepcopy(array1)
    array3 = np.arange(9)

    run(array1, array=array2)
    assert not was_memoized()

    run(array1, array=array2)
    assert was_memoized()

    # Arrays are identical
    run(array2, array=array1)
    assert was_memoized()

    # Array 3 is different
    run(array2, array=array3)
    assert not was_memoized()

    run(array2, array=array2)
    assert was_memoized()

    run(array1, array2)
    assert not was_memoized()

    run(array1, array2)
    assert was_memoized()

    # Show that it won't memoize if modified
    array1[0][0] = 3
    run(array1, array2)
    assert not was_memoized()

    # Modify it back and show that it is still memoized
    array1[0][0] = 0
    run(array1, array2)
    assert was_memoized()

    # It won't memoize if the shape is changed either
    run(array1, array2)
    assert was_memoized()

    run(array1, array2.reshape(3, 2))
    assert not was_memoized()

    run(array1, array2.reshape(2, 3))
    assert was_memoized()

    #### Test lists and dicts #### noqa
    list1 = [1, 2, 3]
    list2 = copy.deepcopy(list1)
    list3 = [5, 9, 8]

    dict1 = {'key1': 4, 'key2': 3}
    dict2 = copy.deepcopy(dict1)
    dict3 = {'key4': 1, 'key3': 2}

    run(list1, list2, dict1, dict2, kwarg=dict2)
    assert not was_memoized()

    run(list1, list2, dict1, dict2, kwarg=dict2)
    assert was_memoized()

    run(list2, list1, dict2, dict1, kwarg=dict1)
    assert was_memoized()

    run(list1, list3, dict1, dict2, kwarg=dict2)
    assert not was_memoized()

    run(list1, list2, dict1, dict2, kwarg=dict3)
    assert not was_memoized()

    dict2['key2'] = 4
    run(list1, list2, dict1, dict2, kwarg=dict2)
    assert not was_memoized()

    dict2['key2'] = 3
    run(list1, list2, dict1, dict2, kwarg=dict2)
    assert was_memoized()
