def create_mission(text, master_id):

    return {

        "text": text,

        "master_id": master_id,

        "claimed": False,

        "claimed_by": None,

        "media_message_id": None,

        "votes": {
            "pass": 0,
            "fail": 0,
            "funny": 0
        }
    }