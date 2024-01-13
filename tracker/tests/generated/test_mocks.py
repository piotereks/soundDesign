import pytest
from unittest.mock import MagicMock, Mock, patch, call, sentinel
import asyncio

class SomeClass():
    # def __init__(self):
    #     pass
    def method(self, a, b, c, key):
        print("Hello")
        return 123


def test_something():
    real = SomeClass()
    # real.method = MagicMock(name='method', return_value=666)
    xxx = real.method(3, 4, 5, key='value')
    pass


class ProductionClass_1:
    def method(self):
        self.something(1, 2, 3)

    def something(self, a, b, c):
        pass

def test_production():

    real = ProductionClass_1()
    real.something = MagicMock(name='something')
    real.method()
    real.something.assert_called_once_with(1, 2, 3)
    real.something.assert_called_with(1, 2, 3)

class ProductionClass:
    def closer(self, something):
        something.close()

def test_pr2():
    real = ProductionClass()
    mock = Mock()
    real.closer(mock)
    mock.close.assert_called_with()
    pass


# class Foo():
#     def methodx(self):
#         return 'class defined'
def some_function():
    instance = module.Foo()
    return instance.method()

import module

# xxx = module.Foo()

def test_some_f():
    with patch('module.Foo') as mock:
        instance = mock.return_value
        instance.method.return_value = 'the result'
        result = some_function()
        assert result == 'the result'

def test_named_mock():
    mock = MagicMock(name='foo')
    x = 1

def test_tracking_all_calls():
    # mock = MagicMock()
    mock = Mock()
    mock.method()
    mock.attribute.method(10, x=53)
    pass
    # mock.mock_calls
    # expected = [call.method(), call.attribute.method(10, x=53)]
    # assert mock.mock_calls == expected

def test_attrib_return():
    # Return value
    #1
    mock = Mock()
    mock.method.return_value = 123
    result = mock.method()
    assert result == 123
    #2
    mock = Mock()
    mock.method.return_value = 3
    mock.method()
    #3
    mock = Mock(return_value=33)
    mock()

    # attribute set
    mock = Mock()
    mock.x = 13
    mock.x

    # complex mock
    mock = Mock()
    cursor = mock.connection.cursor.return_value
    cursor.execute.return_value = ['foo']

    mock.connection.cursor().execute("SELECT 1")
    expected = call.connection.cursor().execute("SELECT 1").call_list()

    # mock.mock_calls
    # [call.connection.cursor(), call.connection.cursor().execute('SELECT 1')]

    mock.mock_calls == expected

    # Exceptions
    mock = Mock(side_effect=Exception('Boom!'))
    mock()

    # side effects and iterations
    mock = MagicMock(side_effect=[4, 5, 6])
    mock()
    mock()
    mock()

    # side effects with function
    vals = {(1, 2): 1, (2, 3): 2}

    def side_effect(*args):
        return vals[args]

    mock = MagicMock(side_effect=side_effect)
    mock(1, 2)
    mock(2, 3)

    # mock async
    mock = MagicMock()  # AsyncMock also works here
    mock.__aiter__.return_value = [1, 2, 3]

    async def main():
        return [i async for i in mock]

    asyncio.run(main())

class SomeClass:
    attribute = 123

def test_patch_object():
    original = SomeClass.attribute

    # attribute is patched only within scope of test()
    @patch.object(SomeClass, 'attribute', sentinel.attributex)
    def test():
        print('xxx')
        print(sentinel.attributex)
        print('yyy')
        assert SomeClass.attribute == sentinel.attributex

    test()
    assert SomeClass.attribute == original
    pass
    #
    # assert SomeClass.attribute == original

    # @patch('package.module.attribute', sentinel.attribute)
    # def test():
    #     from package.module import attribute
    #
    #     assert attribute is sentinel.attribute
    #
    # test()