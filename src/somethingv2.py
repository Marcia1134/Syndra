from time import sleep
import random
import os

# Config

# Stores
population_store = []
dead_store = []

# Variables
space = 1000000000
food = 1000000000
water = 1000000000
resources = 1000

# Population
population = 10000
population_max = population * 10
mating_age = 12
mating_chance = 0.9
mating_children = 2
preg_time = 2
preg_chance = 1
fitness = 1
age = 0
max_age = 100
death_curve = [0.5, 0.5, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 1.0]

# Events
disease_chance = 0.1
disease_mortality = 0.5
disease_cure = 0.5
disease_duration = 1
disease = False
disease_time = 0
natural_disaster_chance = 0.1
natural_disaster_mortality = 0.5
natural_disaster_duration = 1
natural_disaster = False
natural_disaster_time = 0

# Misc
max_init_stats = 10
verbose = False

# classes
class stats():
    def __init__(self):
        self.intelligence = random.randint(1, max_init_stats)
        self.strength = random.randint(1, max_init_stats)
        self.agility = random.randint(1, max_init_stats)
        self.happiness = random.randint(1, max_init_stats)
        self.satisfaction = random.randint(1, max_init_stats)
        self.health = random.randint(1, max_init_stats)

class Person:
    def __init__(self):
        self.age = 0
        self.gender = random.randint(0, 1) # Female | Male
        self.fitness = fitness
        self.ispregnant = False
        self.pregnant_time = 0
        self.pregnant_chance = preg_chance
        self.isfed = True
        self.iswatered = True
        self.ishealthy = True
        self.iseducated = False
        self.isemployed = False
        self.ismilitary = False
        self.isleader = False
        self.ismarried = False
        self.isdead = False

        self.stats = stats()

# Fill stores
for i in range(population):
    population_store.append(Person())
print(len(population_store))
while True:
    
    for person in population_store:
        # Grow
        person.age += 1
        if person.ispregnant:
            person.pregnant_time -= 1
        
        # Get Married
        if person.age >= mating_age and not person.ismarried and random.random() < mating_chance:
            person.ismarried = True

        # Check mating
        if person.age >= mating_age and not person.ismarried and random.random() < mating_chance:
            person.ismarried = True
            if verbose:
                print(f"Person {person} got married.")            

        # Check pregnancy
        if person.age >= mating_age and person.ismarried and not person.ispregnant and random.random() < person.pregnant_chance:
            person.ispregnant = True
            person.pregnant_time = preg_time
            if verbose:
                print(f"Person {person} is pregnant.")

        # Give birth
        if person.ispregnant and person.pregnant_time < 1 and person.gender == 0:
            for i in range(mating_children):
                population_store.append(Person())
            person.ispregnant = False
            person.pregnant_time = 0
            if verbose:
                print(f"Person {person} gave birth to {mating_children} children.")

        # Check food
        if food > 0:
            food -= 1
            person.isfed = True

        # Check water
        if water > 0:
            water -= 1
            person.iswatered = True

        # Check health
        if person.stats.health > 0:
            person.ishealthy = True

        # Work
        if person.isemployed:
            person.isfed = False
            person.iswatered = False

        # Check death
        if person.age > max_age:
            person.isdead = True
            if verbose:
                print(f"Person {person} died of old age.")
        death_chance = death_curve[person.age]
        if not person.isfed:
            death_chance += 0.1
        if not person.iswatered:
            death_chance += 0.1
        if not person.ishealthy:
            death_chance += 0.1
        if not person.iseducated:
            death_chance += 0.05
        if person.stats.health > 0:
            death_chance -= 0.05
        if person.stats.health > 50:
            death_chance -= 0.15
        if person.stats.health > 75:
            death_chance -= 0.20
        if random.random() < death_chance:
            person.isdead = True
            if verbose:
                print(f"Person {person} died of natural causes.")

        # Gleam
        if person.isdead:
            dead_store.append(person)
            population_store.remove(person)
            if verbose:
                print(f"Person {person} was removed from the population.")
                continue
        else:
            continue
    
    # graph
    rows, columns = os.popen('stty size', 'r').read().split()
    unit_space = population_max / int(columns)
    unit = "█"
    bar = ""
    for i in range(1, round(len(population_store)/unit_space)):
        bar += unit
    if bar == "":
        bar = "" + unit
    gap = ''
    for i in range(int(columns) - len(bar) - len(str(len(population_store)))):
        gap += " "
    bar = f"{bar}{gap}{len(population_store)}"
    print(bar)

    sleep(0.01)

    if len(population_store) == 0:
        break