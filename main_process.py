import maps
from classes import Character, Player, Opponent
import random
import json



slime = Opponent("Slime", 80, 0, 100)
slime.set_init_parameter(30, 70, 70, 70)

def move_in_map(actor):
    while True:
        print(maps.map1(actor.get_coordinates()))
        move = input("Move?(w, a, s, d): ")
        move = move.lower()
        if move == 'w':
            try:
                tmp = actor.get_coordinates()
                maps.map1([tmp[0], tmp[1] - 1])
            except Exception as error:
                print(error)
                continue
            else:
                actor.change_coordinates([tmp[0], tmp[1] - 1])
                print(maps.map1(actor.get_coordinates()))
                break

        elif move == 'a':
            try:
                tmp = actor.get_coordinates()
                maps.map1([tmp[0] - 1, tmp[1]])
            except Exception as error:
                print(error)
                continue
            else:
                actor.change_coordinates([tmp[0] - 1, tmp[1]])
                print(maps.map1(actor.get_coordinates()))
                break

        elif move == 's':
            try:
                tmp = actor.get_coordinates()
                maps.map1([tmp[0], tmp[1] + 1])
            except Exception as error:
                print(error)
                continue
            else:
                actor.change_coordinates([tmp[0], tmp[1] + 1])
                print(maps.map1(actor.get_coordinates()))
                break

        elif move == 'd':
            try:
                tmp = actor.get_coordinates()
                maps.map1([tmp[0] + 1, tmp[1]])
            except Exception as error:
                print(error)
                continue
            else:
                actor.change_coordinates([tmp[0] + 1, tmp[1]])
                print(maps.map1(actor.get_coordinates()))
                break


def encounter():
    rand_encounter = random.randint(0, 100)
    if (rand_encounter > 40):
        rand_monster = random.randint(0, 100)
        if 0 <= rand_monster <= 99:
            return slime
    else:
        return 0

def indicate_hp(actor, enemy):
    hpnow_a = actor.get_hp_now()
    hpfull_a = actor.get_hp_full()
    dots_a = round((hpnow_a / hpfull_a * 20))
    print(actor.get_parameter('name') + ' HP: ', end='')
    for i in range(dots_a):
        print('*', end='')
    print('\n')
    hpnow_e = enemy.get_hp_now()
    hpfull_e = enemy.get_hp_full()
    dots_e = round((hpnow_e / hpfull_e * 20))
    print(enemy.get_parameter('name') + ' HP: ', end='')
    for i in range(dots_e):
        print('*', end='')
    print('\n')

def battle(actor, enemy):
    print(enemy.get_parameter('name') + " Appeared!")
    input()
    while True:
        actor_ag = actor.get_parameter('agility')
        enemy_ag = actor.get_parameter('agility')

        tmp_actor_ag = round(actor_ag * (random.randint(80, 121) / 100))
        tmp_enemy_ag = round(enemy_ag * (random.randint(80, 121) / 100))

        flag = 0

        if (tmp_actor_ag > tmp_enemy_ag):
            flag = actor_turn(actor, enemy)
            if not flag:
                flag = enemy_turn(actor, enemy)

        elif (tmp_actor_ag > tmp_enemy_ag):
                flag = enemy_turn(actor, enemy)
                if not flag:
                    flag = actor_turn(actor, enemy)

        actor.set_defend_flag(0)
        enemy.set_defend_flag(0)

        if flag == 1:
            print(actor.get_parameter('name') + " Won!")
            input()
            get_exp(actor, enemy)
            actor.set_hp_now(actor.get_hp_full())
            enemy.set_hp_now(enemy.get_hp_full())
            return 0
        elif flag == 2:
            print(actor.get_parameter('name') + " Lost...")
            input()
            actor.set_hp_now(actor.get_hp_full())
            enemy.set_hp_now(enemy.get_hp_full())
            return 1
        elif flag == 3:
            print("Battle Ended")
            input()
            actor.set_hp_now(actor.get_hp_full())
            enemy.set_hp_now(enemy.get_hp_full())
            return 0

