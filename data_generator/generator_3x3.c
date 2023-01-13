#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "generator.h"

#define STATES_3x3_LIMIT 20000

int states_number;

/**
 * Validates if specific board state is possible to be reached in Tic-Tac-Toe game.
 * @param state Specific state to validate.
 * @returns Information if given state is valid or not (1 - is valid, 0 - invalid).
 */
int is_valid_state(grid_state_t* state)
{
    int x_fields = 0, o_fields = 0;

    // count 'X' and 'O' player fields
    for (int i = 0; i < state -> size * state -> size; i++) {
        if (state -> content[i] == 1) {
            x_fields++;
        }
        else if (state -> content[i] == 2) {
            o_fields++;
        }
    }

    // assign free fields number
    state -> free_fields = state -> size * state -> size - x_fields - o_fields;

    // if one player is ahead more than 1 move it's board error
    if (x_fields - o_fields > 1 || o_fields - x_fields > 1) {
        return 0;
    }

    // vectors initialization for checking game result
    int* rows_sums = malloc(sizeof(int) * state -> size);
    int* columns_sums = malloc(sizeof(int) * state -> size);
    int* diagonal_sums = malloc(sizeof(int) * 2);
    diagonal_sums[0] = 0;
    diagonal_sums[1] = 0;

    for (int i = 0; i < state -> size; i++) {
        rows_sums[i] = 0;
        columns_sums[i] = 0;
    }

    // processing given grid
    for (int row = 0; row < state -> size; row++) {
        for (int column = 0; column < state -> size; column++) {
            // field is marked by 'X' player (+1 for each field taken by that player)
            if (state -> content[row * state -> size + column] == 1) {
                rows_sums[row]++;
                columns_sums[column]++;

                if (row == column) {
                    diagonal_sums[0]++;
                }
                if (column == state -> size - row - 1) {
                    diagonal_sums[1]++;
                }
            }
            // field is marked by 'O' player (-1 for each field taken by that player)
            else if (state -> content[row * state -> size + column] == 2) {
                rows_sums[row]--;
                columns_sums[column]--;

                if (row == column) {
                    diagonal_sums[0]--;
                }
                if (column == state -> size - row - 1) {
                    diagonal_sums[1]--;
                }
            }
        }
    }

    // check if both players wins in this state => it's invalid
    int x_won = 0, o_won = 0;
    for (int i = 0; i < state -> size; i++) {
        if (rows_sums[i] == state -> size || columns_sums[i] == state -> size || diagonal_sums[0] == state -> size || diagonal_sums[1] == state -> size) {
            x_won = 1;
        }
        else if (rows_sums[i] == (-1) * (state -> size) || columns_sums[i] == (-1) * (state -> size) || diagonal_sums[0] == (-1) * (state -> size) || diagonal_sums[1] == (-1) * (state -> size) ) {
            o_won = 1;
        }
    }

    free(rows_sums);
    free(columns_sums);
    free(diagonal_sums);

    if (x_won && o_won) {
        return 0;
    }

    return 1;
}

/**
 * Checks what game result is.
 * @param state Board state that is being checked.
 * @returns Game result for specific board state. 1 if player 'X' won, 2 if player 'O' won, 0 if board is in draw state.
 */
