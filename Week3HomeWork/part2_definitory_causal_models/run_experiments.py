# Runs all the experiments on both reasoners and writes RESULTS.md

import subprocess
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENDOR = "vendor/definitory_causal_models"
REASONERS = {"Original": f"{VENDOR}/causal_reasoner", "Patched": "patched/causal_reasoner"}
TIMEOUT_SECONDS = 30
TOLERANCE = 1e-6
GRID = "models/power_grid.pl"
FLOOD = "models/flood_watch.pl"
CONSERVATION = f"{VENDOR}/conservation.pl"
CYCLIC = f"{VENDOR}/conservation_cyclic.pl"
ECONOMY = f"{VENDOR}/economy.pl"
GRID_TABLES = ["energised/1"]
FLOOD_TABLES = ["warned/1"]
CONSERVATION_TABLES = ["connected/2"]

OPEN_AB = [("breaker_open(a,b)", "true"), ("breaker_open(b,a)", "true")]
OPEN_CD = [("breaker_open(c,d)", "true"), ("breaker_open(d,c)", "true")]


def val(attribute):
    return f"value({attribute},_)"


def grid(total, spare, **energised):
    expected = {val("total_served(grid)"): total, val("spare(grid)"): spare}
    expected.update({f"energised({k})": v for k, v in energised.items()})
    return expected


def birds(n, w, m, e, s):
    return {val(f"birds({k})"): v for k, v in zip("nwmes", (n, w, m, e, s))}


# Cyclic example after do(birds(m),10000): trees(X) = size(X)*T with T the sum
# of all birds, which gives T = 10000 + 1050000*T.
T = -10000 / 1049999


@dataclass
class Experiment:
    id: str
    title: str
    model: str
    tables: list
    interventions: list
    expected: dict


EXPERIMENTS = [
    # power grid
    Experiment("G0", "Baseline", GRID, GRID_TABLES, [],
               grid(100, 20, a=True, b=True, c=True, d=True, e=False)),
    Experiment("G1", "Open a-b: the ring reroutes power to b", GRID, GRID_TABLES, OPEN_AB,
               grid(100, 20, b=True)),
    Experiment("G2", "Open a-b and c-d: b and c go dark", GRID, GRID_TABLES, OPEN_AB + OPEN_CD,
               grid(50, 70, b=False, c=False, d=True)),
    Experiment("G3", "As G2, then start the generator at c", GRID, GRID_TABLES,
               OPEN_AB + OPEN_CD + [("capacity(c)", "60")], grid(100, 80, b=True, c=True)),
    Experiment("G4", "Positive logic intervention on a recursive atom", GRID, GRID_TABLES,
               [("energised(e)", "true")], grid(150, -30, a=True, e=True)),
    Experiment("G5", "Negative logic intervention on a recursive atom", GRID, GRID_TABLES,
               [("energised(b)", "false")], grid(80, 40, a=True, b=False, c=True, d=True)),
    Experiment("G6", "Set an intensional attribute in the middle", GRID, GRID_TABLES,
               [("served(b)", "5")], grid(85, 35, b=True)),
    Experiment("G7", "Set an intensional leaf: upstream is unchanged", GRID, GRID_TABLES,
               [("spare(grid)", "1000")], grid(100, 1000)),
    Experiment("G8", "Set an extensional attribute", GRID, GRID_TABLES,
               [("demand(d)", "100")], grid(160, -40)),
    Experiment("G9", "Zero capacity turns the logic off", GRID, GRID_TABLES,
               [("capacity(a)", "0")], grid(0, 0, a=False, b=False, c=False, d=False)),
    Experiment("G10", "Close one direction of the d-e breaker", GRID, GRID_TABLES,
               [("breaker_open(d,e)", "false")], grid(150, -30, e=True)),

    # flood model
    Experiment("F0", "Baseline", FLOOD, FLOOD_TABLES, [],
               {val("runoff(north)"): 80, "warned(north)": True, "warned(east)": True,
                "warned(south)": False, val("total_cost(all)"): 160}),
    Experiment("F1", "More rain in the south triggers an alert", FLOOD, FLOOD_TABLES,
               [("rainfall(south)", "20")],
               {val("runoff(south)"): 80, "warned(south)": True, val("total_cost(all)"): 200}),
    Experiment("F2", "No alert: the radio cycle must not sustain itself", FLOOD, FLOOD_TABLES,
               [("rainfall(north)", "1")],
               {"warned(north)": False, "warned(east)": False, val("total_cost(all)"): 0}),
    Experiment("F3", "Set runoff directly", FLOOD, FLOOD_TABLES, [("runoff(south)", "99")],
               {"alert(south)": True, val("total_cost(all)"): 200}),
    Experiment("F4", "Force a warning without an alert", FLOOD, FLOOD_TABLES,
               [("warned(south)", "true")],
               {"alert(south)": False, "warned(south)": True, val("total_cost(all)"): 200}),
    Experiment("F5", "Suppress a warning on the cycle", FLOOD, FLOOD_TABLES,
               [("warned(north)", "false")],
               {"warned(north)": False, "warned(east)": False, val("total_cost(all)"): 0}),
    Experiment("F6", "Cut one radio channel", FLOOD, FLOOD_TABLES,
               [("channel(north,east)", "false")],
               {"warned(north)": True, "warned(east)": False, val("total_cost(all)"): 100}),

    # examples from the repo
    Experiment("C0", "Baseline", CONSERVATION, CONSERVATION_TABLES, [],
               birds(50000, 0, 200000, 200000, 100000)),
    Experiment("C1", "Remove the barrier in both directions", CONSERVATION, CONSERVATION_TABLES,
               [("barrier(n,m)", "false"), ("barrier(m,n)", "false")],
               birds(250000, 0, 250000, 250000, 125000)),
    Experiment("C2", "Remove the barrier in one direction", CONSERVATION, CONSERVATION_TABLES,
               [("barrier(n,m)", "false")], birds(250000, 0, 200000, 200000, 100000)),
    Experiment("C3", "Remove the trees from the hub", CONSERVATION, CONSERVATION_TABLES,
               [("trees(m)", "0")], birds(50000, 0, 0, 50000, 50000)),
    Experiment("C4", "Plant trees in w", CONSERVATION, CONSERVATION_TABLES,
               [("trees(w)", "50")], birds(50000, 125000, 250000, 250000, 125000)),
    Experiment("C5", "Set an intensional attribute", CONSERVATION, CONSERVATION_TABLES,
               [("birds(m)", "7")], birds(50000, 0, 7, 200000, 100000)),
    Experiment("C6", "Force a recursive connected/2 atom", CONSERVATION, CONSERVATION_TABLES,
               [("connected(n,e)", "true")], birds(250000, 0, 200000, 200000, 100000)),
    Experiment("Y0", "Numerically cyclic: only the zero solution", CYCLIC, CONSERVATION_TABLES, [],
               {val("birds(m)"): 0, val("trees(m)"): 0}),
    Experiment("Y1", "Numerically cyclic: fix birds(m)", CYCLIC, CONSERVATION_TABLES,
               [("birds(m)", "10000")],
               {val("birds(m)"): 10000, val("trees(m)"): 100 * T, val("birds(n)"): 50000 * T}),
    Experiment("E0", "Baseline", ECONOMY, [], [],
               {val("demand(stationery)"): 8000, val("demand(computers)"): 2100}),
    Experiment("E1", "Add a purchasing directive", ECONOMY, [],
               [("directive(interior,computers)", "true")], {val("demand(computers)"): 2700}),
    Experiment("E2", "Remove a purchasing directive", ECONOMY, [],
               [("directive(finance,stationery)", "false")], {val("demand(stationery)"): 5000}),
    Experiment("E3", "Set a purchase directly", ECONOMY, [],
               [("purchase(exterior,stationery)", "42")], {val("demand(stationery)"): 8042}),
    Experiment("E4", "Set base demand", ECONOMY, [],
               [("base_demand(computers)", "0")], {val("demand(computers)"): 1000}),
]


