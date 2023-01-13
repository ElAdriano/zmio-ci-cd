/**
 * Min-Max AI (for tic-tac-toe game) module functions source file
 * Author: Adrian Bączek
 * License: MIT
 */

#include "minmax.h"
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <time.h>

// additional functions

/**
 * Finds all sequences of fields that make tic-tac-toe game ended.
 * @param grid_size Size of game board.
 * @returns 2D list of ending game fields sequences.
 */
int** get_tic_tac_toe_endgame_sequences(int grid_size)
{
    // preparing memory for endgame sequences
    int** sequences = malloc(sizeof(int*) * (2 * grid_size + 2));
    for (int i = 0; i < 2 * grid_size + 2; i++) {
        sequences[i] = malloc(sizeof(int) * grid_size);
    }

    // finding all endgame sequences
    for (int row = 0; row < grid_size; row++) {
        for (int column = 0; column < grid_size; column++) {
            sequences[row][column] = row * grid_size + column; // endgame sequences in row assignment
            sequences[row + grid_size][column] = column * grid_size + row; // endgame sequences in column assignment

            // endgame sequences for diagonals
            if (row == column) {
                sequences[2 * grid_size][row] = row * grid_size + column;
            }
            if (row == grid_size - column - 1) {
                sequences[2 * grid_size + 1][row] = row * grid_size + column;
            }
        }
    }

    return sequences;
}

/**
 * Finds the most probable game end.
 * @param node Min-Max tree node when whole tree is not analysed.
 * @param root_player_mark Tree root player identifier (1 for 'X' player, 2 for 'O' player).
 * @param current_moving_player Current moving player in the game (1 for 'X' player, 2 for 'O' player).
 * @returns Most probable endgame state (1 if root player wins, 0 if game ends with tie, -1 for root player's loss).
 */
void assign_possible_endgame_result(grid_t* node, int root_player_mark, int current_moving_player)
{
    // stats variables
    int possible_wins = 0, possible_draws = 0, possible_defeats = 0;

    // get endgame sequences to use them in analysis & finding opponent mark on grid
    int** endgame_sequences = get_tic_tac_toe_endgame_sequences(node -> size);
    int opponent_mark = root_player_mark == 1 ? 2 : 1;

    // vectors initialization for endgame sequences (moves to game end and possible game result) 
    int* endgame_moves = malloc(sizeof(int) * (2 * node -> size + 2));
    int* game_results = malloc(sizeof(int) * (2 * node -> size + 2));

    int free_fields_number = 0, x_player_fields_taken = 0, o_player_fields_taken = 0;
    for (int i = 0; i < 2 * node -> size + 2; i++) {
        // fetch currently considered sequence and reset sequence fields
        int* sequence = endgame_sequences[i];

        free_fields_number = 0;
        x_player_fields_taken = 0;
        o_player_fields_taken = 0;

        // get specific data about considered sequence at grid
        for (int p = 0; p < node -> size; p++) {
            if (node -> content[ sequence[p] ] == 0)
                free_fields_number++;
            else if (node -> content[ sequence[p] ] == 1)
                x_player_fields_taken++;
            else if (node -> content[ sequence[p] ] == 2)
                o_player_fields_taken++;
        }

        // both players signs were found in considered sequence
        if (x_player_fields_taken > 0 && o_player_fields_taken > 0) {
            game_results[i] = 0;
        }
        // in specific sequence were found only 'X' player marks
        else if (x_player_fields_taken > 0) {
            if (current_moving_player == 1) { // 'X' player is moving
                if (current_moving_player == root_player_mark) { // for root player it's still win
                    game_results[i] = 1;
                }
                else { // root is not 'X' player, so it's still loss for him
                    game_results[i] = -1;
                }
            }
            else if (current_moving_player == 2) { // 'O' player is moving
                game_results[i] = 0;
            }
        }
        // in specific sequence were found only 'O' player marks
        else if (o_player_fields_taken > 0) {
            if (current_moving_player == 1) { // 'X' player is moving
                game_results[i] = 0;
            }
            else if (current_moving_player == 2) { // 'O' player is moving
                if (current_moving_player == root_player_mark) { // for 'O' player as root it's still win
                    game_results[i] = 1;
                }
                else { // when opponent is 'O' player and only his marks were found in sequence => it's still win for him
                    game_results[i] = -1;
                }
            }
        }
        else if (x_player_fields_taken == 0 && o_player_fields_taken == 0) {
            game_results[i] = 0;
        }
        
        // assign endgame moves number
        endgame_moves[i] = node -> end_game_tree_depth + free_fields_number;
    }

    srand(time(NULL));
    int pivot_index = (rand() % (2 * node -> size + 3));
    if (current_moving_player == root_player_mark) { // maximize result
        int max_game_result = game_results[pivot_index], end_turns = endgame_moves[pivot_index];//INT_MIN, end_turns = INT_MAX;
        // process all sequences data
        for (int i = 0; i < 2 * node -> size + 2; i++) {
            // if better result was found => update global result
            if (game_results[i] > max_game_result) { // if game result is better for root player => we take it
                max_game_result = game_results[i];
                end_turns = endgame_moves[i];
            }
            else if (game_results[i] == max_game_result) { // if game result is the same as current best one => take that one which tracks to game end sooner
                if (endgame_moves[i] < end_turns) {
                    end_turns = endgame_moves[i];
                }
            }
        }
        // assign game result and end game turns
        node -> game_result = max_game_result;
        node -> end_game_tree_depth = end_turns;
    }
    else { // minimize result
        int min_game_result = game_results[pivot_index], end_turns = endgame_moves[pivot_index];
        //int min_game_result = INT_MAX, end_turns = INT_MIN;
        for (int i = 0; i < 2 * node -> size + 2; i++) {
            // if better result for enemy was found => update global result (it's more likely to happen)
            if (game_results[i] < min_game_result) { // if game result is better for opponent => take it (it's more likely to happen)
                min_game_result = game_results[i];
                end_turns = endgame_moves[i];
            }
            else if (game_results[i] == min_game_result) { // if game result is the same for opponent as current best one => take that one which may cause that game ends earlier (more likely to happen)
                if (endgame_moves[i] < end_turns) {
                    end_turns = endgame_moves[i];
                }
            }
        }

        // assign game result and end game moves number to parent
        node -> game_result = min_game_result;
        node -> end_game_tree_depth = end_turns;
    }

    // release all allocated memory
    free(game_results);
    free(endgame_moves);

    // release endgame sequences
    for (int i = 0; i < 2 * node -> size + 2; i++)
        free(endgame_sequences[i]);
    free(endgame_sequences);
}

