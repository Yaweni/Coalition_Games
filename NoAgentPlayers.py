import numpy as np

class NoAgentPlayer():
    def __init__(self, unique_id : int, skills : dict, preferences :dict, neighbors : list):
        self.check_types(unique_id,skills,preferences,neighbors)
        self.unique_id = unique_id
        self.skills = skills
        self.preferences = preferences
        self.neighbors = neighbors

    def check_types(self, unique_id : int, skills : dict, preferences :dict, neighbors : list):
        if not isinstance(unique_id, int) or not isinstance(skills, dict) \
                 or not isinstance(preferences, dict) or not isinstance(neighbors, list) :
              raise TypeError("The unique id must be an integer, skills and preferences dictionaries and the neighbors a list")
        return None
