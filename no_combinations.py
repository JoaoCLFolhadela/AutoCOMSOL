import numpy as np
from itertools import combinations


# This class is taking the number of active PVDF points and checking which combinations exist with all_combinations
# It will will then update the current combination it is on when update_active_points is called
class solving:

    def __init__(self, no_active_points: int) -> None:
        self.no_active_points = no_active_points
        self.current_combination_index = -1
        self.all_combinations = []
        self.current_combination = ()
        self.parameters = {
            'active_1': '0', 'active_2': '0', 'active_3': '0',
            'active_4': '0', 'active_5': '0', 'active_6': '0',
            'active_7': '0', 'active_8': '0', 'active_9': '0'
        }

        # Get all combinations for given number of active points
        for c in combinations([1, 2, 3, 4, 5, 6, 7, 8, 9], no_active_points):
            self.all_combinations.append(c)

    def update_active_points(self, n = 0):
        self.parameters  = self.parameters.fromkeys(self.parameters, 0) # reset all parameters to 0

        if self.current_combination_index < len(self.all_combinations):
            if n == 0:
                self.current_combination_index += 1
            else:
                self.current_combination_index += n

        self.current_combination = self.all_combinations[self.current_combination_index]

        for point in self.current_combination:
            self.parameters[f'active_{point}'] = '1'
    
    def reset_index(self):
        self.parameters  = self.parameters.fromkeys(self.parameters, 0) # reset all parameters to 0
        self.current_combination_index = 0
        self.current_combination = self.all_combinations[0]
