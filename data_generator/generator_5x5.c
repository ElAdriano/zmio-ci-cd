#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "generator.h"

/**
 * Finds available fields indices in game grid.
 * @param grid List of integers which represents tic-tac-toe board state.
 * @returns List of indices of available fields on board.
 */
int* get_available_fields(int* grid)
{
    // find free fields number
    int available_fields_num = 0;
    for (int i = 0; i < 25; i++) {
        if (grid[i] == 0)
            available_fields_num++;
    }

    // create available fields list
    int* available_fields = malloc(sizeof(int) * available_fields_num);
    int pointer = 0;

    // fetch available fields indices
    for (int i = 0; i < 25; i++) {
        if (grid[i] == 0)
            available_fields[pointer++] = i;
    }

    return available_fields;
}

/**
 * Fetches game result from specific board state.
 * @param grid List of integers that represents board state.
 * @param board_size Size of board.
 * @returns Integer value of game result (0 - draw, 1 - 'X' player won, 2 - 'O' player won).
 */
int get_game_result_v2(int* grid, int board_size)
{
    // vectors initialization for checking game result
    int* rows_sums = malloc(sizeof(int) * board_size);
    int* columns_sums = malloc(sizeof(int) * board_size);
    int* diagonal_sums = malloc(sizeof(int) * 2);
    diagonal_sums[0] = 0;
    diagonal_sums[1] = 0;

    for (int i = 0; i < board_size; i++) {
        rows_sums[i] = 0;
        columns_sums[i] = 0;
    }

    // processing given grid
    for (int row = 0; row < board_size; row++) {
        for (int column = 0; column < board_size; column++) {
            // field is marked by 'X' player (+1 for each field taken by that player)
            if (grid[row * board_size + column] == 1) {
                rows_sums[row]++;
                columns_sums[column]++;

                if (row == column) {
                    diagonal_sums[0]++;
                }
                if (column == board_size - row - 1) {
                    diagonal_sums[1]++;
                }
            }
            // field is marked by 'O' player (-1 for each field taken by that player)
            else if (grid[row * board_size + column] == 2) {
                rows_sums[row]--;
                columns_sums[column]--;

                if (row == column) {
                    diagonal_sums[0]--;
                }
                if (column == board_size - row - 1) {
                    diagonal_sums[1]--;
                }
            }
        }
    }

    // extracting game result due to received data
    int game_result = 0;
    for (int i = 0; i < board_size; i++) {
        if (rows_sums[i] == board_size || columns_sums[i] == board_size || diagonal_sums[0] == board_size || diagonal_sums[1] == board_size) {
            game_result = 1;
        }
        else if (rows_sums[i] == (-1) * board_size || columns_sums[i] == (-1) * board_size || diagonal_sums[0] == (-1) * board_size || diagonal_sums[1] == (-1) * board_size ) {
            game_result = 2;
        }
    }

    free(rows_sums);
    free(columns_sums);
    free(diagonal_sums);

    return game_result;
}

/**
 * Verifies whether specific board state is an endgame state or not.
 * @param grid List of integers that represents board state.
 * @param board_size Size of board.
 * @returns Boolean information whether game ended or not.
 */
int is_endgame_state(int* grid, int board_size)
{
    // vectors initialization for checking game result
    int* rows_sums = malloc(sizeof(int) * board_size);
    int* columns_sums = malloc(sizeof(int) * board_size);
    int* diagonal_sums = malloc(sizeof(int) * 2);
    diagonal_sums[0] = 0;
    diagonal_sums[1] = 0;
    int free_fields_num = 0;

    for (int i = 0; i < board_size; i++) {
        rows_sums[i] = 0;
        columns_sums[i] = 0;
    }

    // processing given grid
    for (int row = 0; row < board_size; row++) {
        for (int column = 0; column < board_size; column++) {
            // field is marked by 'X' player (+1 for each field taken by that player)
            if (grid[row * board_size + column] == 1) {
                rows_sums[row]++;
                columns_sums[column]++;

                if (row == column) {
                    diagonal_sums[0]++;
                }
                if (column == board_size - row - 1) {
                    diagonal_sums[1]++;
                }
            }
            // field is marked by 'O' player (-1 for each field taken by that player)
            else if (grid[row * board_size + column] == 2) {
                rows_sums[row]--;
                columns_sums[column]--;

                if (row == column) {
                    diagonal_sums[0]--;
                }
                if (column == board_size - row - 1) {
                    diagonal_sums[1]--;
                }
            }
            else {
                free_fields_num++;
            }
        }
    }

    // extracting game result due to received data
    int game_result = 0;
    for (int i = 0; i < board_size; i++) {
        if (rows_sums[i] == board_size || columns_sums[i] == board_size || diagonal_sums[0] == board_size || diagonal_sums[1] == board_size) {
            game_result = 1;
        }
        else if (rows_sums[i] == (-1) * board_size || columns_sums[i] == (-1) * board_size || diagonal_sums[0] == (-1) * board_size || diagonal_sums[1] == (-1) * board_size ) {
            game_result = 2;
        }
    }

    free(rows_sums);
    free(columns_sums);
    free(diagonal_sums);

    if ((game_result == 0 && free_fields_num == 0) || game_result != 0) {
        return 1;
    }
    return 0;
}

