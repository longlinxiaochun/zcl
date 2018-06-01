# -*- coding:utf-8 -*-
# print "hello world"
# print "say hello again"
# print "你好"  # this comment after is ignored
# 1 calculate exercise
# print 100-25*3+45/5
# print"is it ture or false",5>-2,5<=2  # 注意操作符前后空格
# print 4 % 2, 8.0 / 3.0, 8 / 3  # or enter "from_future_import division"
# 2 variable enter
# cars = 100
# space_in_a_car = 4.0
# drivers = 30
# passengers = 90
# cars_not_driven = cars-drivers
# cars_driven = drivers
# carpool_capacity = cars_driven*space_in_a_car
# print "we can transport", carpool_capacity, "people today"
# 3 more variable print
# name = 'Zed A. Shaw'
# age = 35  # not a lie
# height = 74  # inches
# weight = 180 # lbs
# eyes = 'Blue'
# teeth = 'White'
# hair = 'Brown'
# print "Let's talk about %s." % name
# print "He's %d inches tall." % height
# print "He's got %s eyes and %s hair." % (eyes, hair)
# print "If I add %d, %d,and %d I get %d." % (
#     age, height, weight, age + height + weight )
# print "He's %r cm tall" % height
# 4 print exercise
# formatter = "% r %r %r %r"
# print formatter % (1, 2, 3, 4)
# print formatter % ("one", "two", "three", "four")
# print formatter % (
#    "I had this thing." +"That you could type up right.",
#    "start",
#    "But it didn't sing.",
#    "so I said goodnight."
# )
# print """
# There's something going on here.
# With the three double-quotes.
# """
"""
tabby_cat = "\tI'm tabbed in."
persian_cat = "I'm split\non a line."
backslash_cat = "I'm \\ a \\ cat."
fat_cat = '''
I'll do a list:
\t* Cat food
\t* Catnip\n\t* Grass
'''
print tabby_cat
print persian_cat
print backslash_cat
print fat_cat
# the difference of %s and %r
print "%s" % tabby_cat
print "%r" % tabby_cat
"""
"""
print "How old are you?",  # 逗号让print不会结束这一行输入而跑到下一行
age = raw_input()
print "How tall are you?",
height = raw_input()
weight = raw_input("How much do you weight")
print "So,you're %r old, %r tall, %r heavy" % (
    age, height, weight)
help(raw_input)
from sys import argv
script, first, second, third = argv
print "The script is called:", script
print first
print second
print third
"""