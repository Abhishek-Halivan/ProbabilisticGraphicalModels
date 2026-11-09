# Checks the numbers in SOLUTION.md by going through all noise settings.

from fractions import Fraction as Fr
from itertools import product

VARIABLES = ["S", "M", "O", "F", "D"]
PARENTS = {"S": [], "M": [], "O": ["S", "M"], "F": ["O"], "D": ["S"]}

# Probability that each independent noise variable is true.
NOISE = {
    "U_S": Fr(1, 5),    # a storm happens
    "U_M": Fr(3, 10),   # maintenance is overdue
    "U_SO": Fr(1, 2),   # the storm is strong enough to cut the power
    "U_MO": Fr(2, 5),   # the neglected equipment fails
    "U_O": Fr(1, 10),   # the power fails for some other reason
    "U_OF": Fr(3, 5),   # the outage lasts long enough to spoil the food
    "U_F": Fr(1, 20),   # the food spoils for some other reason
    "U_SD": Fr(7, 10),  # the storm blocks the commute
}

MECHANISMS = {
    "S": lambda v, u: u["U_S"],
    "M": lambda v, u: u["U_M"],
    "O": lambda v, u: (v["S"] and u["U_SO"]) or (v["M"] and u["U_MO"]) or u["U_O"],
    "F": lambda v, u: (v["O"] and u["U_OF"]) or u["U_F"],
    "D": lambda v, u: v["S"] and u["U_SD"],
}

# Same tables, different mechanism for F (for the counterfactual comparison).
ALT_NOISE = {
    **{k: p for k, p in NOISE.items() if k not in ("U_OF", "U_F")},
    "A": Fr(31, 50),  # P(F | O)
    "B": Fr(1, 20),   # P(F | not O)
}
ALT_MECHANISMS = {**MECHANISMS, "F": lambda v, u: u["A"] if v["O"] else u["B"]}


class Model:
    def __init__(self, noise, mechanisms):
        self.noise = noise
        self.mechanisms = mechanisms

    def worlds(self):
        names = list(self.noise)
        for bits in product([False, True], repeat=len(names)):
            weight = Fr(1)
            for name, bit in zip(names, bits):
                weight *= self.noise[name] if bit else 1 - self.noise[name]
            yield dict(zip(names, bits)), weight

    def solve(self, u, do=None):
        do = do or {}
        values = {}
        for var in VARIABLES:
            values[var] = do[var] if var in do else bool(self.mechanisms[var](values, u))
        return values

    def prob(self, event, given=None, do=None):
        given = given or {}
        numerator = denominator = Fr(0)
        for u, weight in self.worlds():
            values = self.solve(u, do)
            if all(values[k] == x for k, x in given.items()):
                denominator += weight
                if all(values[k] == x for k, x in event.items()):
                    numerator += weight
        return numerator / denominator

    def counterfactual(self, event, evidence, do):
        # abduction, action, prediction
        numerator = denominator = Fr(0)
        for u, weight in self.worlds():
            actual = self.solve(u)
            if all(actual[k] == x for k, x in evidence.items()):
                denominator += weight
                alternative = self.solve(u, do)
                if all(alternative[k] == x for k, x in event.items()):
                    numerator += weight
        return numerator / denominator

    def cpt(self, var):
        table = {}
        for setting in product([False, True], repeat=len(PARENTS[var])):
            values = dict(zip(PARENTS[var], setting))
            table[setting] = sum(
                (w for u, w in self.worlds() if self.mechanisms[var](values, u)), Fr(0)
            )
        return table

    def factorised_prob(self, assignment, do=None):
        do = do or {}
        result = Fr(1)
        for var in VARIABLES:
            if var in do:
                result *= 1 if assignment[var] == do[var] else 0
            else:
                setting = tuple(assignment[p] for p in PARENTS[var])
                p = self.cpt(var)[setting]
                result *= p if assignment[var] else 1 - p
        return result


def label(setting):
    return "".join("T" if x else "F" for x in setting) or "-"


