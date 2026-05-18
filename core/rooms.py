rooms = {}
def create_room(chat_id):

    rooms[chat_id] = {

        "started": False,

        "masters": [],
        "players": [],

        "master_turn": 0,

        "active_mission": None,

        "mission_lock": False
    }