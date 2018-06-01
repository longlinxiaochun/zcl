# -*- coding:utf-8 -*-
def printnum(k):
    i = 0
    numbers = []

    while i < k:
        print "At the top i is %d" % i
        numbers.append(i)
        i = i + 1
        print "Numbers now:", numbers
        print "At the bottom i is %d" % i

    print "The numbers:"
    for num in numbers:
        print num
print "How many numbers do you want to print"
k = int(raw_input())  # raw_input输入类型为str，需要转换为int
printnum(k)
"""
the_count = [1, 2, 3, 4, 5]
fruits = ['apples', 'oranges', 'pears', 'apricots']
change = [1, 'pennies', 2, 'dimes', 3, 'quarters']

k = range(1, 3)  # k=[1,2]
print k
for number in k:
    print "This is count %d" % number
elements = []
for i in range(0, 6):
    print "Adding %d to the list" % i
    elements.append(i)
for i in elements:
    print "Element was: %d" % i
"""
