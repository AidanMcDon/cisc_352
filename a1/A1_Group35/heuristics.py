# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    '''Return variables according to the Degree Heuristic.'''
    best = -1  # Initialize with negative infinity
    best_var = None
    degree = 0
    for var in csp.get_all_unasgn_vars():
        # Calculate the degree (number of constraints involving other unassigned variables)
        for con in csp.get_cons_with_var(var):
            degree += 1
        if degree > best:
            best = degree
            best_var = var
        degree = 0
    return best_var

def ord_mrv(csp):
    '''Return variable according to the Minimum Remaining Values heuristic.'''
    best = float('inf')  # Initialize
    best_var = None
    for var in csp.get_all_vars():
        size = var.cur_domain_size()
        if size < best:
            best = size
            best_var = var
    return best_var