// module functions implementation

/**
 * Finds available fields to mark at grid.
 * @param grid List of integer that represents grid state (0 - free field, 1 - X player, 2 - O player).
 * @param size Size of given grid (number element is equal size^2).
 * @returns List with available to mark fields.
 */
int* get_available_fields(int* grid, int size)
{
    // find free fields number
    int free_fields_number = 0;
    for (int i = 0; i < size * size; i++) {
        if (grid[i] == 0) {
            free_fields_number++;
        }
    }

    // getting free fields
    int* free_fields = malloc(sizeof(int) * free_fields_number);
    int p = 0;
    for (int i = 0; i < size * size; i++) {
        if (grid[i] == 0) {
            free_fields[p++] = i;
        }
    }
    return free_fields;
}

/**
 * Finds number of available fields to mark at grid.
 * @param grid List of integer that represents grid state (0 - free field, 1 - X player, 2 - O player).
 * @param size Size of given grid (number element is equal size^2).
 * @returns Number of available to mark fields.
 */
int get_available_fields_number(int* grid, int size)
{
    int free_fields_number = 0;
    for (int i = 0; i < size * size; i++) {
        if (grid[i] == 0) {
            free_fields_number++;
        }
    }
    return free_fields_number;
}

/**
 * Finds result of game for specific player.
 * @param grid List of integer that represents grid state (0 - free field, 1 - X player, 2 - O player).
 * @param size Size of given grid (number element is equal size^2).
 * @param decision_player Identifier of player that wants to know whether he won/tied/lost the game (1 - 'X' player, 2 - 'O' player).
 * @returns 0 if game ended with a tie, 1 if player decision_player won, -1 if player decision_player lost.
 */
