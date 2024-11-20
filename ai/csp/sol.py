from cProfile import Profile
from pstats import SortKey, Stats
from mytypes import Variable, Assignment, CSP, Inferences
from nqueen import NQueensProblem, show
from collections import defaultdict

from copy import deepcopy

def backtrack_search[T](p: CSP[T]) -> Assignment[T] | None:
    unassigned_var = p.assignment.get_one_unassigned()

    if unassigned_var is None:
        return p.assignment

    for v in p.get_domain(unassigned_var):
        if not p.assignment.will_be_consistent(unassigned_var, v):
            continue

        unassigned_var.assign(v)

        result = backtrack_search(p)

        if result is not None:
            return result

        unassigned_var.unassign()
    
    return None

#BacktrackSearch(prob, assign, inferences)
#    if AllVarsAreAssigned(prob, assign)
#        return assign
#    
#    var = pick an unassigned var(prob,assign)
#    
#    for val in PossibleValuesOfVar(var,prob,assign)
#        if (val is consistent with assignment)
#            add {var=val} to assign
#
#        inference = Infer(prob, var, assign)
#
#        add inference to inferences
#
#        if (inference != failure)
#            result = BackTrackSearch(prob, assign, inferences)
#
#        if (result != failure)
#            return result
#
#        remove {var=value} and inference from inferences
#
#    return failure
#

def compute_domain[T](p: CSP[T], var: Variable[T], inferences: Inferences[T]) -> set[T]:
    domain = p.get_domain(var)

    restrictions = inferences.get_inference(var)
    return domain - restrictions

def backtrack_search_infer[T](p: CSP[T], inferences: Inferences[T]) -> Assignment[T] | None:
    unassigned_var = p.assignment.get_one_unassigned()
    if unassigned_var is None:
        return p.assignment

    for v in compute_domain(p, unassigned_var, inferences):
        unassigned_var.assign(v)

        new_inferences = infer(p, unassigned_var, inferences)

        if new_inferences is not None:
            result = backtrack_search_infer(p, new_inferences)

            if result is not None:
                return result

        unassigned_var.unassign()
    
    return None


def infer[T](p: CSP[T], v: Variable[T], inferences: Inferences[T]) -> Inferences[T] | None:
    var_queue = set([v])
    inferences = inferences.__deepcopy__(None)

    while var_queue:
        var = var_queue.pop()

        unassigned_vars = (v for v in p.assignment.vars if not v.is_assigned() and v.id > var.id)

        for free_var in unassigned_vars:
            initial_domain = compute_domain(p, free_var, inferences)
            for value in initial_domain:
                if not p.assignment.will_be_consistent(free_var, value):
                    inferences.add(free_var, value)

            new_domain = compute_domain(p, free_var, inferences)

            if not new_domain:
                return None

            continue

            if initial_domain != new_domain:
            #if initial_domain != new_domain and len(new_domain) == 1:
                var_queue.add(free_var)

    return inferences

N = 18
with Profile() as profile:
    print(backtrack_search_infer(NQueensProblem(N), NQueensProblem.Inferences()))
    
    Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats()

with Profile() as profile:
    print(backtrack_search(NQueensProblem(N)))
    
    Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats()

#Infer(prob, var, assign)
#    inference = []
#    varQueue = [var]
#    while (varQueue is not empty)
#        Y = varQueue.pop()
#        
#        for constraint where Y in (constraints with variable Y)
#            for all X in variables of constraint that is not Y
#                S = ComputeDomain(x, assign, inference)
#                
#                for each v in S
#                    if {x = v} is not consistent
#                        inference.add({x != v})
#    
#            T = ComputeDomain(x, assign, inference)
#
#            if T is empty
#                return Failure
#
#            if S != T
#                varQueue.add(x)
#                
#    return inference
#
