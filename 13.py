class Parent(object):

    def implicit(self):
        print "PARENT implicit()"

    def override(self):
        print "PARENT override()"

    def altered(self):
        print "PARENT altered()"


class Child(Parent):

    def override(self):
        print "CHILD override()"

    def altered(self):
        print "CHILD, BEFORE PARENT altered()"
        super(Child, self).altered()
        print "CHILD, AFTER PARENT altered()"

class other(object):
    def __init__(self):
        self.parent = Parent()

    def implicit(self):
        self.parent.implicit()

    def override(self):
        print "OTHER override()"

    def altered(self):
        print "OTHER, BEFORE OTHER altered()"
        self.parent.altered()
        print "OTHER, AFTER OTHER altered()"

dad = Parent()
son = Child()
girl = other()

dad.implicit()
son.implicit()
dad.override()
son.override()
dad.altered()
son.altered()
girl.implicit()
girl.override()
girl.altered()