def main():
    model = Model(NOISE, MECHANISMS)
    alt = Model(ALT_NOISE, ALT_MECHANISMS)

    print("Conditional probability tables")
    for var in VARIABLES:
        rows = ", ".join(f"{label(s)}: {float(p):.4f}" for s, p in model.cpt(var).items())
        print(f"  P({var} | {','.join(PARENTS[var]) or '-'})  {rows}")

    interventions = [
        ("none", {}),
        ("do(O)", {"O": True}),
        ("do(not O)", {"O": False}),
        ("do(S)", {"S": True}),
        ("do(not S)", {"S": False}),
        ("do(M)", {"M": True}),
        ("do(not M)", {"M": False}),
        ("do(not F)", {"F": False}),
    ]
    print("\nMarginals after each intervention")
    print(f"  {'':10}" + "".join(f"{v:>9}" for v in VARIABLES))
    for name, do in interventions:
        row = "".join(f"{float(model.prob({v: True}, do=do)):9.4f}" for v in VARIABLES)
        print(f"  {name:10}{row}")

    print("\nSeeing versus doing")
    pairs = [
        ("P(S | O)", model.prob({"S": True}, {"O": True})),
        ("P(S | do(O))", model.prob({"S": True}, do={"O": True})),
        ("P(D | O)", model.prob({"D": True}, {"O": True})),
        ("P(D | do(O))", model.prob({"D": True}, do={"O": True})),
        ("P(O | not F)", model.prob({"O": True}, {"F": False})),
        ("P(O | do(not F))", model.prob({"O": True}, do={"F": False})),
        ("P(S | O, M)", model.prob({"S": True}, {"O": True, "M": True})),
        ("P(S | O, not M)", model.prob({"S": True}, {"O": True, "M": False})),
        ("P(S | do(O), M)", model.prob({"S": True}, {"M": True}, {"O": True})),
    ]
    for name, p in pairs:
        print(f"  {name:18}{float(p):.4f}")

    print("\nCounterfactuals")
    no_o, no_s = {"O": False}, {"S": False}
    rows = [
        ("F had there been no outage | O, F", model.counterfactual({"F": True}, {"O": True, "F": True}, no_o)),
        ("  same query, alternative model", alt.counterfactual({"F": True}, {"O": True, "F": True}, no_o)),
        ("O had there been no storm | S, O", model.counterfactual({"O": True}, {"S": True, "O": True}, no_s)),
        ("F had there been no storm | S, F", model.counterfactual({"F": True}, {"S": True, "F": True}, no_s)),
    ]
    for name, p in rows:
        print(f"  {name:36}{float(p):.4f}  ({p})")

    check(model, alt)
    print("\nAll values match.")


def check(model, alt):
    def eq(actual, expected):
        assert actual == Fr(expected), f"{actual} != {expected}"

    # Tables from Step 3.
    assert model.cpt("O") == {
        (False, False): Fr("0.1"),
        (False, True): Fr("0.46"),
        (True, False): Fr("0.55"),
        (True, True): Fr("0.73"),
    }
    assert model.cpt("F") == {(False,): Fr("0.05"), (True,): Fr("0.62")}
    assert model.cpt("D") == {(False,): Fr(0), (True,): Fr("0.7")}

    # tables give the same joint as the noise enumeration
    for do in ({}, {"O": True}, {"O": False}, {"S": True}, {"M": False}, {"F": False}):
        for values in product([False, True], repeat=len(VARIABLES)):
            assignment = dict(zip(VARIABLES, values))
            assert model.prob(assignment, do=do) == model.factorised_prob(assignment, do)

    # Marginals from Step 3.
    eq(model.prob({"O": True}), "0.2872")
    eq(model.prob({"F": True}), "0.213704")
    eq(model.prob({"D": True}), "0.14")

    # Interventions from Step 5.
    eq(model.prob({"F": True}, do={"O": True}), "0.62")
    eq(model.prob({"S": True}, do={"O": True}), "0.2")
    eq(model.prob({"D": True}, do={"O": True}), "0.14")
    eq(model.prob({"F": True}, do={"O": False}), "0.05")
    eq(model.prob({"O": True}, do={"S": True}), "0.604")
    eq(model.prob({"F": True}, do={"S": True}), "0.39428")
    eq(model.prob({"D": True}, do={"S": True}), "0.7")
    eq(model.prob({"O": True}, do={"S": False}), "0.208")
    eq(model.prob({"F": True}, do={"S": False}), "0.16856")
    eq(model.prob({"O": True}, do={"M": False}), "0.19")
    eq(model.prob({"F": True}, do={"M": False}), "0.1583")
    eq(model.prob({"O": True}, do={"F": False}), "0.2872")

    # Seeing versus doing.
    eq(model.prob({"S": True}, {"O": True}), Fr(1208, 2872))
    eq(model.prob({"D": True}, {"O": True}), Fr(7, 10) * Fr(1208, 2872))
    eq(model.prob({"O": True}, {"F": False}), Fr("0.109136") / Fr("0.786296"))
    eq(model.prob({"S": True}, {"O": True, "M": True}), Fr(438, 1542))
    eq(model.prob({"S": True}, {"O": True, "M": False}), Fr(77, 133))
    eq(model.prob({"S": True}, {"M": True}, {"O": True}), "0.2")

    # the two models should agree here
    for do in ({}, {"O": True}, {"O": False}, {"S": True}, {"S": False}):
        for values in product([False, True], repeat=len(VARIABLES)):
            assignment = dict(zip(VARIABLES, values))
            assert model.prob(assignment, do=do) == alt.prob(assignment, do=do)

    # Counterfactuals from Step 6.
    evidence = {"O": True, "F": True}
    eq(model.counterfactual({"F": True}, evidence, {"O": False}), Fr(5, 62))
    eq(alt.counterfactual({"F": True}, evidence, {"O": False}), Fr(1, 20))
    eq(model.counterfactual({"O": True}, {"S": True, "O": True}, {"S": False}), Fr("0.208") / Fr("0.604"))
    eq(model.counterfactual({"F": True}, {"S": True, "F": True}, {"S": False}), Fr("0.16856") / Fr("0.39428"))


if __name__ == "__main__":
    main()
