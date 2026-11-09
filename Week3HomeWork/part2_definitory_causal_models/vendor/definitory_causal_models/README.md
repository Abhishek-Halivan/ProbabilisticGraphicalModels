# Definatory Causal Models

## Goal and scope
This is an implementation of definitory causal models in Prolog.
Definatory causal models combine Boolean reasoning in Datalog with functional causal models.

Currently, the code in this repository works with the SWI dialect of Prolog together with the constraint logic programming system CLP(R), which fixes the domain of the models to be real numbers.
However, in future work it is intended also to support other domains, such as finite domains or the integers by moving beyond CLP(R) to e.g. CLP(FD) as a constraint logic programming system.

## Prerequisites
In addition to a fairly recent SWI-Prolog installation, navigating explanations requires the `ddebug` pack, which can be installed by calling `pack_install('ddebug')` from the Prolog top-level or `swipl pack install ddebug` from the command line.

## Specifying a model
Examples with a non-trivial Datalog part (`conservation.P`) and more interesting relational equations (`economy.P`) are included. They showcase the basic set-up.

In addition to the Datalog program itself, there should be attribute declarations, with a declaration `ext_attribute(Attribute)` for any extensional attribute which will be given directly and a declaration `int_attribute(Attribute)` for any intentional attribute for which defining equations will be provided.

This is followed by a declaration `primary(Predicate)` for the primary predicates used in the Datalog program. This is required to make use of interventional or explanatory reasoning.

Then follows the Datalog program itself, which should define equations for the intensional attributes.  Currently, the definitions allow for addition, multiplication and subtraction as well as multiset summation and multiplication using the `sum/2` and  `product/2` compound terms. They are invoked as `eq_relation(Attribute,Definition)`. Both `conservation.P` and `economy.P` show how these can be used.  It can also provide further background logic as well as Boolean causal relationships. This can be given as plain Prolog, although sometimes tabling may be needed to ensure termination of (positive or stratified) recursive programs.
For negated goals to be included in explanations appropriately, use `not/1` instead of `(\+)` to mark negation.

The concrete domains should be specified, as well as the values of the extensional attributes.  The former is done using plain Prolog facts, while the latter is achieved simply by writing the value in an additional argument. For instance, if `size(field)` is an extensional attribute of `field`, then `size(field,30)` defines its value to be 30.

## Loading a model
To load a model, consult the file `causal_reasoner.pl` and call the goal `load_model(ModelFile)`, where `ModelFile` contains the model specification (see above). `ModelFile` should be given in full and enclosed in single quotes (e.g. `'conservation.pl'`). This loads the Datalog clauses contained in `ModelFile`. Additional directives (e.g. tabling directives) should be given by the user before loading the clauses. for instance by calling `table connected/2` on the command line. For instance, in `conservation.pl`,  the directive `table connected/2` is required for `connected/2` to terminate.

## Querying a model
A model can be queried for numerical values by invoking the binary predicate `value(Attribute,Value)`; for instance, `value(size(field),S)` would query the size of the field, whether `size(field)` is an extensional or an intentional variable. In the latter case, CLP(R) will solve the entire system of equations and memoise (table) the outcome, so additional queries for the values of intensional attributes will not have to recompute the entire set of values.
Primary facts from the Datalog program can also be queried directly for Boolean outcomes.

## Explanations
After a model has been loaded, explanations can be viewed in two ways. They can be navigated interactively by calling `explain(Goal)` from the top-level. As when querying, use ordinary Datalog goals such as `explain(connected(s,e))` for primary goals and expressions such as `explain(value(birds(w),N))` for numerical attributes. This mechanism relies on Jan Wielemaker's `ddebug` pack for SWI-Prolog, which in turn implements ideas of Wlodek Drabent.  Note that unlike the static computation of explanation trees explained below, the interactive navigation does not work for tabled (sub)goals.
Alternatively, an explanation can be computed statically as a single tree data structure, represented as nested lists. This is called as `explanation(Goal,Explanation)`, where `Goal` is the query and `Explanation` is an unbound variable that will be instantiated with the explanation for the goal.
To give useful explanations for numerical attributes, the first call of `explain/1` or `explanation/2` augments the program with additional clauses for the attribute values that refer directly to the computed values.

## Interventions
Interventions, which alter the model by fixing certain values of numerical attributes or by setting primary facts to be true or false regardless of the remainder of the program, can be performed by calling `do(X,V)`. If `X` is a (ground) numerical attribute, `V` is the real number to which `X` should be set; if `X` is a ground primary atom such as `barrier(m,n)`, then `V` is either `true` or `false`.
Intervening abolishes the tables of all tabled predicates since their meanings may change in the new post-intervention program.




