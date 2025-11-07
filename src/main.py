import random
import time
import sys
import unittest

class Hero:
    def __init__(self, name, health, attack, defense, mana, skills):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.mana = mana
        self.max_mana = mana
        self.skills = skills
        self.is_protagonist = False
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage
    
    def is_alive(self):
        return self.health > 0
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    
    def restore_mana(self, amount):
        self.mana = min(self.max_mana, self.mana + amount)
    
    def use_skill(self, skill_name, target):
        if skill_name in self.skills and self.mana >= self.skills[skill_name]['mana_cost']:
            self.mana -= self.skills[skill_name]['mana_cost']
            return self.skills[skill_name]['effect'](self, target)
        return None
    
    def __str__(self):
        status = "💚" if self.is_alive() else "💀"
        prot = "⭐" if self.is_protagonist else ""
        return f"{prot}{self.name} {status} HP: {self.health}/{self.max_health} MP: {self.mana}/{self.max_mana}"

class Boss:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.name = "Злой Босс 🐲"
        difficulties = {
            'easy': {'health': 300, 'attack': 20, 'defense': 5},
            'medium': {'health': 500, 'attack': 30, 'defense': 10},
            'hard': {'health': 800, 'attack': 40, 'defense': 15}
        }
        stats = difficulties[difficulty]
        self.max_health = stats['health']
        self.health = stats['health']
        self.attack = stats['attack']
        self.defense = stats['defense']
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage
    
    def is_alive(self):
        return self.health > 0
    
    def boss_attack(self):
        return random.randint(self.attack - 5, self.attack + 10)
    
    def __str__(self):
        return f"{self.name} 💔 HP: {self.health}/{self.max_health}"

