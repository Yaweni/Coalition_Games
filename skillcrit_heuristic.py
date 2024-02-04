import domination_heuristics
def identify_skill_rarity(targets:list):
    '''

    :param targets: A list of possible targets
    :return: A sorted dictionary ranking skills by their criticality
    '''
    skill_crit = {}
    for target in targets:
        temp = target.skills
        for skill in temp.keys():
            skill_crit[skill] = skill_crit.get(skill,0) + (target.payoff/temp[skill])

    skill_crit = {k: v for k, v in sorted(skill_crit.items(), key=lambda item: item[1], reverse=True)}
    return skill_crit

def players_skill_critical(players: list, targets : list):
    skills_total= domination_heuristics.find_skills_total(players,domination_heuristics.skill_list(players))
    skill_crit = identify_skill_rarity(targets)
    players_crit = {}
    for player in players:
        crit_val = 0
        skills = player.skills
        for skill in skills.keys():
            crit_val += (skills[skill]/skills_total[skill])*skill_crit.get(skill,0)
        players_crit[player.unique_id] = crit_val
    players_crit = {k: v for k, v in sorted(players_crit.items(), key=lambda item: item[1], reverse=True)}
    return [key for key in players_crit.keys()]



