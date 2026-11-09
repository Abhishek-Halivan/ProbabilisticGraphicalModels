:- use_module(library(ddebug)).
:- use_module(causal_reasoner_core).

:- dynamic int_attribute/1, ext_attribute/1, eq_relation/2, candidate/1.

:- table value_list/2.
:- table explanation/3.

load_model(File) :-
%   consult(value_writer),
    load_clauses(File).

load_clauses(File) :-
        setup_call_cleanup(
            open(File, read, Stream),
            load_clauses_from_stream(Stream),
            close(Stream)).

load_clauses_from_stream(Stream) :-
        read(Stream, T0),
        load_clauses(T0, Stream).

load_clauses(end_of_file, _) :- !.
load_clauses(Clause, Stream) :- !,
        assert(Clause),
        read(Stream, T2),
        load_clauses(T2, Stream).

explain(A) :-
    assert_values_if_needed,
    ddebug(A).

explanation(A,E) :-
    assert_values_if_needed,
    explanation(A,[],E).

explanation(P,[P|Es],[P]) :-
    predicate_property(P,built_in),
    call(P),
    \+memberchk(P,Es).

explanation(P,Es,[P|E]) :-
    \+ predicate_property(P,built_in),
    clause(P,B),
    call(B),
    commalist_to_list(B,BList),
    disjoint(BList,Es),
    maplist(explanation_(Es),BList,E).

explanation_(Es,B,E) :-
    explanation(B,[B|Es],E).

commalist_to_list((H,T),[H|TList]) :-
    commalist_to_list(T,TList).
commalist_to_list(X,[X]) :-
    X \= (_,_).

disjoint(BList,Es) :-
    forall(member(B,BList),\+memberchk(B,Es)).



% Utilities for asserting values before explanation

assert_values_if_needed :-
    (   predicate_property(value(_,_),imported_from(_))
    ->  assert_values
    ;   true).

assert_values :-
    abolish(value/2),
    forall(any_attribute(A),assert_attribute_clause(A)).

assert_attribute_clause(A) :-
    attribute_clause(A,Clause),
    assert(Clause).

attribute_clause(A,value(A,V)) :-
    ext_attribute(A),
    call(A,V).

attribute_clause(A,(value(A,V) :- Body)) :-
    int_attribute(A),
    causal_reasoner_core:value(A,V),
    eq_relation(A,F),
    value_cslist(A,F,Body).

value_cslist(A,F,Result) :-
    value_list(F,ValueList),
    condition_list(F,CondList),
    append(CondList,ValueList,BodyList),
    (    BodyList = []
    -> Result = eq_relation(A,F)
    ;
    sort(BodyList,UniqueBL),
    list_to_cs(UniqueBL,Body),
    Result = (eq_relation(A,F),Body)).

value_list(F1+F2,List) :-
    !,
    value_list_([F1,F2],List).
value_list(F1*F2,List) :-
    !,
    value_list_([F1,F2],List).
value_list(sum(Cond,Term),List) :-
    !,
    findall(Term,call(Cond),Terms),
    value_list_(Terms,List).
value_list(product(Cond,Term),List) :-
    !,
    findall(Term,call(Cond),Terms),
    value_list_(Terms,List).
value_list(N,[]) :-
    number(N),
    !.
value_list(A,[value(A,V)]) :-
    any_attribute(A),
    value(A,V),
    !.
value_list_([],[]).
value_list_([H|T],List) :-
    value_list(H,L1),
    value_list_(T,L2),
    append(L1,L2,List).

condition_list(F1+F2,List) :-
    !,
    condition_list_([F1,F2],List).
condition_list(F1*F2,List) :-
    !,
    condition_list_([F1,F2],List).
condition_list(sum(Cond,_),List) :-
    !,
    collect_conditions(Cond,List).
condition_list(product(Cond,_),List) :-
    !,
    collect_conditions(Cond,List).
condition_list(N,[]) :-
    number(N),
    !.
condition_list(A,[]) :-
    any_attribute(A),
    !.

collect_conditions((C1,C2),List) :-
    !,
    collect_conditions(C1,List1),
    collect_conditions(C2,List2),
    append(List1,List2,List).
collect_conditions(Condition,List) :-
    findall(Checked, (candidate(Condition),check_condition(Condition,Checked)),List).

check_condition(Candidate,Checked) :-
    (   call(Candidate)
    ->  Checked = Candidate
    ;   Checked = not(Candidate)
    ).

condition_list_([],[]).
condition_list_([H|T],List) :-
    condition_list(H,L1),
    condition_list_(T,L2),
    append(L1,L2,List).

% Interventions

do(X,V) :-
    restore_defaults,
    intervene(X,V).

do([]).
do([X-V|T]) :-
    do(X,V),
    do(T).

intervene(Attr,N) :-
    ext_attribute(Attr),
    !,
    Attr =.. AttrList,
    append(AttrList,[_],CAttrList),
    CAttr =.. CAttrList,
    prepare_ext(Attr),
    retractall(CAttr),
    append(AttrList,[N],NAttrList),
    NAttr =.. NAttrList,
    assert(NAttr).
intervene(Attr,N) :-
    int_attribute(Attr),
    !,
    prepare_eq_relation(Attr),
    retractall(eq_relation(Attr,_)),
    assert(eq_relation(Attr,N)).
intervene(Fact,true) :-
    prepare(Fact),
    retractall(Fact),
    assert(Fact).
intervene(Fact,false) :-
    prepare(Fact),
    retractall(Fact).

restore_defaults :-
    (   predicate_property(value(_,_),imported_from(_))
    ->  true
    ;   abolish(value/2)),
    abolish_all_tables.

prepare(X) :-
    arg_vars(X,T),
    findall((T :- B), (clause(T,B), candidate(T)), Clauses),
    forall(member((Head :- _), Clauses), retractall(Head)),
    forall(member(Clause, Clauses), assert(Clause)).

prepare_ext(Attr) :-
    arg_vars(Attr,VarAttr),
    VarAttr =.. VarAttrList,
    append(VarAttrList,[_],VarCAttrList),
    T =.. VarCAttrList,
    forall((clause(T,B), ext_attribute(VarAttr)),(retractall(T), assert((T :-B)))).

prepare_eq_relation(Attr) :-
    arg_vars(Attr,T),
    forall((clause(eq_relation(T,F),B), int_attribute(T)),(retractall(T), assert((eq_relation(T,F):-B)))).

arg_vars(X,T) :-
    X =.. [F|ArgList],
    to_vars(ArgList,VarList),
    T =.. [F|VarList].

to_vars([],[]).
to_vars([_|T],[_|TVars]) :-
    to_vars(T,TVars).


any_attribute(X) :-
    ext_attribute(X).
any_attribute(X) :-
    int_attribute(X).

list_to_cs([A],A).
list_to_cs([A|[B|T]],(A,CommaList)) :-
    list_to_cs([B|T],CommaList).

