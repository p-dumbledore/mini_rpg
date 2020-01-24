import random

class Character():
    def __init__(self, name, hp_full):
        self.name = name
        self.hp_full = hp_full
        self.hp_now = self.hp_full
        self.defend_flag = 0

    def set_init_parameter(self, ap, cp, rs, ag):
        """ap, cp, rs, ag"""
        self.attack_point = ap
        self.cure_point = cp
        self.run_successrate = rs
        self.agility = ag

    def update_parameter(self, param, value):
        """attack_point, cure_point, run_successrate, agility"""
        if param == 'hp_full':
            self.hp_full = value

        elif param == 'attack_point':
            self.attack_point = value

        elif param == 'cure_point':
            self.cure_point = value

        elif param == 'run_successrate':
            self.run_successrate = value

        elif param == 'agility':
            self.agility = value

    def set_hp_now(self, hp):
        self.hp_now = hp

    def plus_hp(self, hp):
        self.hp_now += hp

    def minus_hp(self, hp):
        self.hp_now -= hp

    def get_hp_full(self):
        return self.hp_full

    def get_hp_now(self):
        return self.hp_now

    def get_parameter(self, param):
        if param == 'hp_full':
            return self.hp_full

        elif param == 'attack_point':
            return self.attack_point

        elif param == 'cure_point':
            return self.cure_point

        elif param == 'run_successrate':
            return self.run_successrate

        elif param == 'agility':
            return self.agility
        elif param == 'name':
            return self.name

    def set_defend_flag(self, zero_or_one):
        if zero_or_one == 0 or zero_or_one == 1:
            self.defend_flag = zero_or_one
        else:
            raise Exception("Set Positional Argument Zero Or One")
            exit()

    def check_defend_flag(self):
        return self.defend_flag

class Player(Character):
    def __init__(self, name, hp_full, init_coordinates):
        self.name = name
        self.hp_full = hp_full
        self.hp_now = self.hp_full
        self.defend_flag = 0
        self.coordinates = init_coordinates
        self.exp = 0
        self.level = 1
        self.levels = [[1, 0], [2, 300], [3, 1000], [4, 2500], [5, 4000], [6, 10000], [7, 15000],
                      [8, 30000], [9, 50000], [10, 100000]]

    def change_coordinates(self, coordinates):
        self.coordinates = coordinates

    def get_coordinates(self):
        return self.coordinates

    def gain_exp(self, exp):
        self.exp += exp

    def update_level(self):
        for i in range(10):
            if self.exp >= self.levels[i][1]:
                print("***Level Up to " + str(i + 1) + "***")
                self.level = i + 1


class Opponent(Character):
    def __init__(self, name, hp_full, strategy, exp):
        self.name = name
        self.hp_full = hp_full
        self.hp_now = self.hp_full
        self.defend_flag = 0
        self.strategy = strategy
        self.exp = exp

    def get_command(self):
        if self.strategy == 0:
            hpn = self.hp_now
            hpf = self.hp_full
            if hpn > hpf * 0.8:
                rand = random.randint(0, 5)
                if 0 <= rand < 2:
                    return 'a'
                elif 2 <= rand < 4:
                    return 'd'
                else:
                    return 'r'
            elif hpf * 0.6 < hpn <= hpf * 0.8:
                rand = random.randint(0, 2)
                if rand == 0:
                    return 'a'
                elif rand == 1:
                    return 'd'
                elif rand == 2:
                    return 'c'
            elif hpf * 0.2 < hpn <= hpf * 0.6:
                rand = random.randint(0, 100)
                if 0 <= rand < 20:
                    return 'a'
                elif 20 <= rand < 50:
                    return 'd'
                elif 50 <= rand < 80:
                    return 'c'
                else:
                    return 'r'
            else:
                return 'c'

    def get_exp(self):
        return self.exp
