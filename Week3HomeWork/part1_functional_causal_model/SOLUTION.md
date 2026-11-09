# Exercise 1: Functional causal model to Bayesian network

[fcm.py](fcm.py) checks the calculations below with exact fractions (run `python fcm.py`).

## 1. Causal diagram

I went with a household during a possible power cut:

| Symbol | Proposition |
|---|---|
| S | There is a storm |
| M | Grid maintenance is overdue |
| O | There is a power outage |
| F | The food in the freezer spoils |
| D | The commute is disrupted |

```text
   S       M
  / \     /
 v   \   /
 D    v v
       O        (collider: S -> O <- M)
       |
       v
       F
```

So the edges are S->D, S->O, M->O and O->F. O is the collider, since both the storm and the maintenance point into it.

## 2. Markovian functional causal model

Every variable is a function of its parents and its own noise terms. The noise variables are all independent of each other, so the model is Markovian.

```text
S := U_S
M := U_M
O := (S and U_SO) or (M and U_MO) or U_O
F := (O and U_OF) or U_F
D := S and U_SD
```

| Noise | Meaning | P(true) |
|---|---|---|
| U_S | A storm happens | 0.2 |
| U_M | Maintenance is overdue | 0.3 |
| U_SO | The storm is strong enough to cut the power | 0.5 |
| U_MO | The neglected equipment fails | 0.4 |
| U_O | The power fails for some other reason | 0.1 |
| U_OF | The outage lasts long enough to spoil the food | 0.6 |
| U_F | The food spoils for some other reason | 0.05 |
| U_SD | The storm blocks the commute | 0.7 |

## 3. The Bayesian network

For each setting of the parents, I need the probability that the noise makes the equation true. A disjunction is only false if all of its parts fail, so it is easiest to multiply the failure probabilities and subtract from 1.

Root nodes: P(S) = 0.2 and P(M) = 0.3.

P(O | S, M) = 1 - (1 - 0.5·s)(1 - 0.4·m)(1 - 0.1)

| S | M | Calculation | P(O \| S, M) |
|---|---|---|---|
| F | F | 1 - 0.9 | 0.10 |
| F | T | 1 - 0.6·0.9 | 0.46 |
| T | F | 1 - 0.5·0.9 | 0.55 |
| T | T | 1 - 0.5·0.6·0.9 | 0.73 |

P(F | O):

| O | Calculation | P(F \| O) |
|---|---|---|
| F | only U_F can make it true | 0.05 |
| T | 1 - 0.4·0.95 | 0.62 |

P(D | S):

| S | Calculation | P(D \| S) |
|---|---|---|
| F | equation is false | 0 |
| T | U_SD | 0.7 |

The joint is P(S)·P(M)·P(O|S,M)·P(F|O)·P(D|S). The script confirms that this equals the distribution you get by enumerating the noise, for all 32 assignments.

Marginals:

```text
P(O) = 0.56·0.10 + 0.24·0.46 + 0.14·0.55 + 0.06·0.73 = 0.2872
P(F) = 0.2872·0.62 + 0.7128·0.05                      = 0.213704
P(D) = 0.2·0.7                                        = 0.14
```

## 4. What I noticed about the probabilities

The first thing is that the tables are monotone. My equations only use `and` and `or`, so adding a cause can never lower a probability. To get a parent that lowers the probability I would need a negation in the equation.

The table for O also has fewer degrees of freedom than it looks like. Its four entries come from just three noise probabilities, and they satisfy P(¬O|S,M)·P(¬O|¬S,¬M) = P(¬O|S,¬M)·P(¬O|¬S,M), because 0.27·0.90 = 0.45·0.54 = 0.243. A general table wouldn't have to do that. This is the noisy-or pattern, where k parents need about k + 1 numbers instead of 2^k.

The causes don't simply add up, though. The storm adds 0.45 to the outage probability if maintenance is fine, but only 0.27 if maintenance is overdue, since the outage is already more likely in that case.

Zeros come up easily too. P(D | ¬S) = 0 just because I didn't model any other cause of D. The "leak" noise terms like U_O and U_F are what keep entries away from zero, and with no noise at all every entry would be 0 or 1. The entries also tend to be short products of the same few numbers.

A conjunction would behave differently. It gives zero in every row where a required parent is false, so those rows are all the same (context-specific independence).

Finally, the tables lose information about the mechanism, since different equations can give identical tables. Section 6 has an example.

## 5. Interventions

An intervention replaces the equation of one variable. In the network, that means cutting the edges into that node and leaving the other tables as they are.

