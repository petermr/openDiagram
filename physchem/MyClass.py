class MyClass:
    """A simple example class"""
    i = 12345

    def f(self):
        print("ctr")
        return 'hello world'

    def test():
        print("TEST")
        mc = MyClass()
        print ("hw", mc.f())


if __name__ == '__main__':
    print("class called")
    MyClass.test()