int get_game_result(grid_state_t* state)
{
    // vectors initialization for checking game result
    int* rows_sums = malloc(sizeof(int) * state -> size);
    int* columns_sums = malloc(sizeof(int) * state -> size);
    int* diagonal_sums = malloc(sizeof(int) * 2);
    diagonal_sums[0] = 0;
    diagonal_sums[1] = 0;

    for (int i = 0; i < state -> size; i++) {
        rows_sums[i] = 0;
        columns_sums[i] = 0;
    }

    // processing given grid
    for (int row = 0; row < state -> size; row++) {
        for (int column = 0; column < state -> size; column++) {
            // field is marked by 'X' player (+1 for each field taken by that player)
            if (state -> content[row * state -> size + column] == 1) {
                rows_sums[row]++;
                columns_sums[column]++;

                if (row == column) {
                    diagonal_sums[0]++;
                }
                if (column == state -> size - row - 1) {
                    diagonal_sums[1]++;
                }
            }
            // field is marked by 'O' player (-1 for each field taken by that player)
            else if (state -> content[row * state -> size + column] == 2) {
                rows_sums[row]--;
                columns_sums[column]--;

                if (row == column) {
                    diagonal_sums[0]--;
                }
                if (column == state -> size - row - 1) {
                    diagonal_sums[1]--;
                }
            }
        }
    }

    // extracting game result due to received data
    int game_result = 0;
    for (int i = 0; i < state -> size; i++) {
        if (rows_sums[i] == state -> size || columns_sums[i] == state -> size || diagonal_sums[0] == state -> size || diagonal_sums[1] == state -> size) {
            game_result = 1;
        }
        else if (rows_sums[i] == (-1) * (state -> size) || columns_sums[i] == (-1) * (state -> size) || diagonal_sums[0] == (-1) * (state -> size) || diagonal_sums[1] == (-1) * (state -> size) ) {
            game_result = 2;
        }
    }

    free(rows_sums);
    free(columns_sums);
    free(diagonal_sums);

    return game_result;
}

/**
 * Generates list of all possible states that can be reached while tic-tac-toe game.
 * @returns Vector of pointers to generated grid states.
 */
