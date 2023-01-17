import networks_config as config

import sys
# load trained model
import pathlib
from neural_network_cls import NeuralNetworkSklearn
from random import randint
import numpy
import time
import matplotlib.pyplot as plt

allowed_sizes = [3, 4, 5]

try:
    size = int(sys.argv[1])
    if size not in allowed_sizes:
        raise Exception()
except Exception:
    exit()

type = None

types = ["games", "prob"]
if size == 3:
    type = "prob"
elif size == 4:
    type = "games"
elif size == 5:
    type = "games"

def get_configuration(size: int):
    if size == 3:
        return config.network_configuration_3x3
    elif size == 4:
        return config.network_configuration_4x4
    elif size == 5:
        return config.network_configuration_5x5
    return None

configuration = get_configuration(size)
network_sklearn = NeuralNetworkSklearn(configuration)

if pathlib.Path("./network_{size}x{size}".format(size=size)).exists():
    print("Loading neural network...")
    network_sklearn.load_model("network_{size}x{size}".format(size=size))
    print("Model loaded...")

def load_data(size: int):
    learning_dataset = {"input": [], "output": []}
    validation_dataset = {"input": [], "output": []}

    learning_dataset_file = open("../data_generator/ttt_{size}x{size}_data.dat".format(size=size), "r")
    content_lines = learning_dataset_file.read().split("\n")

    if type == "prob":
        for i in range(0, len(content_lines)):
            if content_lines[i] != "":
                line_split = content_lines[i].split("->")
                grid_state = eval(line_split[0])
                game_result = eval(line_split[1])

                tmp = []
                for k in range(0, len(grid_state)):
                    tmp.append(grid_state[k])

                learning_dataset["input"].append(tmp)
                learning_dataset["output"].append([game_result[0], game_result[1], game_result[2]])

                validation_dataset["input"].append(tmp)
                validation_dataset["output"].append([game_result[0], game_result[1], game_result[2]])

    elif type == "games":
        for i in range(0, len(content_lines)):
            if content_lines[i] != "":
                line_split = content_lines[i].split("->")
                grid_state = eval(line_split[0])
                game_result = eval(line_split[1])

                tmp = []
                for k in range(0, len(grid_state)):
                    tmp.append(grid_state[k])

                learning_dataset["input"].append(tmp)
                learning_dataset["output"].append([game_result[0], game_result[1], game_result[2]])

                validation_dataset["input"].append(tmp)
                validation_dataset["output"].append([game_result[0], game_result[1], game_result[2]])

    return (learning_dataset, validation_dataset)


if "--learn" in sys.argv:
    print("Loading learning data...")
    datasets = load_data(size)
    print("Learning data loaded...")

    learning_input_data = numpy.array(datasets[0]['input']).reshape((-1, size**2))
    learning_output_data = numpy.array(datasets[0]['output']).reshape((-1, 3))

    print("Learning network...")
    network_sklearn.learn(learning_input_data, learning_output_data)
    print("Network learnt...")

def check_game_status(grid, grid_size):
    # initiate checkers
    rows_sums = [0 for i in range(grid_size)]
    columns_sums = [0 for i in range(grid_size)]
    diagonal_sums = [0, 0]

    # process grid
    for row in range(0, grid_size):
        for column in range(0, grid_size):
            field_value = grid[row * grid_size + column]
            if field_value == 1:  # 'X' player
                rows_sums[row] += 1
                columns_sums[column] += 1
                if row == column:
                    diagonal_sums[0] += 1
                if row == grid_size - column - 1:
                    diagonal_sums[1] += 1
            elif field_value == 2:  # 'O' player
                rows_sums[row] -= 1
                columns_sums[column] -= 1
                if row == column:
                    diagonal_sums[0] -= 1
                if row == grid_size - column - 1:
                    diagonal_sums[1] -= 1

    if grid_size in rows_sums or grid_size in columns_sums or grid_size in diagonal_sums:
        return 1
    elif -grid_size in rows_sums or -grid_size in columns_sums or -grid_size in diagonal_sums:
        return 2
    else:
        return 0

def get_available_fields(grid, grid_size):
    available_fields = []
    for i in range(0, grid_size * grid_size):
        if grid[i] == 0:
            available_fields.append(i)
    return available_fields

