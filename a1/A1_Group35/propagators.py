# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#

from collections import deque

#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    if not newVar:
        return True, []
    
    prune_list = []
    
    for constraint_with_newvar in csp.get_cons_with_var(newVar):
        for unassigned_variable in constraint_with_newvar.get_unasgn_vars():
            for domain_element in unassigned_variable.cur_domain():
                if not constraint_with_newvar.check_var_val(unassigned_variable, domain_element):
                    unassigned_variable.prune_value(domain_element)
                    prune_list.append((unassigned_variable, domain_element))
            if unassigned_variable.cur_domain_size() == 0:
                return False, prune_list
            
    return True, prune_list




    pass


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    arc_queue = set()

    '''Run Forward Checking First'''

    pruned_list = set()

    '''if no new varible assigned, check all constraints in the csp
    if new varible is assigned check all contraints with the new variable'''
    if not newVar:
        for constraint in csp.get_all_cons():
            for variable in constraint.get_unasgn_vars():
                arc_queue.add((variable, constraint))
    else:
        for constraint_with_newvar in csp.get_cons_with_var(newVar):
            for variable in constraint_with_newvar.get_unasgn_vars():
                arc_queue.add((variable, constraint_with_newvar))


    while len(arc_queue) > 0:
        variable, constraint = arc_queue.pop()
        for domain_value in variable.cur_domain():
            domain_changed = False
            if not constraint.check_var_val(variable, domain_value):
                domain_changed = True
                variable.prune_value(domain_value)
                pruned_list.add((variable,domain_value))
        if variable.cur_domain_size() == 0:
            return False, list(pruned_list)
        if domain_changed:
            domain_changed = False
            for constraint_under_dequeue_var in csp.get_cons_with_var(variable):
                if  (constraint_under_dequeue_var != constraint) and ((variable, constraint_under_dequeue_var) not in arc_queue):
                    if (constraint_under_dequeue_var.get_n_unasgn() > 0):
                        arc_queue.add((variable, constraint_under_dequeue_var))

    return True, list(pruned_list)






