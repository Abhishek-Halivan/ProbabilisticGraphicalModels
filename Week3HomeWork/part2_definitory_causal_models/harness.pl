% Runs one experiment and prints a RESULT line for each query.
% Called once per process since interventions can't be undone.

:- prolog_load_context(directory, Dir),
   atom_concat(Dir, '/shim', Shim),
   asserta(user:file_search_path(library, Shim)).

run_experiment(Reasoner, Model, Tables, Interventions, Queries) :-
    consult(Reasoner),
    forall(member(T, Tables), table(T)),
    load_model(Model),
    forall(member(X-V, Interventions), do(X, V)),
    forall(nth1(I, Queries, Q), report(I, Q)).

report(I, Q) :-
    catch(answer(Q, A), E, A = error(E)),
    format("RESULT\t~w\t~q~n", [I, A]),
    flush_output.

answer(value(X, _), A) :-
    !,
    (   value(X, V)
    ->  A = V
    ;   A = no_value
    ).
answer(Goal, A) :-
    (   call(Goal)
    ->  A = true
    ;   A = false
    ).
