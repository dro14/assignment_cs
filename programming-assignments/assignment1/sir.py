'''
Epidemic modelling


21SE099 - Anvarova Sarvinoz

Functions for running a simple epidemiological simulation
'''

import random
import click

# This seed should be used for debugging purposes only!  Do not refer
# to it in your code.
TEST_SEED = 20170217

def count_infected(city):
    num_of_infected = 0
    for i in city:
        if (i[0] != 'S' and i[0] != 'R' and i[0] != 'V'):
            num_of_infected += 1
    return num_of_infected


def has_an_infected_neighbor(city, position):
    p = position
    is_infected = False
    if (len(city) > 1):
        if (p != 0 and p != len(city) - 1):
            if ((city[p-1] != 'S' and city[p-1] != 'R' and city[p-1] != 'V') or (city[p+1] != 'S' and city[p+1] != 'R' and city[p+1] != 'V')):
                is_infected = True
        elif (p == 0):
            if (city[p+1] != 'S' and city[p+1] != 'R' and city[p+1] != 'V'):
                is_infected = True
        elif (p == len(city) - 1):
            if (city[p-1] != 'S' and city[p-1] != 'R' and city[p-1] != 'V'):
                is_infected = True
    return is_infected


def advance_person_at_position(city, position, days_contagious):
    p = position
    s = city[p]
    if (s[0] == "I"):
        x = int(s[1:])
        if (x + 1 < days_contagious):
            s = "I" + str(x + 1)
        else:
            s = "R"
    elif (s == "S" and has_an_infected_neighbor(city, position)):
        s = "I0"    
    return s


def simulate_one_day(starting_city, days_contagious):
    city = starting_city[:]
    for i in range(len(starting_city)):
        city[i] = advance_person_at_position(starting_city, i, days_contagious)    
    return city


def run_simulation(starting_city, days_contagious,
                   random_seed=None, vaccine_effectiveness=0.0):
    num_of_days = 0
    city = starting_city[:]
    random.seed(random_seed)
    for i, elem in enumerate(city):
        if (elem == 'S'):
            if (random.random() < vaccine_effectiveness):
                city[i] = 'V'
    while (count_infected(city) > 0):
        city = simulate_one_day(city, days_contagious)
        num_of_days += 1
    return (city, num_of_days)


def vaccinate_city(starting_city, vaccine_effectiveness):
    city = starting_city[:]
    for i in range(len(city)):
        if (city[i] == 'S'):
            if (random.random() < vaccine_effectiveness):
                city[i] = 'V'             
    return city


def calc_avg_days_to_zero_infections(
        starting_city, days_contagious,
        random_seed, vaccine_effectiveness,
        num_trials):
    
    sum_of_days = 0
    for i in range(num_trials):
        tupl = run_simulation(starting_city, days_contagious, random_seed, vaccine_effectiveness)
        sum_of_days += tupl[1]
        random_seed += 1
    average_days = sum_of_days/num_trials
    return average_days


################ Do not change the code below this line #######################


@click.command()
@click.argument("city", type=str)
@click.option("--days-contagious", default=2, type=int)
@click.option("--random_seed", default=None, type=int)
@click.option("--vaccine-effectiveness", default=0.0, type=float)
@click.option("--num-trials", default=1, type=int)
@click.option("--task-type", default="single",
              type=click.Choice(['single', 'average']))
def cmd(city, days_contagious, random_seed, vaccine_effectiveness,
        num_trials, task_type):
    '''
    Process the command-line arguments and do the work.
    '''

    # Convert the city string into a city list.
    city = [p.strip() for p in city.split(",")]
    emsg = ("Error: people in the city must be susceptible ('S'),"
            " recovered ('R'), or infected ('Ix', where *x* is an integer")
    for p in city:
        if p[0] == "I":
            try:
                _ = int(p[1])
            except ValueError:
                print(emsg)
                return -1
        elif p not in {"S", "R"}:
            print(emsg)
            return -1

    if task_type == "single":
        print("Running one simulation...")
        final_city, num_days_simulated = run_simulation(
            city, days_contagious, random_seed, vaccine_effectiveness)
        print("Final city:", final_city)
        print("Days simulated:", num_days_simulated)
    else:
        print("Running multiple trials...")
        avg_days = calc_avg_days_to_zero_infections(
            city, days_contagious, random_seed, vaccine_effectiveness,
            num_trials)
        msg = ("Over {} trial(s), on average, it took {:3.1f} days for the "
               "number of infections to reach zero")
        print(msg.format(num_trials, avg_days))

    return 0


if __name__ == "__main__":
    cmd()  # pylint: disable=no-value-for-parameter
