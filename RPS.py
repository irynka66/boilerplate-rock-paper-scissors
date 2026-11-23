def player(prev_play, opponent_history=[], my_history=[], state={}):
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    if prev_play == "":
        opponent_history.clear()
        my_history.clear()
        state.clear()
        state["opp_patterns"] = {}
        state["my_pairs"] = {
            "RR": 0, "RP": 0, "RS": 0,
            "PR": 0, "PP": 0, "PS": 0,
            "SR": 0, "SP": 0, "SS": 0,
        }
        state["scores"] = [0.0, 0.0, 0.0, 0.0]
        state["last_preds"] = ["R", "R", "R", "R"]

        first_move = "R"
        my_history.append(first_move)
        return first_move

    opponent_history.append(prev_play)

    for i, pred_opp in enumerate(state["last_preds"]):
        hypothetical_move = ideal_response[pred_opp]
        if hypothetical_move == ideal_response[prev_play]:
            reward = 1.0
        elif hypothetical_move == prev_play:
            reward = 0.0
        else:
            reward = -1.0
        state["scores"][i] = state["scores"][i] * 0.9 + reward

    if len(opponent_history) >= 5:
        pattern = "".join(opponent_history[-5:])
        state["opp_patterns"][pattern] = state["opp_patterns"].get(pattern, 0) + 1

    if len(my_history) == 1:
        pair = "R" + my_history[-1]
    else:
        pair = my_history[-2] + my_history[-1]
    state["my_pairs"][pair] += 1

    if len(opponent_history) >= 4:
        last_four = "".join(opponent_history[-4:])
        candidates = [last_four + "R", last_four + "P", last_four + "S"]
        pred_0 = max(candidates, key=lambda k: state["opp_patterns"].get(k, 0))[-1]
    else:
        pred_0 = "R"

    my_last = my_history[-1]
    pred_1 = ideal_response[my_last]

    last_ten = my_history[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)
    pred_2 = ideal_response[most_frequent]

    potential_pairs = [my_last + "R", my_last + "P", my_last + "S"]
    predicted_my_next = max(potential_pairs, key=lambda k: state["my_pairs"][k])[-1]
    pred_3 = ideal_response[predicted_my_next]

    preds = [pred_0, pred_1, pred_2, pred_3]
    state["last_preds"] = preds

    best_idx = state["scores"].index(max(state["scores"]))
    my_move = ideal_response[preds[best_idx]]

    my_history.append(my_move)
    return my_move