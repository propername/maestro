import copy

from maestro.simulations import env


class RubiksCube(env.Environment):
    ''' simulates a Rubiks Cube with a 20 cube representaiton '''

    def __init__(self):
        self.name = '3x3 Rubiks Cube'
        self.state = {
            1: 'top', 2: 'top', 3: 'top', 4: 'top',
            5: 'top', 6: 'top', 7: 'top', 8: 'top',
            9: 'left',
            10: 'front', 11: 'front', 12: 'front',
            13: 'right', 14: 'right', 15: 'right',
            16: 'back', 17: 'back', 18: 'back',
            19: 'left', 20: 'left', 21: 'left',
            22: 'front', 23: 'front',
            24: 'right', 25: 'right',
            26: 'back', 27: 'back',
            28: 'left', 29: 'left',
            30: 'front', 31: 'front', 32: 'front',
            33: 'right', 34: 'right', 35: 'right',
            36: 'back', 37: 'back', 38: 'back',
            39: 'left', 40: 'left',
            41: 'under', 42: 'under', 43: 'under', 44: 'under',
            45: 'under', 46: 'under', 47: 'under', 48: 'under'}
        self.original_state = copy.deepcopy(self.state)
        self.actions = [
            {0: 'top'}, {0: 'under'},
            {0: 'right'}, {0: 'left'},
            {0: 'front'}, {0: 'back'}, ]
        self.do_right = {
            3: 16, 16: 45, 45: 32, 32: 3,
            4: 26, 26: 44, 44: 23, 23: 4,
            5: 36, 36: 43, 43: 12, 12: 5,
            14: 25, 25: 34, 34: 24, 24: 14,
            35: 33, 33: 13, 13: 15, 15: 35, }
        self.do_left = {
            7: 10, 10: 41, 41: 38, 38: 7,
            8: 22, 22: 48, 48: 27, 27: 8,
            1: 30, 30: 47, 47: 18, 18: 1,
            19: 9, 9: 29, 29: 39, 39: 19,
            20: 21, 21: 40, 40: 28, 28: 20, }
        self.do_top = {
            9: 12, 12: 15, 15: 18, 18: 9,
            10: 13, 13: 16, 16: 19, 19: 10,
            11: 14, 14: 17, 17: 20, 20: 11,
            1: 3, 3: 5, 5: 7, 7: 1,
            2: 4, 4: 6, 6: 8, 8: 2, }
        self.do_under = {
            30: 33, 33: 36, 36: 39, 39: 30,
            31: 34, 34: 37, 37: 40, 40: 31,
            32: 35, 35: 38, 38: 29, 29: 32,
            41: 43, 43: 45, 45: 47, 47: 41,
            42: 44, 44: 46, 46: 48, 48: 42, }
        self.do_front = {
            1: 13, 13: 43, 43: 29, 29: 1,
            2: 24, 24: 42, 42: 21, 21: 2,
            3: 33, 33: 41, 41: 9, 9: 3,
            10: 12, 12: 32, 32: 30, 30: 10,
            11: 23, 23: 31, 31: 22, 22: 11, }
        self.do_back = {
            7: 15, 15: 45, 45: 39, 39: 7,
            6: 25, 25: 46, 46: 28, 28: 6,
            5: 35, 35: 47, 47: 19, 19: 5,
            18: 16, 16: 36, 36: 38, 38: 18,
            17: 26, 26: 37, 37: 27, 27: 17, }

    def act(self, action: dict) -> dict:
        action = self.clean_act(action)
        if action not in self.actions:
            print(
                action, type(action),
                ': action not found.\navailable actions:',
                self.actions)
            return self.state
        cube = copy.deepcopy(self.state)
        for k, v in eval(f'self.do_{action[0]}').items():
            self.state[k] = cube[v]
        return self.see()


