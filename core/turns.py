def get_current_master(room):

    return room["masters"][
        room["master_turn"]
    ]
def next_master(room):

    room["master_turn"] += 1

    if room["master_turn"] >= len(room["masters"]):
        room["master_turn"] = 0