grid_state_t** get_board_states()
{
    grid_state_t** possible_states = malloc(sizeof(grid_state_t*) * STATES_3x3_LIMIT);
    states_number = 0;

    // generate states and get only valid ones
    for (int a = 0; a < 3; a++) {
        for (int b = 0; b < 3; b++) {
            for (int c = 0; c < 3; c++) {

                for (int d = 0; d < 3; d++) {
                    for (int e = 0; e < 3; e++) {
                        for (int f = 0; f < 3; f++) {

                            for (int g = 0; g < 3; g++) {
                                for (int h = 0; h < 3; h++) {
                                    for (int i = 0; i < 3; i++) {
                                        // create new state
                                        grid_state_t* state = malloc(sizeof(grid_state_t));
                                        
                                        state -> x_wins = 0;
                                        state -> o_wins = 0;
                                        state -> draws = 0;

                                        state -> content = malloc(sizeof(int) * 9);
                                        state -> size = 3;

                                        // assign state content
                                        state -> content[0] = a;
                                        state -> content[1] = b;
                                        state -> content[2] = c;
                                        state -> content[3] = d;
                                        state -> content[4] = e;
                                        state -> content[5] = f;
                                        state -> content[6] = g;
                                        state -> content[7] = h;
                                        state -> content[8] = i;

                                        // check if state is valid
                                        int is_valid = is_valid_state(state);

                                        // if state is valid => take it
                                        if (is_valid) {
                                            int game_result = get_game_result(state);
                                            // check if this is endgame state
                                            int is_endgame_state = (game_result != 0 || state -> free_fields == 0);
                                            if (is_endgame_state) {
                                                switch (game_result) {
                                                    case 0:
                                                        state -> draws++;
                                                        break;
                                                    case 1:
                                                        state -> x_wins++;
                                                        break;
                                                    case 2:
                                                        state -> o_wins++;
                                                        break;
                                                }
                                            }

                                            // add state to list
                                            possible_states[states_number++] = state;
                                        }
                                        else { // if state is not valid => remove it
                                            free(state -> content);
                                            free(state);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return possible_states;
}

/**
 * Releases memory just before program ending.
 * @param data Vector of pointers that we want to destroy.
 */
void release_memory(grid_state_t** data)
{
    // free all states data
    for (int i = 0; i < states_number; i++) {
        free(data[i] -> content);
        free(data[i]);
    }
    // free memory of vector
    free(data);
}

/**
 * Checks whether specific vector of integer contains given element.
 * @param vector List of integers to filter.
 * @param element Number that should be verified with provided vector.
 * @param vector_size Number of elements in vector.
 * @returns Boolean value whether vector contains provided element or not (1 means that it contains, 0 - it doesn't).
 */
int contains_element(int* vector, int element, int vector_size)
{
    for (int i = 0; i < vector_size; i++) {
        if (vector[i] == element)
            return 1;
    }
    return 0;
}

/**
 * Process generated board states.
 * @param states Vector of pointers to generated board states.
 * @returns Modified vector of pointers to generated board states (with all endgame results).
 */
grid_state_t** process_states(grid_state_t** states)
{
    int* endgame_states_indices = malloc(sizeof(int) * STATES_3x3_LIMIT);
    int endgame_states_number = 0;

    // filter endgame states indices
    for (int i = 0; i < states_number; i++) {
        // if any value (draws, x_wins, o_wins) is greater than 0 => it's endgame state
        if (states[i] -> draws > 0 || states[i] -> x_wins > 0 || states[i] -> o_wins > 0) {
            endgame_states_indices[endgame_states_number++] = i;
        }
    }

    // process rest board states
    for (int i = 0; i < states_number; i++) {
        int is_endgame_state = contains_element(endgame_states_indices, i, endgame_states_number);

        // if it's not endgame state
        if (!is_endgame_state) {

            // find probabilities for specific common (not endgame) state
            for (int j = 0; j < endgame_states_number; j++) {
                // find number of matching fields
                int matching_fields = 0;
                for (int k = 0; k < 9; k++) {
                    if (states[i] -> content[k] != 0 && states[ endgame_states_indices[j] ] -> content[k] == states[i] -> content[k]) {
                        matching_fields++;
                    }
                }

                // possible to reach endgame state
                if (matching_fields == 9 - states[i] -> free_fields) {
                    if (states[ endgame_states_indices[j] ] -> x_wins == 1) {
                        states[i] -> x_wins++;
                    }
                    else if (states[ endgame_states_indices[j] ] -> o_wins == 1) {
                        states[i] -> o_wins++;
                    }
                    else if (states[ endgame_states_indices[j] ] -> draws == 1) {
                        states[i] -> draws++;
                    }
                }
            }
        }
    }

    free(endgame_states_indices);
    return states;
}

/**
 * Prints generated board states to specific file determined by provided filename.
 * @param states Vector of pointers to processed board states.
 * @param filename Name of file where all generated data will be stored.
 */
void save_to_file(grid_state_t** states, char* filename)
{
    // open output file
    FILE* output = fopen(filename, "w");

    // print all states data to file
    for (int i = 0; i < states_number; i++) {
        // calculating game ending probabilities
        double draw_prob = ((double) states[i] -> draws) / (double) (states[i] -> x_wins + states[i] -> o_wins + states[i] -> draws);
        double x_win_prob = ((double) states[i] -> x_wins) / (double) (states[i] -> x_wins + states[i] -> o_wins + states[i] -> draws);
        double o_win_prob = ((double) states[i] -> o_wins) / (double) (states[i] -> x_wins + states[i] -> o_wins + states[i] -> draws);

        fprintf(output, "(");
        for (int j = 0; j < states[i] -> size * states[i] -> size; j++) {
            fprintf(output, "%d, ", states[i] -> content[j]);
        }
        fprintf(output, ") -> (%.4lf, %.4lf, %.4lf)\n", draw_prob, x_win_prob, o_win_prob);
    }

    // close output file
    fclose(output);
}

/**
 * Checks if user wants to get help about generator or not. If so, then proper message is printed and whole program exits.
 * @param argc Number of arguments provided while running program.
 * @param argv Vector of program start arguments.
 */
void handle_help(int argc, char** argv)
{
    for (int i = 0; i < argc; i++) {
        if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            printf("In order to use this generator you need to run command presented below\n'./<compiled program name> <name of file with results>'\nEx. './generator3x3 data_3x3.dat'\nAfter that you should see file with wanted data.\n");
            exit(0);
        }
    }
}

int main(int argc, char** argv)
{
    // handle help for user
    handle_help(argc, argv);

    // handle lack of necessary argument
    if (argc != 2) {
        printf("Invalid number of arguments, there should be just one argument - name of file where prepared data should be stored\n");
        exit(0);
    }

    // get board possible states
    grid_state_t** states = get_board_states();

    // find endgame probabilities for generated possible board states
    states = process_states(states);

    // print the to file
    save_to_file(states, argv[1]);

    // release memory 
    release_memory(states);
    return 0;
}