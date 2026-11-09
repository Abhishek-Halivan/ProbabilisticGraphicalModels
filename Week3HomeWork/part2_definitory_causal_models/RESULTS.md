# Experiment results

- Original reasoner: 84 of 113 queries matched.
- Patched reasoner: 113 of 113 queries matched.

| ID | Experiment | Query | Expected | Original | Match | Patched | Match |
|---|---|---|---|---|---|---|---|
| G0 | Baseline | `value(total_served(grid),_)` | 100 | `100.0` | yes | `100.0` | yes |
| G0 | Baseline | `value(spare(grid),_)` | 20 | `20.0` | yes | `20.0` | yes |
| G0 | Baseline | `energised(a)` | true | `true` | yes | `true` | yes |
| G0 | Baseline | `energised(b)` | true | `true` | yes | `true` | yes |
| G0 | Baseline | `energised(c)` | true | `true` | yes | `true` | yes |
| G0 | Baseline | `energised(d)` | true | `true` | yes | `true` | yes |
| G0 | Baseline | `energised(e)` | false | `false` | yes | `false` | yes |
| G1 | Open a-b: the ring reroutes power to b | `value(total_served(grid),_)` | 100 | `100.0` | yes | `100.0` | yes |
| G1 | Open a-b: the ring reroutes power to b | `value(spare(grid),_)` | 20 | `20.0` | yes | `20.0` | yes |
| G1 | Open a-b: the ring reroutes power to b | `energised(b)` | true | `true` | yes | `true` | yes |
| G2 | Open a-b and c-d: b and c go dark | `value(total_served(grid),_)` | 50 | `50.0` | yes | `50.0` | yes |
| G2 | Open a-b and c-d: b and c go dark | `value(spare(grid),_)` | 70 | `70.0` | yes | `70.0` | yes |
| G2 | Open a-b and c-d: b and c go dark | `energised(b)` | false | `false` | yes | `false` | yes |
| G2 | Open a-b and c-d: b and c go dark | `energised(c)` | false | `false` | yes | `false` | yes |
| G2 | Open a-b and c-d: b and c go dark | `energised(d)` | true | `true` | yes | `true` | yes |
| G3 | As G2, then start the generator at c | `value(total_served(grid),_)` | 100 | `100.0` | yes | `100.0` | yes |
| G3 | As G2, then start the generator at c | `value(spare(grid),_)` | 80 | `80.0` | yes | `80.0` | yes |
| G3 | As G2, then start the generator at c | `energised(b)` | true | `true` | yes | `true` | yes |
| G3 | As G2, then start the generator at c | `energised(c)` | true | `true` | yes | `true` | yes |
| G4 | Positive logic intervention on a recursive atom | `value(total_served(grid),_)` | 150 | `50.0` | no | `150.0` | yes |
| G4 | Positive logic intervention on a recursive atom | `value(spare(grid),_)` | -30 | `70.0` | no | `-30.0` | yes |
| G4 | Positive logic intervention on a recursive atom | `energised(a)` | true | `false` | no | `true` | yes |
| G4 | Positive logic intervention on a recursive atom | `energised(e)` | true | `true` | yes | `true` | yes |
| G5 | Negative logic intervention on a recursive atom | `value(total_served(grid),_)` | 80 | `0.0` | no | `80.0` | yes |
| G5 | Negative logic intervention on a recursive atom | `value(spare(grid),_)` | 40 | `120.0` | no | `40.0` | yes |
| G5 | Negative logic intervention on a recursive atom | `energised(a)` | true | `false` | no | `true` | yes |
| G5 | Negative logic intervention on a recursive atom | `energised(b)` | false | `false` | yes | `false` | yes |
| G5 | Negative logic intervention on a recursive atom | `energised(c)` | true | `false` | no | `true` | yes |
| G5 | Negative logic intervention on a recursive atom | `energised(d)` | true | `false` | no | `true` | yes |
| G6 | Set an intensional attribute in the middle | `value(total_served(grid),_)` | 85 | `85.0` | yes | `85.0` | yes |
| G6 | Set an intensional attribute in the middle | `value(spare(grid),_)` | 35 | `35.0` | yes | `35.0` | yes |
| G6 | Set an intensional attribute in the middle | `energised(b)` | true | `true` | yes | `true` | yes |
| G7 | Set an intensional leaf: upstream is unchanged | `value(total_served(grid),_)` | 100 | `100.0` | yes | `100.0` | yes |
| G7 | Set an intensional leaf: upstream is unchanged | `value(spare(grid),_)` | 1000 | `1000.0` | yes | `1000.0` | yes |
| G8 | Set an extensional attribute | `value(total_served(grid),_)` | 160 | `160.0` | yes | `160.0` | yes |
| G8 | Set an extensional attribute | `value(spare(grid),_)` | -40 | `-40.0` | yes | `-40.0` | yes |
| G9 | Zero capacity turns the logic off | `value(total_served(grid),_)` | 0 | `0.0` | yes | `0.0` | yes |
| G9 | Zero capacity turns the logic off | `value(spare(grid),_)` | 0 | `0.0` | yes | `0.0` | yes |
| G9 | Zero capacity turns the logic off | `energised(a)` | false | `false` | yes | `false` | yes |
| G9 | Zero capacity turns the logic off | `energised(b)` | false | `false` | yes | `false` | yes |
| G9 | Zero capacity turns the logic off | `energised(c)` | false | `false` | yes | `false` | yes |
| G9 | Zero capacity turns the logic off | `energised(d)` | false | `false` | yes | `false` | yes |
| G10 | Close one direction of the d-e breaker | `value(total_served(grid),_)` | 150 | `150.0` | yes | `150.0` | yes |
| G10 | Close one direction of the d-e breaker | `value(spare(grid),_)` | -30 | `-30.0` | yes | `-30.0` | yes |
| G10 | Close one direction of the d-e breaker | `energised(e)` | true | `true` | yes | `true` | yes |
| F0 | Baseline | `value(runoff(north),_)` | 80 | `error(error(existence_error(reset,call_info(ret,3204566793424)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `80.0` | yes |
| F0 | Baseline | `warned(north)` | true | `error(error(existence_error(reset,call_info(ret,3204566796160)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `true` | yes |
| F0 | Baseline | `warned(east)` | true | `error(error(existence_error(reset,call_info(ret,3204566796160)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `true` | yes |
| F0 | Baseline | `warned(south)` | false | `error(error(existence_error(reset,call_info(ret,3204566796160)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `false` | yes |
| F0 | Baseline | `value(total_cost(all),_)` | 160 | `error(error(existence_error(reset,call_info(ret,3204566793568)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `160.0` | yes |
| F1 | More rain in the south triggers an alert | `value(runoff(south),_)` | 80 | `error(error(existence_error(reset,call_info(ret,1714174226368)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `80.0` | yes |
| F1 | More rain in the south triggers an alert | `warned(south)` | true | `error(error(existence_error(reset,call_info(ret,1714174228384)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `true` | yes |
| F1 | More rain in the south triggers an alert | `value(total_cost(all),_)` | 200 | `error(error(existence_error(reset,call_info(ret,1714174226512)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `200.0` | yes |
| F2 | No alert: the radio cycle must not sustain itself | `warned(north)` | false | `error(error(existence_error(reset,call_info(ret,1267731219952)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `false` | yes |
| F2 | No alert: the radio cycle must not sustain itself | `warned(east)` | false | `error(error(existence_error(reset,call_info(ret,1267731225856)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `false` | yes |
| F2 | No alert: the radio cycle must not sustain itself | `value(total_cost(all),_)` | 0 | `error(error(existence_error(reset,call_info(ret,1267731218656)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `0.0` | yes |
| F3 | Set runoff directly | `alert(south)` | true | `error(error(existence_error(reset,call_info(ret,2529871442080)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `true` | yes |
| F3 | Set runoff directly | `value(total_cost(all),_)` | 200 | `error(error(existence_error(reset,call_info(ret,2529871439488)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `200.0` | yes |
| F4 | Force a warning without an alert | `alert(south)` | false | `false` | yes | `false` | yes |
| F4 | Force a warning without an alert | `warned(south)` | true | `true` | yes | `true` | yes |
| F4 | Force a warning without an alert | `value(total_cost(all),_)` | 200 | `40.0` | no | `200.0` | yes |
| F5 | Suppress a warning on the cycle | `warned(north)` | false | `false` | yes | `false` | yes |
| F5 | Suppress a warning on the cycle | `warned(east)` | false | `false` | yes | `false` | yes |
| F5 | Suppress a warning on the cycle | `value(total_cost(all),_)` | 0 | `0.0` | yes | `0.0` | yes |
| F6 | Cut one radio channel | `warned(north)` | true | `error(error(existence_error(reset,call_info(ret,2642514956928)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `true` | yes |
| F6 | Cut one radio channel | `warned(east)` | false | `error(error(existence_error(reset,call_info(ret,2642514956208)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `false` | yes |
| F6 | Cut one radio channel | `value(total_cost(all),_)` | 100 | `error(error(existence_error(reset,call_info(ret,2642514962256)),context(shift/1,'Cannot catch continuation through findall/3')))` | no | `100.0` | yes |
| C0 | Baseline | `value(birds(n),_)` | 50000 | `5.0e+04` | yes | `5.0e+04` | yes |
| C0 | Baseline | `value(birds(w),_)` | 0 | `0.0` | yes | `0.0` | yes |
| C0 | Baseline | `value(birds(m),_)` | 200000 | `2.0e+05` | yes | `2.0e+05` | yes |
| C0 | Baseline | `value(birds(e),_)` | 200000 | `2.0e+05` | yes | `2.0e+05` | yes |
| C0 | Baseline | `value(birds(s),_)` | 100000 | `1.0e+05` | yes | `1.0e+05` | yes |
| C1 | Remove the barrier in both directions | `value(birds(n),_)` | 250000 | `2.5e+05` | yes | `2.5e+05` | yes |
| C1 | Remove the barrier in both directions | `value(birds(w),_)` | 0 | `0.0` | yes | `0.0` | yes |
| C1 | Remove the barrier in both directions | `value(birds(m),_)` | 250000 | `2.5e+05` | yes | `2.5e+05` | yes |
| C1 | Remove the barrier in both directions | `value(birds(e),_)` | 250000 | `2.5e+05` | yes | `2.5e+05` | yes |
| C1 | Remove the barrier in both directions | `value(birds(s),_)` | 125000 | `125000.0` | yes | `125000.0` | yes |
| C2 | Remove the barrier in one direction | `value(birds(n),_)` | 250000 | `2.5e+05` | yes | `2.5e+05` | yes |
| C2 | Remove the barrier in one direction | `value(birds(w),_)` | 0 | `0.0` | yes | `0.0` | yes |
| C2 | Remove the barrier in one direction | `value(birds(m),_)` | 200000 | `2.0e+05` | yes | `2.0e+05` | yes |
| C2 | Remove the barrier in one direction | `value(birds(e),_)` | 200000 | `2.0e+05` | yes | `2.0e+05` | yes |
| C2 | Remove the barrier in one direction | `value(birds(s),_)` | 100000 | `1.0e+05` | yes | `1.0e+05` | yes |
| C3 | Remove the trees from the hub | `value(birds(n),_)` | 50000 | `5.0e+04` | yes | `5.0e+04` | yes |
| C3 | Remove the trees from the hub | `value(birds(w),_)` | 0 | `0.0` | yes | `0.0` | yes |
| C3 | Remove the trees from the hub | `value(birds(m),_)` | 0 | `0.0` | yes | `0.0` | yes |
| C3 | Remove the trees from the hub | `value(birds(e),_)` | 50000 | `5.0e+04` | yes | `5.0e+04` | yes |
| C3 | Remove the trees from the hub | `value(birds(s),_)` | 50000 | `5.0e+04` | yes | `5.0e+04` | yes |
| C4 | Plant trees in w | `value(birds(n),_)` | 50000 | `5.0e+04` | yes | `5.0e+04` | yes |
| C4 | Plant trees in w | `value(birds(w),_)` | 125000 | `125000.0` | yes | `125000.0` | yes |
| C4 | Plant trees in w | `value(birds(m),_)` | 250000 | `2.5e+05` | yes | `2.5e+05` | yes |
| C4 | Plant trees in w | `value(birds(e),_)` | 250000 | `2.5e+05` | yes | `2.5e+05` | yes |
| C4 | Plant trees in w | `value(birds(s),_)` | 125000 | `125000.0` | yes | `125000.0` | yes |
| C5 | Set an intensional attribute | `value(birds(n),_)` | 50000 | `5.0e+04` | yes | `5.0e+04` | yes |
| C5 | Set an intensional attribute | `value(birds(w),_)` | 0 | `0.0` | yes | `0.0` | yes |
| C5 | Set an intensional attribute | `value(birds(m),_)` | 7 | `7.0` | yes | `7.0` | yes |
| C5 | Set an intensional attribute | `value(birds(e),_)` | 200000 | `2.0e+05` | yes | `2.0e+05` | yes |
| C5 | Set an intensional attribute | `value(birds(s),_)` | 100000 | `1.0e+05` | yes | `1.0e+05` | yes |
| C6 | Force a recursive connected/2 atom | `value(birds(n),_)` | 250000 | `2.0e+05` | no | `2.5e+05` | yes |
| C6 | Force a recursive connected/2 atom | `value(birds(w),_)` | 0 | `0.0` | yes | `0.0` | yes |
| C6 | Force a recursive connected/2 atom | `value(birds(m),_)` | 200000 | `0.0` | no | `2.0e+05` | yes |
| C6 | Force a recursive connected/2 atom | `value(birds(e),_)` | 200000 | `0.0` | no | `2.0e+05` | yes |
| C6 | Force a recursive connected/2 atom | `value(birds(s),_)` | 100000 | `0.0` | no | `1.0e+05` | yes |
| Y0 | Numerically cyclic: only the zero solution | `value(birds(m),_)` | 0 | `0.0` | yes | `0.0` | yes |
| Y0 | Numerically cyclic: only the zero solution | `value(trees(m),_)` | 0 | `0.0` | yes | `0.0` | yes |
| Y1 | Numerically cyclic: fix birds(m) | `value(birds(m),_)` | 10000 | `1.0e+04` | yes | `1.0e+04` | yes |
| Y1 | Numerically cyclic: fix birds(m) | `value(trees(m),_)` | -0.952382 | `-0.952381859412981` | yes | `-0.9523818594236563` | yes |
| Y1 | Numerically cyclic: fix birds(m) | `value(birds(n),_)` | -476.191 | `-476.19092970760033` | yes | `-476.19092968798213` | yes |
| E0 | Baseline | `value(demand(stationery),_)` | 8000 | `8000.0` | yes | `8000.0` | yes |
| E0 | Baseline | `value(demand(computers),_)` | 2100 | `2100.0` | yes | `2100.0` | yes |
| E1 | Add a purchasing directive | `value(demand(computers),_)` | 2700 | `2700.0` | yes | `2700.0` | yes |
| E2 | Remove a purchasing directive | `value(demand(stationery),_)` | 5000 | `5000.0` | yes | `5000.0` | yes |
| E3 | Set a purchase directly | `value(demand(stationery),_)` | 8042 | `8042.0` | yes | `8042.0` | yes |
| E4 | Set base demand | `value(demand(computers),_)` | 1000 | `1000.0` | yes | `1000.0` | yes |
