# 1
def print_two(*args):
    arg1, arg2 = args
    print "arg1: %r, arg2: %r" % (arg1, arg2)


# 2
def print_two_again(arg1, arg2):
    print "arg1: %r, arg2: %r" % (arg1, arg2)


# 3
def print_one(arg1):
    print "arg1: %r" % arg1


# 4
def print_none():
    print "I got nothin'."


# 5 exercise
def max(a, b):
    if a < b:
        print b
    else:
        print a

print_two("Zed", "Shaw")
print_two_again("Zed", "Shaw")
print_one("First!")
print_none()
max(2, 3)

