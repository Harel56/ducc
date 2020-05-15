from ducc import saver


def test_class_init():
    s = saver.Saver("mysql://host:4444")
    assert s.scheme == "mysql"
