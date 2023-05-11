class A:
    def __init__(self):
        print("Function A is called")
        B()
        F()
        insidiest()

class B:
    def __init__(self):
        print("Function B is called")
        C()

class C:
    def __init__(self):
        print("Function C is called")
        self.cIn()
        self.cInThree()

    def cIn(self):
        def cInTwo():
            print("a")
            print("b")
        cInTwo()

    def cInThree(self):
        print("c")
        D()

class D:
    def __init__(self):
        print("Function D is called")
        E()

class E:
    def __init__(self):
        self.inside()
        print("Function E is called")
        F()

    def inside(self):
        def insider():
            def insidiest():
                print("Comically nested functions.")
            insidiest()
            print("We're so in")
        insider()
        print("Wow...?")