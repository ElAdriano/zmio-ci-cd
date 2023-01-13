/**
 * Min-Max AI (for tic-tac-toe game) module functions header file
 * Author: Adrian Bączek
 * License: MIT
 */

#ifndef MINMAX_H_INCLUDED
#define MINMAX_H_INCLUDED

// min-max tree node struct
typedef struct grid {
    int size;
    int* content;
    struct grid* parent;
    struct grid** children;
    int children_num;
    int game_result;
    int end_game_tree_depth;
} grid_t;

// min-max algorithm functions
grid_t* create_min_max_tree_node(grid_t* parent);
void get_result_from_children(grid_t* node, int root_player_mark, int current_player_mark);
void minmax_analysis(grid_t* start_node, int root_player_mark, int current_player_mark, int tree_depth_limit);
int get_optimal_move(grid_t* root);
int make_minmax_move(int* grid, int grid_size, int root_player_mark, int processing_depth_limit);

int* get_available_fields(int* grid, int size);
int get_available_fields_number(int* grid, int size);
int get_game_result(int* grid, int size, int decision_player);

#endif