from sklearn.neural_network import MLPRegressor
from joblib import dump, load

class NeuralNetworkSklearn():
    _model = None
    _model_config = None

    def __init__(self, configuration):
        self._model = MLPRegressor(
            **configuration
        )
        self._model_config = configuration

    def learn(self, input_data, output_data):
        self._model.fit(input_data, output_data)

    def __fetch_available_moves(self, grid, grid_size):
        free_fields = []

        for i in range(0, grid_size * grid_size):
            if grid[i] == 0:
                free_fields.append(i)

        return free_fields

    def make_move(self, grid, grid_size, neural_network_sign):
        available_moves = self.__fetch_available_moves(grid, grid_size)

        final_move_value = 0
        final_move_index = available_moves[0]

        # predict game final status after each move
        for move in available_moves:
            grid_copy = [ grid[i] for i in range(0, grid_size * grid_size) ]
            grid_copy[move] = neural_network_sign

            # get predictions
            predictions = self._model.predict([grid_copy])
            predictions = predictions[0]

            current_move_value = max(predictions[0], predictions[neural_network_sign])
            # check if current move is better than current best one
            if current_move_value > final_move_value:
                final_move_index = move
                final_move_value = current_move_value

        return final_move_index

    def save_model(self, filename):
        dump(self._model, filename)

    def load_model(self, filename):
        try:
            self._model = load(filename) 
        except FileNotFoundError as err:
            return False
        return True
        