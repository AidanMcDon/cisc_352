# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *

def binary_ne_grid(cagey_grid):
    n = cagey_grid[0]

    vars = []
    cons = []


    '''Domain from 1 to n for all variables
    satisfying tuples from 1 to n with none matching'''
    dom = []
    sat_tuple = []
    for i in range(n):
        dom.append(i)
        for j in range(n):
            if i != j:
                sat_tuple.append((i + 1,j + 1))
                sat_tuple.append((j + 1,i + 1))


    

    

    for i in range(n * n):
        vars.append(Variable(str(i),dom))

    for i in range(n*n):
        for j in range(i % n):
            new_con = Constraint("R" + str(i) + str(j), [vars[i], vars[i-j-1]])
            new_con.add_satisfying_tuples(sat_tuple)
            cons.append(new_con)
        for j in range(i // n):
            new_con = Constraint("C" + str(i) + str(j), [vars[i], vars[i-j*n-1]])
            new_con.add_satisfying_tuples(sat_tuple)
            cons.append(new_con)

    csp = CSP("binary",vars)
    for con in cons:
        csp.add_constraint(con)

    return [csp, vars]



    


    pass


def nary_ad_grid(cagey_grid):
    n = cagey_grid[0]

    vars = []
    cons = []


    '''Domain from 1 to n for all variables
    satisfying tuples from 1 to n with none matching'''
    dom = []
    sat_tuple = []
    for i in range(n):
        dom.append(i)
        new_sat_tuple = []
        for j in range(n):
            new_sat_tuple.append((i + j) % n)
        sat_tuple.append(new_sat_tuple)


    


    

    

    for i in range(n * n):
        vars.append(Variable(str(i),dom))

    for i in range(n):
        new_con_row = []
        new_con_col = []
        for j in range(n):
            new_con_row.append(vars[i * n + j ])
            new_con_col.append(vars[j * n + i ])
        new_con_row = Constraint("R" + str(i), tuple(new_con_row))
        new_con_col = Constraint("C" + str(i), tuple(new_con_col))
        new_con_row.add_satisfying_tuples(sat_tuple)
        new_con_col.add_satisfying_tuples(sat_tuple)
        cons.append(new_con_col)
        cons.append(new_con_row)

    csp = CSP("nary", vars)
    for con in cons:
        csp.add_constraint(con)

    return [csp, vars]
    pass

def cagey_csp_model(cagey_grid):
    ##IMPLEMENT
    pass


if __name__ == '__main__':
    b = (3, [(2, [(1, 1), (1, 2)], '-'), (2, [(1, 3)], '?'), (2, [(2, 1), (3, 1)], '/'), (3, [(2, 2), (2, 3)], '/'),
                 (1, [(3, 2), (3, 3)], '-')])



    csp_nary = nary_ad_grid(b)[0]
    constraints_nary = csp_nary.get_all_cons()