| Intervention | Type | P(S) | P(M) | P(O) | P(F) | P(D) |
|---|---|---|---|---|---|---|
| None | | 0.2 | 0.3 | 0.2872 | 0.2137 | 0.14 |
| do(O) | Positive, non-root, non-leaf | 0.2 | 0.3 | 1 | 0.62 | 0.14 |
| do(¬O) | Negative, non-root, non-leaf | 0.2 | 0.3 | 0 | 0.05 | 0.14 |
| do(S) | Positive, root | 1 | 0.3 | 0.604 | 0.3943 | 0.7 |
| do(¬S) | Negative, root | 0 | 0.3 | 0.208 | 0.1686 | 0 |
| do(M) | Positive, root | 0.2 | 1 | 0.514 | 0.3430 | 0.14 |
| do(¬M) | Negative, root | 0.2 | 0 | 0.19 | 0.1583 | 0.14 |
| do(¬F) | Negative, non-root, leaf | 0.2 | 0.3 | 0.2872 | 0 | 0.14 |

Some of the calculations:

```text
do(O):     P(F) = P(F | O) = 0.62   (S and D don't change, they aren't downstream of O)
do(not O): P(F) = P(F | not O) = 0.05
do(S):     P(O) = 0.3·0.73 + 0.7·0.55 = 0.604
           P(F) = 0.604·0.62 + 0.396·0.05 = 0.39428
do(not S): P(O) = 0.3·0.46 + 0.7·0.10 = 0.208
           P(F) = 0.208·0.62 + 0.792·0.05 = 0.16856
do(not M): P(O) = 0.2·0.55 + 0.8·0.10 = 0.19
           P(F) = 0.19·0.62 + 0.81·0.05 = 0.1583
```

Observing and intervening give different answers:

| Observing | Value | Intervening | Value | Reason |
|---|---|---|---|---|
| P(S \| O) | 0.4206 | P(S \| do(O)) | 0.2 | If I see an outage, a storm is more likely. If I cause the outage myself, it tells me nothing about the weather. |
| P(D \| O) | 0.2944 | P(D \| do(O)) | 0.14 | Seeing O tells me something about D through S. |
| P(O \| ¬F) | 0.1388 | P(O \| do(¬F)) | 0.2872 | Throwing the food away says nothing about the power. |

The collider is the interesting case. S and M are independent until O is observed, and then they start competing to explain it:

```text
P(S | O, not M) = 0.077 / 0.133   = 0.5789
P(S | O, M)     = 0.0438 / 0.1542 = 0.2840
P(S | do(O), M) = 0.2
```

So once I know there was an outage, finding out that maintenance was overdue makes a storm less likely (explaining away). This doesn't happen with do(O), because the intervention removes the edges into O.

## 6. Counterfactuals

I used the usual three steps: abduction, action, prediction.

### Would the food have spoiled without the outage?

I observed O and F, and I want the probability of F if there had been no outage.

1. Abduction: given O, the equation is F = U_OF or U_F. So P(F | O) = 0.62. Since U_F implies F, P(U_F | O, F) = 0.05 / 0.62 = 5/62.
2. Action: set O to false, which leaves F = U_F.
3. Prediction: the food would still have spoiled with probability 5/62 ≈ 0.0806.

That means the outage was necessary for the spoiling with probability 57/62 ≈ 0.919.

Note that this is higher than P(F | do(¬O)) = 0.05. Seeing the food spoil makes the other cause U_F more likely, and that carries over into the counterfactual world.

### Same tables, different answer

Suppose instead F := A if O else B, with A and B independent, P(A) = 0.62 and P(B) = 0.05. The tables are the same, and so are the interventions I checked. But now seeing O and F tells me nothing about B, so the counterfactual is 0.05 rather than 0.0806.

So the Bayesian network alone doesn't determine counterfactuals. You need the functional model.

### Two more

Nothing is negated in my model, so removing a cause can't make an effect true. If the effect would happen without the cause, it also happens with it. That gives a shortcut for these queries:

```text
P(B had there been no A | A, B) = P(B | not A) / P(B | A)
```

| Evidence | Query | Calculation | Counterfactual | do(¬A) value |
|---|---|---|---|---|
| S, O | O had there been no storm | 0.208 / 0.604 | 52/151 ≈ 0.3444 | 0.208 |
| S, F | F had there been no storm | 0.16856 / 0.39428 | 4214/9857 ≈ 0.4275 | 0.1686 |

I can read P(B | ¬A) and P(B | A) off the interventions here because S is a root. The script doesn't use the shortcut, it enumerates the noise, and it gets the same values.
