import random
import time

class Hero:
    def __init__(self, name, health, attack, defense, ability):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.ability = ability
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage
    
    def is_alive(self):
        return self.health > 0
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    
    def special_attack(self):
        return random.randint(self.attack, self.attack * 2)
    
    def __str__(self):
        status = "ЖИВ" if self.is_alive() else "МЕРТВ"
        return f"{self.name}: {self.health}/{self.max_health} HP [{status}]"

class Boss:
    def __init__(self):
        self.name = "Злой Босс 🐲"
        self.max_health = 500
        self.health = 500
        self.attack = 30
        self.defense = 10
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage
    
    def is_alive(self):
        return self.health > 0
    
    def boss_attack(self):
        return random.randint(self.attack - 5, self.attack + 10)
    
    def __str__(self):
        return f"{self.name}: {self.health}/{self.max_health} HP"

class TextGame:
    def __init__(self):
        self.heroes = [
            Hero("Воин 🛡️", 120, 25, 15, "Двойной удар"),
            Hero("Маг 🔮", 80, 40, 5, "Огненный шар"),
            Hero("Лучник 🏹", 90, 30, 8, "Критический выстрел"),
            Hero("Жрец ✨", 100, 15, 10, "Лечение")
        ]
        self.boss = Boss()
        self.current_hero = 0
        self.battle_log = []
    
    def clear_screen(self):
        print("\n" * 50)
    
    def add_log(self, message):
        self.battle_log.append(message)
        if len(self.battle_log) > 10:
            self.battle_log.pop(0)
    
    def show_status(self):
        print("═" * 50)
        print(f"⚔️  {self.boss}")
        print("─" * 30)
        for hero in self.heroes:
            print(f"  {hero}")
        print("═" * 50)
    
    def show_log(self):
        print("\n📜 Ход боя:")
        for log in self.battle_log[-5:]:  # Последние 5 записей
            print(f"  • {log}")
    
    def hero_turn(self):
        hero = self.heroes[self.current_hero]
        if not hero.is_alive():
            self.current_hero = (self.current_hero + 1) % len(self.heroes)
            return
        
        print(f"\n🎯 Ход {hero.name}...")
        time.sleep(1)
        
        # Обычная атака или способность
        if random.random() < 0.3:  # 30% шанс использовать способность
            damage = hero.special_attack()
            actual_damage = self.boss.take_damage(damage)
            self.add_log(f"{hero.name} использует {hero.ability}! Урон: {actual_damage}")
        else:
            damage = random.randint(hero.attack - 5, hero.attack + 5)
            actual_damage = self.boss.take_damage(damage)
            self.add_log(f"{hero.name} атакует! Урон: {actual_damage}")
        
        # Жрец лечит случайного героя
        if hero.name == "Жрец ✨":
            alive_heroes = [h for h in self.heroes if h.is_alive() and h != hero]
            if alive_heroes:
                target = random.choice(alive_heroes)
                heal_amount = random.randint(15, 25)
                target.heal(heal_amount)
                self.add_log(f"{hero.name} лечит {target.name} на {heal_amount} HP")
        
        self.current_hero = (self.current_hero + 1) % len(self.heroes)
    
    def boss_turn(self):
        if not self.boss.is_alive():
            return
        
        print(f"\n👹 Ход {self.boss.name}...")
        time.sleep(1)
        
        # Босс атакует случайного живого героя
        alive_heroes = [hero for hero in self.heroes if hero.is_alive()]
        if alive_heroes:
            target = random.choice(alive_heroes)
            damage = self.boss.boss_attack()
            actual_damage = target.take_damage(damage)
            self.add_log(f"{self.boss.name} атакует {target.name}! Урон: {actual_damage}")
    
    def check_game_over(self):
        if not self.boss.is_alive():
            return "VICTORY"
        
        if all(not hero.is_alive() for hero in self.heroes):
            return "DEFEAT"
        
        return None
    
    def show_menu(self):
        self.clear_screen()
        print("🎮" * 25)
        print("           PARTY VS BOSS - ТЕКСТОВАЯ ВЕРСИЯ")
        print("🎮" * 25)
        print("\n👥 Ваша партия:")
        for hero in self.heroes:
            print(f"  • {hero.name} - {hero.ability}")
        print(f"\n🐲 Противник: {self.boss.name}")
        print("\n🎯 Управление:")
        print("  • ENTER - следующий ход")
        print("  • q - выйти из игры")
        print("\n" + "═" * 50)
        input("Нажмите ENTER чтобы начать бой...")
    
    def show_victory(self):
        self.clear_screen()
        print("🎉" * 25)
        print("           ПОБЕДА! ГЕРОИ СПАСЛИ МИР!")
        print("🎉" * 25)
        print(f"\n🏆 {self.boss.name} повержен!")
        print("\n🎊 Выжившие герои:")
        for hero in self.heroes:
            if hero.is_alive():
                print(f"  • {hero.name} - {hero.health} HP")
    
    def show_defeat(self):
        self.clear_screen()
        print("💀" * 25)
        print("           ПОРАЖЕНИЕ... БОСС ПОБЕДИЛ")
        print("💀" * 25)
        print(f"\n😈 {self.boss.name} торжествует!")
        print("\n⚰️  Павшие герои:")
        for hero in self.heroes:
            if not hero.is_alive():
                print(f"  • {hero.name}")
    
    def run(self):
        self.show_menu()
        
        while True:
            self.clear_screen()
            self.show_status()
            self.show_log()
            
            # Проверка конца игры
            game_result = self.check_game_over()
            if game_result == "VICTORY":
                self.show_victory()
                break
            elif game_result == "DEFEAT":
                self.show_defeat()
                break
            
            print(f"\n🎯 Следующий ход: {self.heroes[self.current_hero].name}")
            command = input("\nНажмите ENTER для хода (q - выход): ")
            
            if command.lower() == 'q':
                print("\n👋 Выход из игры...")
                break
            
            # Ход героя
            self.hero_turn()
            
            # Проверка после хода героя
            game_result = self.check_game_over()
            if game_result:
                self.clear_screen()
                self.show_status()
                self.show_log()
                if game_result == "VICTORY":
                    self.show_victory()
                else:
                    self.show_defeat()
                break
            
            # Ход босса
            self.boss_turn()
            
            time.sleep(1)
        
        print("\n" + "═" * 50)
        restart = input("Хотите сыграть еще раз? (y/n): ")
        if restart.lower() == 'y':
            new_game = TextGame()
            new_game.run()

# Запуск игры
if __name__ == "__main__":
    print("Загрузка игры...")
    game = TextGame()
    game.run()