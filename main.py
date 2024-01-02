import itertools
from Player import Player
from modelCoal import Networkmodel
from Target import Target
from NoAgentPlayers import NoAgentPlayer



if __name__ == "__main__":

    # Example usage
    # Define players, targets, and their attributes
    player1 = NoAgentPlayer(1, {'skill1':2, 'skill2':3}, {'target1': 0.7, 'target2': 0.3}, [2])
    player2 = NoAgentPlayer(2, {'skill2':4, 'skill3':1}, {'target1': 0.4, 'target2': 0.6}, [1, 3])
    player3 = NoAgentPlayer(3, {'skill1':2, 'skill3':2}, {'target1': 0.5, 'target2': 0.5}, [2])

    players = [player1, player2, player3]

    target1 = Target('Target 1',{'skill1':3, 'skill2':2}, 10)
    target2 = Target('Target 2',{'skill2':1, 'skill3':4}, 15)


    targets = [target1, target2]

