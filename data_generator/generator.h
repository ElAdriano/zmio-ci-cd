#ifndef GENERATOR_H_INCLUDED
#define GENERATOR_H_INCLUDED

typedef struct grid_state {
    int* content;
    int size;
    int free_fields;

    int x_wins;
    int o_wins;
    int draws;
} grid_state_t;

typedef struct game_simulation {
    int** grid_states;
    int turns;
    int result;
} game_simulation_t;

int is_valid_state(grid_state_t* state);
int get_game_result(grid_state_t* state);

#endif