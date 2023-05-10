def a():
    print("Function A is called")
    b()

def b():
    print("Function B is called")
    c()

def c():
    print("Function C is called")

    def cIn():
        def cInTwo():
            print("a")
            print("b")

        cInTwo()


    def cInThree():
        print("c")
        
    d()

def d():
    print("Function D is called")
    e()

def e():

    def inside():

        def insider():

            def insidiest():
                print("Comically nested functions.")

            insidiest()
            print("We're so in")

        insider()
        print("Wow...?")

    inside()
    print("Function E is called")