/**
 * Runs specified number of tic-tac-toe game simulations.
 * @param games_number Number of games to simulate.
 * @returns List of pointers to game_simulation_t objects.
 */
game_simulation_t** simulate_games(int games_number)
{
    int board_size = 5;

    // create vector for simulated games
    game_simulation_t** games = malloc(sizeof(game_simulation_t*) * games_number);

    // simulate specific number of games
    for (int i = 0; i < games_number; i++) {
        int max_turns = board_size * board_size, turns = 0, is_endgame = 0;

        // prepare simulation data structure
        game_simulation_t* simulation = malloc(sizeof(game_simulation_t));
        simulation -> grid_states = malloc(sizeof(int*) * max_turns);
        for (int j = 0; j < max_turns; j++)
            simulation -> grid_states[j] = malloc(sizeof(int) * board_size * board_size);

        int current_player = rand() % 2;
        if (current_player == 0)
            current_player = 2;

        // create empty grid
        int* grid = malloc(sizeof(int) * board_size * board_size);
        for (int j = 0; j < board_size * board_size; j++)
            grid[j] = 0;
        
        memcpy(simulation -> grid_states[turns], grid, sizeof(int) * board_size * board_size);
        turns++;

        // simulate game
        while (turns < max_turns && !is_endgame) {
            // get available fields
            int* available_fields = get_available_fields(grid);

            // choose which field will be marked
            int random_field = rand() % (max_turns - turns);
            int field_to_mark = available_fields[random_field];
            free(available_fields);

            // mark field
            grid[field_to_mark] = current_player;

            // copy current grid state
            memcpy(simulation -> grid_states[turns], grid, sizeof(int) * board_size * board_size);
            turns++;

            // check if current state become endgame state after player move
            is_endgame = is_endgame_state(grid, board_size);
            if (!is_endgame) {
                // change currently moving player
                current_player = (current_player + 1) % 2;
                if (current_player == 0)
                    current_player = 2;
            }
        }

        int game_result = get_game_result_v2(grid, board_size);
        simulation -> result = game_result;
        simulation -> turns = turns;

        free(grid);

        // add simulation to simulated games list
        games[i] = simulation;
    }

    return games;
}

/**
 * Prints generated data to specific file.
 * @param filename Name of file where generated data will be stored.
 * @param games Vector of pointers to generated simulations data.
 * @param games_played Number of games that were simulated.
 * @param board_size Size of board.
 */
void save_to_file(char* filename, game_simulation_t** games, int games_played, int board_size)
{
    FILE* output = fopen(filename, "w");

    for (int gameNr = 0; gameNr < games_played; gameNr++) {
        for (int turnNr = 0; turnNr < games[gameNr] -> turns; turnNr++) {
            fprintf(output, "(");
            for (int cellId = 0; cellId < board_size * board_size; cellId++) {
                fprintf(output, "%d, ", games[gameNr] -> grid_states[turnNr][cellId]);
            }

            if (games[gameNr] -> result == 0) {
                fprintf(output, ") -> (%.4lf, %.4lf, %.4lf)\n", 1.0, 0.0, 0.0);
            } 
            else if (games[gameNr] -> result == 1) {
                fprintf(output, ") -> (%.4lf, %.4lf, %.4lf)\n", 0.0, 1.0, 0.0);
            } 
            else if (games[gameNr] -> result == 2) {
                fprintf(output, ") -> (%.4lf, %.4lf, %.4lf)\n", 0.0, 0.0, 1.0);
            }
        }
        fprintf(output, "\n");
    }

    fclose(output);
}

/**
 * Releases generated games data.
 * @param games 2D list of 'game_simulation_t' type with generated data.
 * @param board_size Size of board.
 * @param games_played Number of games to simulate.
 */
void release_memory(game_simulation_t** games, int board_size, int games_played)
{
    // free all games data structures
    for (int i = 0; i < games_played; i++) {
        // free all game state changes
        for (int j = 0; j < board_size * board_size; j++) {
            free(games[i] -> grid_states[j]);
        }
        free(games[i] -> grid_states);
        free(games[i]);
    }
    // free games container
    free(games);
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
            printf("In order to use this generator you need to run command presented below\n'./<compiled program name> <number of games to simulate> <name of file with results>'\nEx. './generator5x5 1000 data_5x5.dat'\nAfter that you should see file with wanted data.\n");
            exit(0);
        }
    }
}

int main(int argc, char** argv)
{
    // initiate rand machine
    srand(time(NULL));

    // handle help for user
    handle_help(argc, argv);

    // handle lack of necessary argument
    if (argc != 3) {
        printf("Invalid number of arguments, user should provide exactly 2 arguments\n");
        exit(0);
    }

    int games_played = atoi(argv[1]);
    char* output_filename = argv[2];
    int board_size = 5;

    // prepare number of game simulations
    game_simulation_t** games = simulate_games(games_played);

    // save results to file
    save_to_file(output_filename, games, games_played, board_size);

    // free allocated memory
    release_memory(games, board_size, games_played);
    return 0;
}