# server configuration imports
from enum import Enum
from flask import Flask, request, make_response

# min-max algorithm C implementation binding imports
import ctypes
import pathlib

# neural network handling
from neural_network.networks_config import (
    network_configuration_3x3,
    network_configuration_4x4,
    network_configuration_5x5
)
from neural_network.neural_network_cls import NeuralNetworkSklearn as NeuralNetwork
# request handling
from validators.validators import TicTacToeRequestValidator


neural_network_3x3 = NeuralNetwork(network_configuration_3x3)
neural_network_4x4 = NeuralNetwork(network_configuration_4x4)
neural_network_5x5 = NeuralNetwork(network_configuration_5x5)

# load trained models from files
neural_network_3x3.load_model("./neural_network/network_3x3")
neural_network_4x4.load_model("./neural_network/network_4x4")
neural_network_5x5.load_model("./neural_network/network_5x5")


# response status enum class
class ResponseStatus(Enum):
    HTTP_200_OK = 200
    HTTP_400_BAD_REQUEST = 400
    HTTP_404_NOT_FOUND = 404
    HTTP_500_INTERNAL_SERVER_ERROR = 500

# Tree depth limits
MINMAX_3x3_TREE_PROCESSING_LIMIT = 10
MINMAX_4x4_TREE_PROCESSING_LIMIT = 5
MINMAX_5x5_TREE_PROCESSING_LIMIT = 3

server = Flask(__name__)


# common function for request handlers
def prefetch_request_data(request):
    '''
    Forms request data dictionary from received request data.
    That method is necessary, because Flask can't handle request data like Django does.
    '''

    # create returned request data structure
    request_data = {
        'moving_player': None,
        'grid': None,
        'grid_size': None
    }

    # prefetch 'grid_size'
    try:
        grid_size = request.form.get("grid_size", None)
        if grid_size is not None:
            grid_size = int(grid_size)
    except ValueError:
        grid_size = None

    # prefetch 'grid'
    grid = request.form.get("grid", None)

    # prefetch 'moving_player'
    try:
        moving_player = request.form.get("moving_player", None)
        if moving_player is not None:
            moving_player = int(moving_player)
    except ValueError:
        moving_player = None

    # assign prefetched request data
    request_data['moving_player'] = moving_player
    request_data['grid'] = grid
    request_data['grid_size'] = grid_size

    return request_data


@server.route("/tic-tac-toe/min-max", methods=["POST"])
def tic_tac_toe_min_max_request_handler():
    '''
    Handles request that is sent for '/tic-tac-toe/min-max' url.
    '''

    # get request data from incoming request
    request_data = prefetch_request_data(request)
    validator = TicTacToeRequestValidator(request_data)

    # check if received request data are correct
    validator_valid = validator.is_valid()
    if not validator_valid:
        return make_response(validator.errors, ResponseStatus.HTTP_400_BAD_REQUEST.value)

    # assign min-max algorithm to calculate next move
    minmax_libname = str(pathlib.Path().absolute()) + "/minmax/lib/minmax.so"
    minmax_lib = ctypes.CDLL(minmax_libname)

    # prepare grid state array for loaded C library
    grid_state = request_data['grid']
    grid = [0 for i in range(len(grid_state))]
    for i in range(0, len(grid_state)):
        grid[i] = int(grid_state[i])

    GridStateCls = ctypes.c_int * len(grid)
    grid = GridStateCls(*grid)

    grid_size = request_data['grid_size']
    if grid_size == 3:
        minmax_move = minmax_lib.make_minmax_move(grid, request_data['grid_size'],
                                                  request_data['moving_player'], MINMAX_3x3_TREE_PROCESSING_LIMIT)
    elif grid_size == 4:
        minmax_move = minmax_lib.make_minmax_move(grid, request_data['grid_size'],
                                                  request_data['moving_player'], MINMAX_4x4_TREE_PROCESSING_LIMIT)
    elif grid_size == 5:
        minmax_move = minmax_lib.make_minmax_move(grid, request_data['grid_size'],
                                                  request_data['moving_player'], MINMAX_5x5_TREE_PROCESSING_LIMIT)

    response = make_response({ 'move' : minmax_move }, ResponseStatus.HTTP_200_OK.value)
    return response


@server.route("/tic-tac-toe/neural-network", methods=["POST"])
def tic_tac_toe_neural_network_request_handler():
    '''
    Handles request that is sent for '/tic-tac-toe/neural-network' url.
    '''

    # get request data from incoming request
    request_data = prefetch_request_data(request)
    validator = TicTacToeRequestValidator(request_data)

    # check if received request data are correct
    validator_valid = validator.is_valid()
    if not validator_valid:
        return make_response(validator.errors, ResponseStatus.HTTP_400_BAD_REQUEST.value)

    # prepare grid state array for loaded neural network
    grid_state = request_data['grid']
    grid = []
    for i in range(0, len(grid_state)):
        grid.append(int(grid_state[i]))

    grid_size = request_data['grid_size']

    if grid_size == 3:
        nn_move = neural_network_3x3.make_move(grid, grid_size, request_data['moving_player'])
    elif grid_size == 4:
        nn_move = neural_network_4x4.make_move(grid, grid_size, request_data['moving_player'])
    elif grid_size == 5:
        nn_move = neural_network_5x5.make_move(grid, grid_size, request_data['moving_player'])

    response = make_response({ 'move': nn_move }, ResponseStatus.HTTP_200_OK.value)
    return response

if __name__ == "__main__":
    server.run(debug=False)