int get_game_result(int* grid, int size, int decision_player) 
{
    // vectors initialization for checking game result
    int* rows_sums = malloc(sizeof(int) * size);
    int* columns_sums = malloc(sizeof(int) * size);
    int* diagonal_sums = malloc(sizeof(int) * 2);
    diagonal_sums[0] = 0;
    diagonal_sums[1] = 0;

    for (int i = 0; i < size; i++) {
        rows_sums[i] = 0;
        columns_sums[i] = 0;
    }

    // processing given grid
    for (int row = 0; row < size; row++) {
        for (int column = 0; column < size; column++) {
            if (grid[row * size + column] == 1) { // field is marked by 'X' player (+1 for each field taken by that player)
                rows_sums[row]++;
                columns_sums[column]++;
                if (row == column) {
                    diagonal_sums[0]++;
                }
                if(column == size - row - 1) {
                    diagonal_sums[1]++;
                }
            }
            else if (grid[row * size + column] == 2) { // field is marked by 'O' player (-1 for each field taken by that player)
                rows_sums[row]--;
                columns_sums[column]--;
                if (row == column)
                    diagonal_sums[0]--;
                if(column == size - row - 1)
                    diagonal_sums[1]--;
            }
        }
    }

    // extracting game result due to received data
    int game_result = 0;
    for (int i = 0; i < size; i++) {
        if (rows_sums[i] == size || columns_sums[i] == size || diagonal_sums[0] == size || diagonal_sums[1] == size) {
            game_result = 1;
        }
        else if (rows_sums[i] == -size || columns_sums[i] == -size || diagonal_sums[0] == -size || diagonal_sums[1] == -size) {
            game_result = 2;
        }
    }

    // casting game result to decision player's point of view (if it won (1) / lost (-1) / tied (0) )
    if (game_result == 0) {
        game_result = 0;
    }
    else if (decision_player == 1) {
        if (game_result == 1)
            game_result = 1;
        else if (game_result == 2)
            game_result = -1;
    }
    else if (decision_player == 2) {
        if (game_result == 1)
            game_result = -1;
        else if (game_result == 2)
            game_result = 1;
    }

    // deallocate used memory
    free(rows_sums);
    free(columns_sums);
    free(diagonal_sums);
    return game_result;
}

/**
 * Creates new min-max tree node in the image of specific parent node.
 * @param parent In tree structure parent for newly created node.
 * @returns New tree node pointer connected with its parent.
 */
grid_t* create_min_max_tree_node(grid_t* parent) 
{
    // allocate memory for new node
    grid_t* new_node = malloc(sizeof(grid_t));

    // assign new node data
    new_node -> parent = parent;
    new_node -> children = NULL;

    new_node -> size = parent -> size;
    new_node -> content = malloc(sizeof(int) * new_node -> size * new_node -> size);
    memcpy(new_node -> content, parent -> content, sizeof(int) * new_node -> size * new_node -> size);
    
    new_node -> end_game_tree_depth = parent -> end_game_tree_depth + 1;
    return new_node;
}

/**
 * Finds best move for specific root and destroyes node children if they are useless.
 * @param node Min-Max tree node for which we want to find best move.
 * @param root_player_mark Id that represents player for which created tree will be analysed (1 - 'X' player, 2 - 'O' player).
 * @param current_player_mark Id that represents player that currently makes move (1 - 'X' player, 2 - 'O' player).
 */
void get_result_from_children(grid_t* node, int root_player_mark, int current_player_mark)
{
    if (current_player_mark == root_player_mark) { // maximize result -> getting best move for root player
        int max_game_result = INT_MIN, end_turns = INT_MAX;
        for (int i = 0; i < node -> children_num; i++) {
            if (node -> children[i] -> game_result > max_game_result) { // if game result is better for root player => we take it
                max_game_result = node -> children[i] -> game_result;
                end_turns = node -> children[i] -> end_game_tree_depth;
            }
            else if (node -> children[i] -> game_result == max_game_result) { // if game result is the same as current best one => take that one which tracks to game end sooner
                if (node -> children[i] -> end_game_tree_depth < end_turns) {
                    end_turns = node -> children[i] -> end_game_tree_depth; 
                }
            }
        }
        // assign game result and end game moves number to parent
        node -> game_result = max_game_result;
        node -> end_game_tree_depth = end_turns;
    }
    else { // minimize enemy result -> getting best move for enemy (which is most likely to be marked)
        int min_game_result = INT_MAX, end_turns = INT_MIN;
        for (int i = 0; i < node -> children_num; i++) {
            if (node -> children[i] -> game_result < min_game_result) { // if game result is better for opponent => take it (it's more likely to happen)
                min_game_result = node -> children[i] -> game_result;
                end_turns = node -> children[i] -> end_game_tree_depth;
            }
            else if (node -> children[i] -> game_result == min_game_result) { // if game result is the same for opponent as current best one => take that one which may cause that game ends earlier (more likely to happen)
                if (node -> children[i] -> end_game_tree_depth < end_turns) {
                    end_turns = node -> children[i] -> end_game_tree_depth; 
                }
            }
        }
        // assign game result and end game moves number to parent
        node -> game_result = min_game_result;
        node -> end_game_tree_depth = end_turns;
    }

    // if currently considered node is not tree root => destroy all it's children (they're useless now, so we can free memory)
    if (node -> parent != NULL) {
        for (int i = 0; i < node -> children_num; i++) {
            free(node -> children[i] -> content);
            free(node -> children[i]);
        }
        free(node -> children);
    }
}