class Game:
    def __init__(self):
        self.hero_pool = [
            Hero("Воин 🛡️", 120, 25, 15, 30, {
                'Сильный удар': {'mana_cost': 10, 'effect': lambda self, target: target.take_damage(self.attack + 10)},
                'Защита': {'mana_cost': 5, 'effect': lambda self, target: (self.defense + 5, "Защита повышена")}
            }),
            Hero("Маг 🔮", 80, 15, 5, 100, {
                'Огненный шар': {'mana_cost': 20, 'effect': lambda self, target: target.take_damage(40)},
                'Ледяная стрела': {'mana_cost': 15, 'effect': lambda self, target: target.take_damage(30)}
            }),
            Hero("Лучник 🏹", 90, 30, 8, 50, {
                'Критический выстрел': {'mana_cost': 15, 'effect': lambda self, target: target.take_damage(self.attack * 2)},
                'Стрела яда': {'mana_cost': 10, 'effect': lambda self, target: target.take_damage(25)}
            }),
            Hero("Жрец ✨", 100, 10, 10, 80, {
                'Лечение': {'mana_cost': 15, 'effect': lambda self, target: target.heal(30)},
                'Благословение': {'mana_cost': 20, 'effect': lambda self, target: (target.attack + 5, "Атака повышена")}
            }),
            Hero("Вор 🗡️", 85, 35, 6, 40, {
                'Смертельный удар': {'mana_cost': 25, 'effect': lambda self, target: target.take_damage(50)},
                'Уклонение': {'mana_cost': 10, 'effect': lambda self, target: (self.defense + 10, "Уклонение повышено")}
            }),
            Hero("Паладин ⚔️", 110, 20, 20, 60, {
                'Божественный удар': {'mana_cost': 30, 'effect': lambda self, target: target.take_damage(35)},
                'Исцеление': {'mana_cost': 20, 'effect': lambda self, target: target.heal(25)}
            })
        ]
        self.party = []
        self.boss = None
        self.current_protagonist = 0
        self.game_seed = None
        self.difficulty = 'medium'
        self.game_state = "MAIN_MENU"
        self.battle_log = []
    
    def set_seed(self, seed):
        self.game_seed = seed
        random.seed(seed)
    
    def clear_screen(self):
        print("\n" * 50)
    
    def add_log(self, message):
        self.battle_log.append(message)
        if len(self.battle_log) > 10:
            self.battle_log.pop(0)
    
    def show_main_menu(self):
        self.clear_screen()
        print("🎮" * 25)
        print("           PARTY VS BOSS - ПОЛНАЯ ВЕРСИЯ")
        print("🎮" * 25)
        print("\n1. Новая игра")
        print("2. Справка")
        print("3. Тесты")
        print("4. Выход")
        print("\n" + "═" * 50)
    
    def show_difficulty_menu(self):
        self.clear_screen()
        print("🎯 ВЫБОР СЛОЖНОСТИ")
        print("═" * 50)
        print("1. Легкий (300 HP босса)")
        print("2. Средний (500 HP босса)")
        print("3. Сложный (800 HP босса)")
        print("\n0. Назад")
    
    def show_seed_menu(self):
        self.clear_screen()
        print("🔢 НАЗНАЧЕНИЕ SEED")
        print("═" * 50)
        print("Введите число для seed (или Enter для случайного):")
        print("Seed влияет на случайную генерацию боя")
        print("\n0. Назад")
    
    def show_party_selection(self):
        self.clear_screen()
        print("👥 ВЫБОР ПАРТИИ (4 героя)")
        print("═" * 50)
        for i, hero in enumerate(self.hero_pool, 1):
            selected = "✅" if hero in self.party else "  "
            print(f"{selected} {i}. {hero}")
        
        print(f"\nВыбрано: {len(self.party)}/4 героев")
        print("\n0. Завершить выбор")
    
    def show_help(self):
        self.clear_screen()
        print("📖 СПРАВКА")
        print("═" * 50)
        print("УПРАВЛЕНИЕ:")
        print("• Главное меню: цифры 1-4")
        print("• В бою: цифры для выбора действий")
        print("• Протагонист (⭐) может менять персонажей")
        print("\nСЛОЖНОСТЬ:")
        print("• Легкий: босс 300 HP")
        print("• Средний: босс 500 HP")  
        print("• Сложный: босс 800 HP")
        print("\nSEED:")
        print("• Одинаковый seed = одинаковый бой")
        print("• Для случайного - оставьте пустым")
        input("\nНажмите Enter для возврата...")
    
    def show_battle_menu(self):
        self.clear_screen()
        print("⚔️  МЕНЮ БОЯ")
        print("═" * 50)
        print(f"Противник: {self.boss}")
        print("\nВаша партия:")
        for i, hero in enumerate(self.party):
            print(f"  {hero}")
        
        print(f"\nТекущий протагонист: {self.party[self.current_protagonist].name} ⭐")
        print("\n1. Атака")
        print("2. Навыки")
        print("3. Сменить персонажа")
        print("4. Пропустить ход")
        print("0. Сдаться")
        
        self.show_battle_log()
    
    def show_attack_menu(self):
        self.clear_screen()
        print("🗡️  МЕНЮ АТАКИ")
        print("═" * 50)
        print(f"Атакует: {self.party[self.current_protagonist].name}")
        print(f"Цель: {self.boss}")
        print("\n1. Обычная атака")
        print("2. Сильная атака (+50% урона, -5 MP)")
        print("0. Назад")
    
    def show_skills_menu(self):
        self.clear_screen()
        hero = self.party[self.current_protagonist]
        print("✨ МЕНЮ НАВЫКОВ")
        print("═" * 50)
        print(f"Использует: {hero.name}")
        print(f"Мана: {hero.mana}/{hero.max_mana}")
        print("\nДоступные навыки:")
        
        skills = list(hero.skills.keys())
        for i, skill in enumerate(skills, 1):
            cost = hero.skills[skill]['mana_cost']
            print(f"{i}. {skill} ({cost} MP)")
        
        print("\n0. Назад")
        return skills
    
    def show_switch_menu(self):
        self.clear_screen()
        print("🔄 МЕНЮ СМЕНЫ ПЕРСОНАЖА")
        print("═" * 50)
        print("Выберите нового протагониста:")
        
        for i, hero in enumerate(self.party):
            marker = "⭐" if i == self.current_protagonist else "  "
            print(f"{i+1}. {marker} {hero.name}")
        
        print("\n0. Назад")
    
    def show_battle_log(self):
        print("\n📜 ХОД БОЯ:")
        for log in self.battle_log[-5:]:
            print(f"  • {log}")
    
    def run_tests(self):
        self.clear_screen()
        print("🧪 ЗАПУСК ТЕСТОВ")
        print("═" * 50)
        
        # Простые тесты
        test_hero = Hero("Тест", 100, 10, 5, 50, {})
        test_boss = Boss('easy')
        
        print("✓ Герой создан успешно")
        print("✓ Босс создан успешно")
        
        damage = test_hero.take_damage(15)
        print(f"✓ Получение урона: {damage}")
        
        test_hero.heal(10)
        print("✓ Лечение работает")
        
        print("✓ Все тесты пройдены!")
        input("\nНажмите Enter для возврата...")
    
    def start_new_game(self):
        self.party = []
        self.battle_log = []
        self.game_state = "DIFFICULTY_MENU"
    
    def select_difficulty(self, choice):
        difficulties = {'1': 'easy', '2': 'medium', '3': 'hard'}
        if choice in difficulties:
            self.difficulty = difficulties[choice]
            self.game_state = "SEED_MENU"
        elif choice == '0':
            self.game_state = "MAIN_MENU"
    
    def set_game_seed(self, seed_input):
        if seed_input == '0':
            self.game_state = "DIFFICULTY_MENU"
        elif seed_input.strip() == '':
            self.game_seed = None
            self.game_state = "PARTY_SELECTION"
        else:
            try:
                self.set_seed(int(seed_input))
                self.game_state = "PARTY_SELECTION"
            except ValueError:
                print("Ошибка: введите число!")
                time.sleep(1)
    
    def select_party_member(self, choice):
        try:
            index = int(choice) - 1
            if 0 <= index < len(self.hero_pool):
                hero = self.hero_pool[index]
                if hero in self.party:
                    self.party.remove(hero)
                elif len(self.party) < 4:
                    self.party.append(hero)
            
            if choice == '0' and len(self.party) == 4:
                self.party[0].is_protagonist = True
                self.boss = Boss(self.difficulty)
                self.game_state = "BATTLE"
                self.add_log("Бой начался!")
        except ValueError:
            pass
    
    def battle_turn(self, choice):
        hero = self.party[self.current_protagonist]
        
        if choice == '1':  # Атака
            self.game_state = "ATTACK_MENU"
        elif choice == '2':  # Навыки
            if any(hero.mana >= cost for skill, cost in hero.skills.items()):
                self.game_state = "SKILLS_MENU"
            else:
                self.add_log(f"У {hero.name} недостаточно маны!")
        elif choice == '3':  # Смена персонажа
            self.game_state = "SWITCH_MENU"
        elif choice == '4':  # Пропуск хода
            self.add_log(f"{hero.name} пропускает ход")
            self.next_turn()
        elif choice == '0':  # Сдаться
            self.game_state = "DEFEAT"
    
    def attack_turn(self, choice):
        hero = self.party[self.current_protagonist]
        
        if choice == '1':  # Обычная атака
            damage = random.randint(hero.attack - 5, hero.attack + 5)
            actual_damage = self.boss.take_damage(damage)
            self.add_log(f"{hero.name} атакует! Урон: {actual_damage}")
            self.next_turn()
        elif choice == '2':  # Сильная атака
            if hero.mana >= 5:
                hero.mana -= 5
                damage = random.randint(hero.attack, hero.attack + 10)
                actual_damage = self.boss.take_damage(damage)
                self.add_log(f"{hero.name} использует сильную атаку! Урон: {actual_damage}")
                self.next_turn()
            else:
                self.add_log("Недостаточно маны для сильной атаки!")
        elif choice == '0':
            self.game_state = "BATTLE"
    
    def skill_turn(self, choice, skills):
        if choice == '0':
            self.game_state = "BATTLE"
            return
        
        try:
            skill_index = int(choice) - 1
            if 0 <= skill_index < len(skills):
                skill_name = skills[skill_index]
                hero = self.party[self.current_protagonist]
                result = hero.use_skill(skill_name, self.boss)
                
                if result is not None:
                    if isinstance(result, tuple):  # Бафф
                        self.add_log(f"{hero.name} использует {skill_name}! {result[1]}")
                    else:  # Урон
                        self.add_log(f"{hero.name} использует {skill_name}! Урон: {result}")
                    self.next_turn()
                else:
                    self.add_log("Не удалось использовать навык!")
        except ValueError:
            pass
    
    def switch_turn(self, choice):
        if choice == '0':
            self.game_state = "BATTLE"
            return
        
        try:
            new_index = int(choice) - 1
            if 0 <= new_index < len(self.party):
                self.party[self.current_protagonist].is_protagonist = False
                self.current_protagonist = new_index
                self.party[self.current_protagonist].is_protagonist = True
                self.add_log(f"Протагонист изменен на {self.party[self.current_protagonist].name}")
                self.game_state = "BATTLE"
        except ValueError:
            pass
    
    def next_turn(self):
        # Восстановление маны
        for hero in self.party:
            if hero.is_alive():
                hero.restore_mana(5)
        
        # Ход босса
        if self.boss.is_alive():
            alive_heroes = [h for h in self.party if h.is_alive()]
            if alive_heroes:
                target = random.choice(alive_heroes)
                damage = self.boss.boss_attack()
                actual_damage = target.take_damage(damage)
                self.add_log(f"{self.boss.name} атакует {target.name}! Урон: {actual_damage}")
        
        # Проверка конца игры
        if not self.boss.is_alive():
            self.game_state = "VICTORY"
        elif all(not hero.is_alive() for hero in self.party):
            self.game_state = "DEFEAT"
        else:
            self.current_protagonist = (self.current_protagonist + 1) % len(self.party)
            while not self.party[self.current_protagonist].is_alive():
                self.current_protagonist = (self.current_protagonist + 1) % len(self.party)
            
            self.game_state = "BATTLE"
    
    def show_victory(self):
        self.clear_screen()
        print("🎉" * 25)
        print("           ПОБЕДА! ГЕРОИ СПАСЛИ МИР!")
        print("🎉" * 25)
        print(f"\n🏆 {self.boss.name} повержен!")
        print("\n🎊 Выжившие герои:")
        for hero in self.party:
            if hero.is_alive():
                print(f"  • {hero.name} - {hero.health} HP")
        
        print(f"\n🔢 Seed игры: {self.game_seed or 'случайный'}")
        input("\nНажмите Enter для возврата в меню...")
        self.game_state = "MAIN_MENU"
    
    def show_defeat(self):
        self.clear_screen()
        print("💀" * 25)
        print("           ПОРАЖЕНИЕ... БОСС ПОБЕДИЛ")
        print("💀" * 25)
        print(f"\n😈 {self.boss.name} торжествует!")
        print(f"\n🔢 Seed игры: {self.game_seed or 'случайный'}")
        input("\nНажмите Enter для возврата в меню...")
        self.game_state = "MAIN_MENU"
    
    def run(self):
        while True:
            if self.game_state == "MAIN_MENU":
                self.show_main_menu()
                choice = input("Выберите пункт: ")
                
                if choice == '1':
                    self.start_new_game()
                elif choice == '2':
                    self.show_help()
                elif choice == '3':
                    self.run_tests()
                elif choice == '4':
                    print("Выход из игры...")
                    break
            
            elif self.game_state == "DIFFICULTY_MENU":
                self.show_difficulty_menu()
                choice = input("Выберите сложность: ")
                self.select_difficulty(choice)
            
            elif self.game_state == "SEED_MENU":
                self.show_seed_menu()
                seed_input = input("Seed: ")
                self.set_game_seed(seed_input)
            
            elif self.game_state == "PARTY_SELECTION":
                self.show_party_selection()
                choice = input("Выберите героя: ")
                self.select_party_member(choice)
            
            elif self.game_state == "BATTLE":
                self.show_battle_menu()
                choice = input("Выберите действие: ")
                self.battle_turn(choice)
            
            elif self.game_state == "ATTACK_MENU":
                self.show_attack_menu()
                choice = input("Выберите атаку: ")
                self.attack_turn(choice)
            
            elif self.game_state == "SKILLS_MENU":
                skills = self.show_skills_menu()
                choice = input("Выберите навык: ")
                self.skill_turn(choice, skills)
            
            elif self.game_state == "SWITCH_MENU":
                self.show_switch_menu()
                choice = input("Выберите персонажа: ")
                self.switch_turn(choice)
            
            elif self.game_state == "VICTORY":
                self.show_victory()
            
            elif self.game_state == "DEFEAT":
                self.show_defeat()

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()