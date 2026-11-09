:- module(causal_reasoner_core, [value/2, values/1]).
%:- meta_predicate value(1,?).
%:- meta_predicate transform_term(+,:,-).

:- use_module(library(clpr)).
%:- import {}/1 from clpr.
%:- import lookup/3 from pairlist.
:- table values/1.

value(X,Y) :-
    ext_attribute(X),
    call(X,Y).
value(X,Y) :-
    int_attribute(X),
    values(VarPairs),
    lookup(VarPairs,X,Y).

values(VarPairs):-
    setof(X, int_attribute(X), Atts),
    pairs_keys(VarPairs,Atts),
    setof(LHS-RHS, (eq_relation(LHS,RHS)), Equations),
    make_equations(VarPairs,Equations,VarEquations),
    add_all(VarEquations).

equation(VarPairs,LHS-RHS, NewLHS = NewRHS) :-
    transform_term(VarPairs,LHS,NewLHS),
    transform_term(VarPairs,RHS,NewRHS).

transform_term(VarPairs,T1 + T2, TT1 + TT2) :-
    !,
    transform_term(VarPairs,T1,TT1),
    transform_term(VarPairs,T2,TT2).
transform_term(VarPairs,T1 - T2, TT1 - TT2) :-
    !,
    transform_term(VarPairs,T1,TT1),
    transform_term(VarPairs,T2,TT2).

transform_term(VarPairs,T1 * T2, TT1 * TT2) :-
    !,
    transform_term(VarPairs,T1,TT1),
    transform_term(VarPairs,T2,TT2).
transform_term(VarPairs,sum(Condition, Term),TTerm) :-
    findall(Term,call(Condition),Terms),
    expand_sum(Terms,NewTerm),
    transform_term(VarPairs,NewTerm,TTerm).
transform_term(VarPairs,product(Condition, Term),TTerm) :-
    findall(Term,call(Condition),Terms),
    expand_product(Terms,NewTerm),
    transform_term(VarPairs,NewTerm,TTerm).

transform_term(_,Num,Num) :-
    number(Num),
    !.
transform_term(_,Term,Num) :-
    ext_attribute(Term),
    call(Term,Num),
    !.
transform_term(VarPairs,Term, Var) :-
    lookup(VarPairs,Term,Var),
    !.

expand_sum([],0).
expand_sum([T|Ts],T + ETs) :-
    expand_sum(Ts,ETs).

expand_product([],1).
expand_product([T|Ts],T * ETs) :-
    expand_product(Ts,ETs).

add_all([]).
add_all([X|Xs]) :-
    {X},
    add_all(Xs).

%pairs_keys([],[]).
%pairs_keys([T-_|Pairs],[T|Terms]) :-
%    pairs_keys(Pairs,Terms).

make_equations(_,[],[]).
make_equations(VarPairs,[Eq|Eqs],[VarEq|VarEqs]) :-
    equation(VarPairs,Eq,VarEq),
    make_equations(VarPairs,Eqs,VarEqs).

lookup([K - V | KVs],Key,Value) :-
        ( K = Key ->
                V = Value
        ;
                lookup(KVs,Key,Value)
        ).


