from constraint import AllDifferentConstraint
import constraint


def stringSumCheckCaesar(s, i, n, c, e, j, u, l, a, r):
    return addChars([s, i, n, c, e]) + addChars([j, u, l, i, u, s]) == addChars([c, a, e, s, a, r])

def stringSumCheckTires(c, h, e, k, t, i, r, s):
    return addChars([c, h, e, c, k]) + addChars([t, h, e]) == addChars([t, i, r, e, s])

def stringSumCheckLucky(d, o, y, u, f, e, l, c, k):
    return addChars([d, o]) + addChars([y, o, u]) + addChars([f, e, e, l]) == addChars([l, u, c, k, y])

def addChars(chars):
    total = 0
    cnt = 0
    #starting at the last char in the string, multiply by the correct power of 10
    for char in chars[::-1]:
        total += char * pow(10, cnt)
        cnt += 1
    return total

p = constraint.Problem()

"""
# Problem 1.1
# unique variables include: S, I, N, C, E, J, U, L, A, R
p.addVariables("ineular", range(10))
p.addVariables("sjc",     range(1,10))
p.addConstraint(stringSumCheckCaesar, "sincejular")
"""

"""
# Problem 1.2
# unique variables: C, H, E, K, T, I, R, S
p.addVariables("hekirs", range(10))
p.addVariables("ct",     range(1,10))
p.addConstraint(stringSumCheckTires, "chektirs")
"""

# Problem 1.3
# do + you + feel = lucky
# unique variables: D, O, Y, U, F, E, L, C, K
p.addVariables("oueck", range(10))
p.addVariables("dyfl",  range(1,10))
p.addConstraint(stringSumCheckLucky, "doyufelck")

p.addConstraint(AllDifferentConstraint())

solutions = p.getSolutions()

length = len(solutions)
print("Solutions: ")
for index, solution in enumerate(solutions):
    print(solution)

print("Number of solutions: ", length)