def simulate_ttt_game_for_neural_network_against_random(network, nn_player, random_player, grid_size):
    grid = [0 for j in range(0, grid_size * grid_size)]
    turn_counter = 0
    current_player = randint(1, 2)

    # game simulation
    while turn_counter < grid_size * grid_size:
        # neural network move
        if current_player == nn_player:
            nn_move = network.make_move(grid, grid_size, nn_player)
            grid[nn_move] = nn_player
        else:  # random move
            available_moves = get_available_fields(grid, grid_size)
            random_index = randint(0, len(available_moves) - 1)
            grid[random_index] = random_player

        # if game ended, return game result
        game_status = check_game_status(grid, grid_size)
        if game_status != 0:
            return game_status

        # change player turn
        current_player = (current_player + 1) % 2
        if current_player == 0:
            current_player = 2
        # increase turn counter
        turn_counter += 1

    game_status = check_game_status(grid, grid_size)
    return game_status

def make_network_efficiency_stats(network, games_number, grid_size):
    neural_network_wins = 0
    neural_network_draws = 0
    neural_network_defeats = 0
    for i in range(0, games_number):
        nn_player = 1 if i % 2 == 1 else 2
        minmax_player = 2 if i % 2 == 1 else 1

        game_result = simulate_ttt_game_for_neural_network_against_random(network, nn_player, minmax_player, grid_size)

        if game_result == nn_player:
            neural_network_wins += 1
        elif game_result == 0:
            neural_network_draws += 1
        else:
            neural_network_defeats += 1

    print("Neural Network vs. Random stats")
    print("===============================")
    print("Wins: {wins}\nDraws: {draws}\nDefeats: {defeats}".format(
        wins=neural_network_wins,
        draws=neural_network_draws,
        defeats=neural_network_defeats
    ))

    return (neural_network_draws, neural_network_wins, neural_network_defeats)

def simulate_ttt_scikit_time(grid_size, scikit_network):
    grid = [0 for j in range(0, grid_size * grid_size)]
    turn_counter = 0
    current_player = randint(1, 2)

    moves_time = []

    # game simulation
    while turn_counter < grid_size * grid_size:
        start = time.time_ns()
        nn_move = scikit_network.make_move(grid, grid_size, current_player)
        end = time.time_ns()

        moves_time.append((turn_counter, end - start))

        grid[nn_move] = current_player

        # change player turn
        current_player = (current_player + 1) % 2
        if current_player == 0:
            current_player = 2
        # increase turn counter
        turn_counter += 1
    return moves_time

def make_network_time_stats(network, games_number, grid_size):
    average_stats = [[i, 0] for i in range(grid_size**2)]

    for i in range(0, games_number):
        time_stats = simulate_ttt_scikit_time(grid_size, network)
        for j in range(0, grid_size**2):
            average_stats[time_stats[j][0]][1] += time_stats[j][1]

    for i in range(grid_size**2):
        average_stats[i][1] /= games_number

    return average_stats

if "--learn" in sys.argv:
    print("Saving network to file...")
    network_sklearn.save_model("network_{size}x{size}".format(size=size))
    print("Network exported to file...")

# generating efficiency stats
if "--stats" in sys.argv:
    print("Preparing efficiency stats...")

    labels = list(['Remisy', 'Zwycięstwa', 'Porażki'])
    values = make_network_efficiency_stats(network_sklearn, 100, size)
    explode = (0, 0, 0)

    fig1, ax = plt.subplots(figsize=(7, 7))
    ax.pie(values, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    ax.axis('equal')
    ax.legend(labels)
    ax.set_title("Wykres kołowy skuteczności sieci neuronowej\ndla gry 'Kółko i krzyżyk' (na planszy o wymiarach \
{size}x{size})\n".format(size=size))

    print("Efficiency stats prepared...")
    plt.show()

if "--timestats" in sys.argv:
    print("Preparing time efficiency stats")

    times = make_network_time_stats(network_sklearn, 100, size)
    # Create a figure containing a single axes
    fig, ax = plt.subplots(figsize=(7, 7))
    # plot stored data
    ax.plot(
        [i for i in range(size**2)],
        [times[i][1] for i in range(size**2)],
    )

    ax.set_xlabel("Liczba wolnych pól")
    ax.set_ylabel("Średni czas określania ruchu [ns]")
    ax.set_title("Wykres czasu predykcjonowania ruchu przez sieć neuronową dla\nplanszy wym. \
{size}x{size} w zależności od liczby zaznaczonych pól\n".format(size=size))

    print("Time efficiency stats prepared...")
    plt.show()