def prolog_goal(reasoner, experiment, queries):
    tables = ",".join(experiment.tables)
    interventions = ",".join(f"{x}-{v}" for x, v in experiment.interventions)
    return (f"run_experiment('{reasoner}','{experiment.model}',[{tables}],"
            f"[{interventions}],[{','.join(queries)}])")


def run(reasoner, experiment):
    queries = list(experiment.expected)
    command = ["swipl", "-q", "-g", prolog_goal(reasoner, experiment, queries),
               "-t", "halt", "harness.pl"]
    try:
        done = subprocess.run(command, cwd=HERE, capture_output=True, text=True,
                              timeout=TIMEOUT_SECONDS)
        output, fallback = done.stdout, f"crashed (exit {done.returncode})"
    except subprocess.TimeoutExpired as err:
        output = err.stdout.decode() if err.stdout else ""
        fallback = f"timed out after {TIMEOUT_SECONDS}s"

    answers = {query: fallback for query in queries}
    for line in output.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3 and parts[0] == "RESULT":
            answers[queries[int(parts[1]) - 1]] = parts[2]
    return answers


def matches(expected, raw):
    if isinstance(expected, bool):
        return raw == str(expected).lower()
    try:
        return abs(float(raw) - expected) <= TOLERANCE * max(1, abs(expected))
    except ValueError:
        return False


def main():
    answers = {name: {e.id: run(path, e) for e in EXPERIMENTS} for name, path in REASONERS.items()}
    passed = dict.fromkeys(REASONERS, 0)
    total = sum(len(e.expected) for e in EXPERIMENTS)

    rows = ["| ID | Experiment | Query | Expected | Original | Match | Patched | Match |",
            "|---|---|---|---|---|---|---|---|"]
    for e in EXPERIMENTS:
        for query, expected in e.expected.items():
            shown = str(expected).lower() if isinstance(expected, bool) else f"{expected:g}"
            row = f"| {e.id} | {e.title} | `{query}` | {shown} |"
            for name in REASONERS:
                raw = answers[name][e.id][query]
                ok = matches(expected, raw)
                passed[name] += ok
                cell = raw.replace("|", "\\|")
                row += f" `{cell}` | {'yes' if ok else 'no'} |"
                if not ok:
                    print(f"{name} {e.id} {query}: expected {shown}, got {raw}")
            rows.append(row)

    summary = [f"- {name} reasoner: {passed[name]} of {total} queries matched." for name in REASONERS]
    lines = ["# Experiment results", "", *summary, "", *rows]
    (HERE / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
