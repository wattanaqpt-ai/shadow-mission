rooms = {}

def create_room(chat_id):
    rooms[chat_id] = {
        "started": False,
        "masters": [],
        "slaves": [],
        "master_turn": 0,
        "active_mission": None,
        "mission_lock": False,
        "scores": {},
        "endgame_votes": {"yes": [], "no": []},
        "message_ids": []
    }
