from ducc import server


def test_decorator():
    @server.publisher
    def foo(msg, arga, argb):
        return msg, arga, argb
    assert foo(1, 2)(3) == (3, 1, 2)
