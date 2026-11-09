%:- auto_table.
%:- table connected/2.
%:- use_module(causal_reasoner_core).

% Declarations for attributes
ext_attribute(trees(X)) :-
    plot(X).

ext_attribute(size(X)) :-
    plot(X).

int_attribute(birds(X)) :-
    plot(X).

% Domain declarations
candidate(connected(X,Y)) :-
    plot(X),
    plot(Y).
candidate(adjacent(X,Y)) :-
    plot(X),
    plot(Y).
candidate(barrier(X,Y)) :-
    plot(X),
    plot(Y).




% The Datalog program

eq_relation(birds(X), 5 * (trees(X) * sum(connected(X,Y), size(Y)))) :-
    plot(X).

connected(X,X) :-
    value(trees(X),T),
    T > 0.
connected(X,Y) :-
    connected(X,Z),
    adjacent(Z,Y),
    \+ barrier(Z,Y),
    value(trees(Y),T),
    T > 0.

adjacent(X,m) :-
    plot(X),
    X \= m.
adjacent(m,X) :-
    plot(X),
    X \= m.

barrier(n,m).
barrier(m,n).


% Domains
plot(n).
plot(m).
plot(e).
plot(w).
plot(s).

% Extensional attribute values
size(n,100).
size(w,100).
size(m,100).
size(e,100).
size(s,200).

trees(n,100).
trees(w,0).
trees(m,100).
trees(e,100).
trees(s,50).

