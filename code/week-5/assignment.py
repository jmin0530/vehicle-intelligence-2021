import numpy as np
import itertools

# Given map
grid = np.array([
    [1, 1, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1]
])

# List of possible actions defined in terms of changes in
# the coordinates (y, x)
forward = [
    (-1,  0),   # Up
    ( 0, -1),   # Left
    ( 1,  0),   # Down
    ( 0,  1),   # Right
]

# Three actions are defined:
# - right turn & move forward
# - straight forward
# - left turn & move forward
# Note that each action transforms the orientation along the
# forward array defined above.
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

init = (4, 3, 0)    # Representing (y, x, o), where
                    # o denotes the orientation as follows:
                    # 0: up
                    # 1: left
                    # 2: down
                    # 3: right
                    # Note that this order corresponds to forward above.
goal = (2, 0)
cost = (2, 1, 20)   # Cost for each action (right, straight, left)

# EXAMPLE OUTPUT:
# calling optimum_policy_2D with the given parameters should return
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]

def optimum_policy_2D(grid, init, goal, cost):
    # Initialize the value function with (infeasibly) high costs.
    value = np.full((4, ) + grid.shape, 999, dtype=np.int32)
    # Initialize the policy function with negative (unused) values.
    policy = np.full((4,) + grid.shape, -1, dtype=np.int32)
    # Final path policy will be in 2D, instead of 3D.
    policy2D = np.full(grid.shape, ' ')

    # Apply dynamic programming with the flag change.
    change = True
    while change:
        change = False
        # This will provide a useful iterator for the state space.
        p = itertools.product(
            range(grid.shape[0]),
            range(grid.shape[1]),
            range(len(forward))
        )
        # Compute the value function for each state and
        # update policy function accordingly.
        for y, x, t in p:
            # Mark the final state with a special value that we will
            # use in generating the final path policy.
            if (y, x) == goal and value[(t, y, x)] > 0:
                # TODO: implement code.
                value[(t,y,x)] = 0
                policy[(t,y,x)] = 999
                change = True
                
            # Try to use simple arithmetic to capture state transitions.
            elif grid[(y, x)] == 0:
                # TODO 2:
                for i in range(len(action)): # action 3가지 경우에 대한 for문 반복
                    t_next = (t+action[i]) % 4 # 다음에 차량이 향하고자 하는 방향 갱신
                    y2, x2 = y + forward[t_next][0], x + forward[t_next][1] # action 방향에 따른 다음 위치
                    if 0 <= y2 < grid.shape[0] and 0 <= x2 < grid.shape[1] and grid[(y2,x2)] == 0:
                        # 다음 위치가 grid 내에 있고 grid값이 0인 경우에는
                        # value값 갱신하고 이에따른 policy행렬에 action 방향 저장
                        v2 = value[(t_next, y2, x2)] + cost[i]
                        if v2 < value[(t,y,x)]:
                            change = True
                            value[(t,y,x)] = v2
                            policy[(t,y,x)] = action[i]
    # Now navigate through the policy table to generate a
    # sequence of actions to take to follow the optimal path.
    # TODO 3
        for i in range(4): # 4가지 방향 중에서 value가 가장 작은 cell로 가는 방향 출력하도록 함.
            if value[(i,y,x)] < minimum:
                minimum = value[(i,y,x)]
                policy2D[(y,x)] = action_name[policy[(theta,y,x)]+1] # cost가 최소가 되도록 현재위치에서의 방향 저장
                
        minimum = 999 #  minimum 초기화. 안하면 출력한 방향과 다른 방향으로 경로가 그려진다.
        

        # 이동 후 theta,y,x값 갱신
        new_theta = (theta + policy[(theta,y,x)]) % 4
        y = y + forward[new_theta][0]
        x = x + forward[new_theta][1]
        theta=new_theta
    # Return the optimum policy generated above.
    return policy2D

print(optimum_policy_2D(grid, init, goal, cost))
