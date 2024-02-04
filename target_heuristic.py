import domination_heuristics


def find_target_difficulty(players: list, targets: list):
    skills_total = domination_heuristics.find_skills_total(players, domination_heuristics.skill_list(players))
    target_diff = {}
    for target in targets:
        diff = 0
        for skill in target.skills.keys():
            if skills_total.get(skill, 0) == 0:
                diff += 100000
            else:
                diff += (target.skills[skill] / skills_total[skill]) / target.payoff
        target_diff[target.name] = diff
    target_diff = {k: v for k, v in sorted(target_diff.items(), key=lambda item: item[1], reverse=False)}
    return [key for key in target_diff.keys()]
