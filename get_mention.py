REACTION_NAME = '興味アリ'


def mention_user_list(msg):
    if not ('reactions' in msg.keys()): return []
    users = []
    for reaction in msg['reactions']:
        if reaction['name'] != REACTION_NAME: continue
        for user in reaction['users']:
            users.append(user)
        return users
    return users