def actor_turn(actor, enemy):
    while True:
        indicate_hp(actor, enemy)
        try:
            command = input("Command?([A]ttack, [D]efend, [C]ure, [R]un): ")
            command = command.lower()
            if command == 'a':
                print(actor.get_parameter('name') + " Hit " + enemy.get_parameter('name'))
                input()
                enemy_flag = enemy.check_defend_flag()
                if enemy_flag == 1:
                    print(enemy.get_parameter('name') + " Defended!")
                    input()
                    actor_attack = round(actor.get_parameter('attack_point') * (random.randint(80, 121) / 100) * 0.5)
                else:
                    actor_attack = round(actor.get_parameter('attack_point') * (random.randint(80, 121) / 100))
                print("Damage: " + str(actor_attack))
                input()
                enemy.minus_hp(actor_attack)
                if enemy.get_hp_now() < 0:
                    return 1
                return 0

            elif command == 'd':
                print(actor.get_parameter('name') + " Got Ready to Defend!")
                input()
                actor.set_defend_flag(1)
                return 0

            elif command == 'c':
                cure = round(actor.get_parameter('cure_point') * (random.randint(80, 121) / 100))
                if actor.get_hp_now() + cure > actor.get_hp_full():
                    actor.set_hp_now(actor.get_hp_full())
                    print("The HP of " + actor.get_parameter('name') + " Was Set Full!")
                    input()

                else:
                    actor.plus_hp(cure)
                    print("The HP of " + actor.get_parameter('name') + " Was Cured " + str(cure) + " Points!")
                    input()
                return 0

            elif command == 'r':
                success_counter = random.randint(1, 101)
                if success_counter <= actor.run_successrate:
                    print(actor.get_parameter('name') + " Succeeded to Run Away!")
                    input()
                    return 3
                else:
                    print(actor.get_parameter('name') + " Failed to Run Away!")
                    input()
                    return 0

            else:
                raise Exception("Error: Command Not Found")
        except Exception as error:
            print(error)
            continue


def enemy_turn(actor, enemy):
    while True:
        indicate_hp(actor, enemy)
        command = enemy.get_command()

        try:
            if command == 'a':
                print(enemy.get_parameter('name') + " Hit " + actor.get_parameter('name'))
                input()
                actor_flag = actor.check_defend_flag()
                if actor_flag == 1:
                    print(actor.get_parameter('name') + " Defended!")
                    input()
                    enemy_attack = round(enemy.get_parameter('attack_point') * (random.randint(80, 121) / 100) * 0.5)
                else:
                    enemy_attack = round(enemy.get_parameter('attack_point') * (random.randint(80, 121) / 100))
                print("Damage: " + str(enemy_attack))
                input()
                actor.minus_hp(enemy_attack)
                if actor.get_hp_now() < 0:
                    return 1
                return 0

            elif command == 'd':
                print(enemy.get_parameter('name') + " Got Ready to Defend!")
                input()
                enemy.set_defend_flag(1)
                return 0

            elif command == 'c':
                cure = round(enemy.get_parameter('cure_point') * (random.randint(80, 121) / 100))
                if enemy.get_hp_now() + cure > enemy.get_hp_full():
                    enemy.set_hp_now(enemy.get_hp_full())
                    print("The HP of " + enemy.get_parameter('name') + " Was Set Full!")
                    input()
                else:
                    enemy.plus_hp(cure)
                    print("The HP of " + enemy.get_parameter('name') + " Was Cured " + str(cure) + " Points!")
                    input()
                return 0

            elif command == 'r':
                success_counter = random.randint(1, 101)
                if success_counter <= enemy.run_successrate:
                    print(enemy.get_parameter('name') + " Succeeded to Run Away!")
                    input()
                    return 3
                else:
                    print(enemy.get_parameter('name') + " Failed to Run Away!")
                    input()
                    return 0

            else:
                raise Exception("Error: Command Not Found")
        except Exception as error:
            print(error)
            continue

def get_exp(actor, enemy):
    exp_given = enemy.get_exp()
    actor.gain_exp(exp_given)

    actor.update_level()

def base(actor):
    while True:
        move_in_map(actor)
        enemy = encounter()
        if not enemy:
            continue
        else:
            battle_flag = battle(actor, enemy)
            if battle_flag == 1:
                print("Game Over...")
                input()
                print("Please Play Again")
                input()
                exit()
            else:
                continue


print("""How to Move:
   ^
   |
   w
<-asd->
   |
   v
Control+Z to Quit""")
input()

tmp = input("Your Name?: ")
player = Player(tmp, 100, [1, 2])
player.set_init_parameter(30, 70, 70, 80)


base(player)
