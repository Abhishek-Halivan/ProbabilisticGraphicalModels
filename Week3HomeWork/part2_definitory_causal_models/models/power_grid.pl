% Power grid: substations on a ring plus one spur.
%
%       a --- b
%       |     |
%       d --- c
%       |
%       e          (d-e breakers start open)
%
% energised/1 depends on itself around the ring, so it has to be tabled
% before loading (table energised/1).
%
% The numbers are still acyclic:
%   capacity, demand -> served -> total_served -> spare
%   capacity         -> online_capacity        -> spare

% Attribute declarations
ext_attribute(capacity(G)) :-
    generator(G).
ext_attribute(demand(X)) :-
    substation(X).

int_attribute(served(X)) :-
    substation(X).
int_attribute(total_served(grid)).
int_attribute(online_capacity(grid)).
int_attribute(spare(grid)).

% Primary predicates
candidate(energised(X)) :-
    substation(X).
candidate(online(G)) :-
    generator(G).
candidate(breaker_open(X,Y)) :-
    substation(X),
    substation(Y).

% Equations
eq_relation(served(X), sum(energised(X), demand(X))) :-
    substation(X).
eq_relation(total_served(grid), sum(substation(X), served(X))).
eq_relation(online_capacity(grid), sum(online(G), capacity(G))).
eq_relation(spare(grid), online_capacity(grid) - total_served(grid)).

% Boolean causal rules
online(G) :-
    generator(G),
    value(capacity(G),C),
    C > 0.

energised(X) :-
    online(X).
energised(Y) :-
    energised(X),
    linked(X,Y),
    not(breaker_open(X,Y)).

linked(X,Y) :-
    line(X,Y).
linked(X,Y) :-
    line(Y,X).

% Domains
substation(a).
substation(b).
substation(c).
substation(d).
substation(e).

generator(a).
generator(c).

line(a,b).
line(b,c).
line(c,d).
line(d,a).
line(d,e).

breaker_open(d,e).
breaker_open(e,d).

% Extensional attribute values
capacity(a,120).
capacity(c,0).

demand(a,10).
demand(b,20).
demand(c,30).
demand(d,40).
demand(e,50).