class RubiksCubeTwo(env.Environment):
    ''' simulates a Rubiks two by two Cube '''

    def __init__(self):
        self.name = '2x2 Rubiks Cube'
        self.state = {
            1: 'top', 2: 'top', 3: 'top', 4: 'top',
            5: 'front', 6: 'right', 7: 'back', 8: 'left',
            9: 'front',  10: 'right', 11: 'back', 12: 'left',
            13: 'front', 14: 'right', 15: 'back', 16: 'left',
            17: 'front', 18: 'right', 19: 'back', 20: 'left',
            21: 'under', 22: 'under', 23: 'under', 24: 'under', }
        self.original_state = copy.deepcopy(self.state)
        self.actions = [
            {0: 'top'}, {0: 'under'},
            {0: 'right'}, {0: 'left'},
            {0: 'front'}, {0: 'back'}, ]
        self.do_top = {
            1: 2, 2: 3, 3: 4, 4: 1,
            5: 6, 6: 7, 7: 8, 8: 5,
            9: 10, 10: 11, 11: 12, 12: 9, }
        self.do_under = {
            5: 6, 6: 7, 7: 8, 8: 5,
            9: 10, 10: 11, 11: 12, 12: 9,
            21: 22, 22: 23, 23: 24, 24: 21, }
        self.do_right = {
            9: 3, 3: 15, 15: 22, 22: 9,
            17: 2, 2: 7, 7: 23, 23: 17,
            6: 10, 10: 18, 18: 14, 14: 6, }
        self.do_left = {
            5: 4, 4: 19, 19: 21, 21: 5,
            13: 1, 1: 11, 11: 24, 24: 13,
            12: 8, 8: 16, 16: 20, 20: 12, }
        self.do_front = {
            5: 9, 9: 17, 17: 13, 13: 5,
            1: 6, 6: 22, 22: 20, 20: 1,
            2: 14, 14: 21, 21: 12, 12: 2, }
        self.do_back = {
            11: 7, 7: 19, 19: 15, 15: 11,
            4: 10, 10: 23, 23: 16, 16: 4,
            3: 18, 18: 24, 24: 8, 8: 3, }

    def act(self, action: dict) -> dict:
        action = self.clean_act(action)
        if action not in self.actions:
            print(
                action, type(action),
                ': action not found.\navailable actions:',
                self.actions)
            return self.state
        cube = copy.deepcopy(self.state)
        for k, v in eval(f'self.do_{action[0]}').items():
            self.state[k] = cube[v]
        return self.see()


class RubiksCubeOne(env.Environment):
    ''' simulates a Rubiks one by one Cube '''

    def __init__(self):
        self.name = '1x1 Rubiks Cube'
        self.state = {
            1: 'top', 2: 'front', 3: 'right', 4: 'back', 5: 'left', 6: 'under'}
        self.original_state = copy.deepcopy(self.state)
        self.actions = [
            {0: 'top'}, {0: 'under'},
            {0: 'right'}, {0: 'left'},
            {0: 'front'}, {0: 'back'}, ]
        self.do_top = {1: 1, 2: 3, 3: 4, 4: 5, 5: 2, 6: 6}
        self.do_under = {1: 1, 2: 5, 3: 2, 4: 3, 5: 4, 6: 6}
        self.do_right = {1: 4, 2: 1, 3: 3, 4: 6, 5: 5, 6: 2}
        self.do_left = {1: 2, 2: 6, 3: 3, 4: 1, 5: 5, 6: 4}
        self.do_front = {1: 3, 2: 2, 3: 6, 4: 4, 5: 1, 6: 5}
        self.do_back = {1: 5, 2: 2, 3: 1, 4: 4, 5: 6, 6: 3}

    def act(self, action: dict) -> dict:
        action = self.clean_act(action)
        if action not in self.actions:
            print(
                action, type(action),
                ': action not found.\navailable actions:',
                self.actions)
            return self.state
        cube = copy.deepcopy(self.state)
        for k, v in eval(f'self.do_{action[0]}').items():
            self.state[k] = cube[v]
        return self.see()
