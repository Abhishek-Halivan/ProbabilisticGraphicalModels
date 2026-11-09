% Dummy version of the ddebug pack so the reasoner loads without it.
% Only explain/1 needs the real pack.
:- module(ddebug, [ddebug/1]).

ddebug(_) :-
    throw(error(existence_error(pack, ddebug),
                context(explain/1, 'run pack_install(ddebug) for interactive explanations'))).
