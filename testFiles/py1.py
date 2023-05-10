def a():
    print("Function A is called")
    b()

def b():
    print("Function B is called")
    c()

def c():
    print("Function C is called")
    d()

def d():
    print("Function D is called")
    e()

def e():
    def inside():
        print("We're so in")
        def insider():
            print("Wow...?")
            def insidiest():
                print("Comically nested functions.")

            insidiest()
        insider()
    inside()
    print("Function E is called")