
def get_world_adj_dict():
    """
        This function loads in FullBoard.csv and builds a adjacency List. Returns a dictionary where the keys are the territory strings and the values are a list of tuples (column index, Territory String)
    """
    import pandas as pd
    import random
    board_df = pd.read_excel('world.xlsx')
    board_al = {}
    for col_index, column in enumerate(board_df.columns):
        board_al[column] = []
        for row_index, row in enumerate(board_df[column]):
            if row == 1:
                board_al[column].append((random.randint(5, 20), board_df.columns[row_index]))
    return board_al

def build_starting_world(world_ref: dict):
    from land import Territory
    import random
    world = {}
    for territory in world_ref:
        world[territory] = Territory(name=territory, cash=random.randrange(100, 10001, 1))
        for cost, neighbor in world_ref[territory]:
            Territory(name=neighbor, cash=random.randrange(100, 10001, 1)).add_connection(territory=world[territory], cost=random.randrange(2, 21, 1), road_condition=random.randrange(0,4,1))
    return world

def get_shortest_path_between_a_b(world_ref, a, b):
    import heapq
    ucs_pq=[]
    visited_nodes = []
    # Add the start node
    heapq.heappush(ucs_pq, (0,a,[a]))
    lowest_cost = 9999999999
    lowest_cost_path = []
    while len(ucs_pq) > 0:
        current_node = heapq.heappop(ucs_pq)
        current_path_cost = current_node[0]
        if current_node[1] == b:
            if current_node[0] < lowest_cost:
                lowest_cost = current_node[0]
                lowest_cost_path = current_node[2]
        elif visited_nodes.count(current_node[1]) > 0:
            pass
        else:
            visited_nodes.append(current_node[1])
            for child_node in world_ref[current_node[1]]:
                if visited_nodes.count(child_node[1]) == 0:
                    path = current_node[2].copy()
                    path.append(child_node[1])
                    heapq.heappush(ucs_pq, (current_path_cost + child_node[0], child_node[1], path))
    return ["No path found"] if len(lowest_cost_path) == 0 else lowest_cost_path

def get_path_A_B(world_ref: dict, a: str, b: str):
    """ Shortest path algorithm"""
    path = get_shortest_path_between_a_b(world_ref, a, b)
    moves = []
    total = 0
    step = 0
    while step < len(path):
        if step == 0:
            previous_step = path[step]
        else:
            total += get_step_cost_a_b(world_ref, (previous_step, path[step]))
            moves.append((previous_step, path[step]))
            previous_step = path[step]
        step+=1
    return (total, moves)

def get_step_cost_a_b(world_ref: dict, step):
    distance = 0
    for cost, neighbor in world_ref[step[0]]:
        if neighbor == step[1]:
            distance = cost
            break
    return distance
