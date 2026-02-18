import math


def generate_cities(num_cities, random_gen, coord_min=0, coord_max=100):
    cities = []
    for _ in range(num_cities):
        x = random_gen.uniform(coord_min, coord_max)
        y = random_gen.uniform(coord_min, coord_max)
        cities.append((x, y))
    return cities


def random_tour(num_cities, random_gen):
    tour = list(range(num_cities))
    random_gen.shuffle(tour)
    return tour


def euclidean(city_a, city_b):
    return math.sqrt(
        (city_a[0] - city_b[0]) ** 2 +
        (city_a[1] - city_b[1]) ** 2
    )


def tour_cost(tour, cities):
    total = 0
    n = len(tour)

    for i in range(n - 1):
        total += euclidean(cities[tour[i]], cities[tour[i + 1]])

    # return to start
    total += euclidean(cities[tour[-1]], cities[tour[0]])
    return total


def two_opt(tour, i, k):
    return tour[:i] + list(reversed(tour[i:k + 1])) + tour[k + 1:]


def two_opt_neighbors(tour):
    n = len(tour)
    for i in range(n - 1):
        for k in range(i + 1, n):
            yield two_opt(tour, i, k)
