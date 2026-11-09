% Flood warnings passed between river basins over radio.
%
% north and east relay warnings to each other, so warned/1 is cyclic and has
% to be tabled before loading (table warned/1). A warning has to start from a
% real alert, the loop alone shouldn't keep it alive.
%
% No numerical cycle:
%   rainfall, area -> runoff -> alert -> warned -> response_cost -> total_cost
%
% Unlike power_grid.pl, a logical rule here reads an intensional attribute
% (runoff).

% Attribute declarations
ext_attribute(rainfall(B)) :-
    basin(B).
ext_attribute(area(B)) :-
    basin(B).
ext_attribute(response(B)) :-
    basin(B).

int_attribute(runoff(B)) :-
    basin(B).
int_attribute(response_cost(B)) :-
    basin(B).
int_attribute(total_cost(all)).

% Primary predicates
candidate(alert(B)) :-
    basin(B).
candidate(warned(B)) :-
    basin(B).
candidate(channel(X,Y)) :-
    basin(X),
    basin(Y).

% Equations
eq_relation(runoff(B), rainfall(B) * area(B)) :-
    basin(B).
eq_relation(response_cost(B), sum(warned(B), response(B))) :-
    basin(B).
eq_relation(total_cost(all), sum(basin(B), response_cost(B))).

% Boolean causal rules
alert(B) :-
    basin(B),
    value(runoff(B),R),
    R > 50.

warned(B) :-
    alert(B).
warned(Y) :-
    warned(X),
    channel(X,Y).

% Domains
basin(north).
basin(east).
basin(south).

channel(north,east).
channel(east,north).

% Extensional attribute values
rainfall(north,10).
rainfall(east,2).
rainfall(south,3).

area(north,8).
area(east,5).
area(south,4).

response(north,100).
response(east,60).
response(south,40).