/**
 * Creates and analyse min-max tree starting from specific position for tic-tac-toe game. All necessary data, to choose final tic-tac-toe is held in root node and its' children.
 * @param start_node Reference to root node of a tree (node from which analysed tree will be created).
 * @param root_player_mark Id that represents player for which created tree will be analysed (1 - 'X' player, 2 - 'O' player).
 * @param current_player_mark Id that represents player that currently makes move (1 - 'X' player, 2 - 'O' player).
 * @param tree_depth_limit Tree processing depth limit (when we don't want to analyse whole tree).
 */
void minmax_analysis(grid_t* start_node, int root_player_mark, int current_player_mark, int tree_depth_limit)
{
    // find free fields number and current game grid result
    int free_fields_num = get_available_fields_number(start_node -> content, start_node -> size);
    int game_result = get_game_result(start_node -> content, start_node -> size, root_player_mark);

    // game surely ended (assign game result => only game result, tree depth is assigned automatically while creating tree leaves)
    if (game_result == 1 || game_result == -1) {
        // root player won or lost the game
        start_node -> game_result = game_result;
    }
    else if (game_result == 0) {
        // potential draw or the game has not ended yet
        if (free_fields_num > 0 && start_node -> end_game_tree_depth <= tree_depth_limit) {
            // find all available fields to mark
            int* free_fields = get_available_fields(start_node -> content, start_node -> size);

            // create memory for node children
            start_node -> children = malloc(sizeof(grid_t*) * free_fields_num);
            start_node -> children_num = free_fields_num;

            // for all free fields
            for (int i = 0; i < free_fields_num; i++) {
                // create new child
                start_node -> children[i] = create_min_max_tree_node(start_node);
                start_node -> children[i] -> content[ free_fields[i] ] = current_player_mark;

                // recursively analyse tree starting from newly created node
                if (current_player_mark == 1) {
                    minmax_analysis(start_node -> children[i], root_player_mark, 2, tree_depth_limit);
                }
                else if (current_player_mark == 2) {
                    minmax_analysis(start_node -> children[i], root_player_mark, 1, tree_depth_limit);
                }
            }

            // deallocate free fields list => all free fields were analysed
            free(free_fields);
            // get move from children, after that free them 
            get_result_from_children(start_node, root_player_mark, current_player_mark);
        }
        else {
            if (free_fields_num == 0) {
                // game_result = 0 and no available moves -> game ended with a tie, so we need to propagate result to the parent
                start_node -> game_result = game_result;
            }
            else {
                // game has not ended yet & we have to foresee game result according to win/draw/loss probability
                assign_possible_endgame_result(start_node, root_player_mark, current_player_mark);
            }
        }
    }
}

/**
 * Finds best tic-tac-toe move for min-max tree root.
 * @param root Min-Max tree root (connected with its children which store data from min-max analysis).
 * @returns Best move for current tic tac toe game turn. 
 */
int get_optimal_move(grid_t* root) 
{
    // find best move state that we can switch to
    grid_t* optimal_move = NULL;
    for(int i = 0; i < root -> children_num; i++) {
        if (root -> children[i] -> game_result == root -> game_result && root -> children[i] -> end_game_tree_depth == root -> end_game_tree_depth) {
            optimal_move = root -> children[i];
            break;
        }
    }

    // find move that differs root grid state from new grid state
    int final_move = -1;
    for (int i = 0; i < root -> size * root -> size; i++) {
        if (root -> content[i] != optimal_move -> content[i]) {
            final_move = i;
            break;
        }
    }

    // deallocate useless root children and root
    for(int i = 0; i < root -> children_num; i++) {
        free(root -> children[i] -> content);
        free(root -> children[i]);
    }
    free(root -> children);
    free(root -> content);
    free(root);
    return final_move;
} 

/**
 * Makes Min-Max algorithm move in tic-tac-toe game.
 * @param grid Grid state for all calculations to be based on.
 * @param grid_size Size of grid.
 * @param root_player_mark Player sign for whom calculated is optimal move.
 * @param processing_depth_limit Tree processing depth limit.
 * @returns Selected by Min-Max algorithm optimal move for root player.
 */
int make_minmax_move(int* grid, int grid_size, int root_player_mark, int processing_depth_limit)
{
    // create min-max tree root
    grid_t* tree_root = malloc(sizeof(grid_t));
    tree_root -> parent = NULL;
    tree_root -> content = malloc(sizeof(int) * grid_size * grid_size);
    memcpy(tree_root -> content, grid, grid_size * grid_size * sizeof(int));
    tree_root -> children = NULL;
    tree_root -> size = grid_size;
    tree_root -> end_game_tree_depth = 0;

    // dynamically create and analyse min-max tree
    minmax_analysis(tree_root, root_player_mark, root_player_mark, processing_depth_limit);

    // extract best move from tree root children
    int ai_move = get_optimal_move(tree_root);
    return ai_move;
}
