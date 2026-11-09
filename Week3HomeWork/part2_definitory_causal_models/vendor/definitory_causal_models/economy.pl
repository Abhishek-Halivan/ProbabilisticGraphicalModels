%:- use_module(causal_reasoner_core).

% Declarations for numeric attributes
int_attribute(purchase(D,G)) :-
    department(D),
    good(G).

int_attribute(demand(G)) :-
    good(G).

ext_attribute(needs(D,G)) :-
    department(D),
    good(G).

ext_attribute(base_demand(G)) :-
    good(G).

% Domain declarations for primary predicates
candidate(directive(X,Y)) :-
    department(X),
    good(Y).

% Domains

good(stationery).
good(computers).

department(finance).
department(interior).
department(exterior).

% Extensional attribute values
needs(finance,stationery,3000).
needs(interior,stationery,300).
needs(exterior,stationery,500).
needs(finance,computers,1000).
needs(interior,computers,600).
needs(exterior,computers,100).

base_demand(computers,1100).
base_demand(stationery,5000).

% Datalog program
eq_relation(demand(G), base_demand(G) + sum(department(D),purchase(D,G))) :-
    good(G).

eq_relation(purchase(D,G),needs(D,G)) :-
    directive(D,G).
eq_relation(purchase(D,G),0) :-
    department(D),
    good(G),
    \+directive(D,G).

directive(finance,stationery).
directive(finance,computers).





