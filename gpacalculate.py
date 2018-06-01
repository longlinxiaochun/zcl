def gpa_cal(grade, quantity):
    gpasum = 0
    l = len(grade)
    for i in range(l):
        gpasum = grade[i] * quantity[i] + gpasum
    gpa = gpasum / sum(quantity)
    return gpa


print "grade:"
my_grade = raw_input("> ")
print "quantity:"
my_quantity = raw_input("> ")
my_grade = my_grade.split(" ")
my_quantity = my_quantity.split(" ")
my_grade = [float(my_grade[i]) for i in range(len(my_grade))]
my_quantity = [float(my_quantity[i]) for i in range(len(my_quantity))]
print len(my_quantity), len(my_grade)
print gpa_cal(my_grade, my_quantity)
