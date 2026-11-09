# Causal models exercises

| Exercise | Files |
|---|---|
| 1. Functional causal model | [SOLUTION.md](part1_functional_causal_model/SOLUTION.md), [fcm.py](part1_functional_causal_model/fcm.py) |
| 2.1 Cyclic models | [power_grid.pl](part2_definitory_causal_models/models/power_grid.pl), [flood_watch.pl](part2_definitory_causal_models/models/flood_watch.pl) |
| 2.2 Interventions | [run_experiments.py](part2_definitory_causal_models/run_experiments.py), [RESULTS.md](part2_definitory_causal_models/RESULTS.md) |

## Running it

Part 1 only needs Python:

```
cd part1_functional_causal_model
python fcm.py
```

Part 2 needs SWI-Prolog (tested on 10.0.2):

```
cd part2_definitory_causal_models
python run_experiments.py
```

This runs every experiment on the original reasoner and on the version in `patched/`, then writes the comparison to `RESULTS.md`. Each experiment gets its own Prolog process, because `do/2` changes the loaded program and there's no way to undo it.

You don't need the `ddebug` pack. `shim/ddebug.pl` is a dummy replacement so that the reasoner loads, and only the interactive `explain/1` would need the real thing.

`vendor/definitory_causal_models/` is an unchanged copy of <https://codeberg.org/felix_weitkaemper/definitory_causal_models> (MIT licence). `patched/` has the two reasoner files with fixes for the problems described below.

## Models

`power_grid.pl` has power spreading around a ring of substations, so `energised/1` depends on itself. The numbers are acyclic: capacity and demand give the served load, then the total served, then the spare capacity.

`flood_watch.pl` has two river basins that relay warnings to each other, so `warned/1` is cyclic. The chain rainfall -> runoff -> alert -> warned -> cost has no numerical cycle. The difference from the grid model is that a logical rule reads an intensional attribute (`runoff`).

## Did the interventions match expectations?

Mostly, but not all of them. The expected values were fixed before running anything.

| Reasoner | Queries matching the expected value |
|---|---|
| Original | 84 of 113 |
| Patched | 113 of 113 |

Numerical interventions and interventions on non-recursive logic atoms all worked on the original reasoner. The 29 mismatches came from two problems:

1. Interventions on atoms of a predicate with several clauses (13 mismatches, in G4, G5, F4 and C6). `prepare/1` retracts inside its loop, so each clause deletes the ground copies made from the clause before, and only the last clause is left. In the grid this removes the base case of `energised/1`, so forcing `energised(e)` on actually turns the rest of the grid off. F5 looks correct on the original, but only by luck, since the deleted clause is the one that would have triggered the second problem.
2. Logic that reads an intensional attribute (16 mismatches, in F0, F1, F2, F3 and F6). `values/1` solves all the equations at once and is tabled, so a rule reading `runoff` re-enters `values/1` while it's still running, and SWI-Prolog throws an error. The model isn't cyclic at the ground level, so this is a limitation of the implementation. It does mean `flood_watch.pl` only runs on the patched version, even with no intervention.

The version in `patched/` solves only the equations an attribute depends on. Numerical cycles still work, since the whole cycle ends up in one system (Y0 and Y1). A real cycle through both the logic and the numbers would not terminate.
