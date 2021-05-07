# Week 5 - Path Planning & the A* Algorithm

## Assignment

You will complete the implementation of a simple path planning algorithm based on the dynamic programming technique demonstrated in `policy.py`. A template code is given by `assignment.py`.

The assignmemt extends `policy.py` in two aspects:

* State space: since we now consider not only the position of the vehicle but also its orientation, the state is now represented in 3D instead of 2D.
* Cost function: we define different cost for different actions. They are:
	- Turn right and move forward
	- Move forward
	- Turn left and move forward

This example is intended to illustrate the algorithm's capability of generating an alternative (detouring) path when left turns are penalized by a higher cost than the other two possible actions. When run with the settings defined in `assignment.py` without modification, a successful implementation shall generate the following output,

"""
[[' ', ' ', ' ', 'R', '#', 'R'],
 [' ', ' ', ' ', '#', ' ', '#'],
 ['*', '#', '#', '#', '#', 'R'],
 [' ', ' ', ' ', '#', ' ', ' '],
 [' ', ' ', ' ', '#', ' ', ' ']]
"""

because of the prohibitively high cost associated with a left turn.

You are highly encouraged to experiment with different (more complex) maps and different cost settings for each type of action.

## Assignment Result

이번 과제는 동적프로그래밍을 이용하여 A star 알고리즘에서 변수 theta를 추가하여 cost에 따른 최적의 경로를 출력할 수 있도록 코드를 구성하는 것이다. 여기서 theta는 차량이 어느 방향으로 향하고 있는지 나타내는 orientation을 말한다.
먼저 TODO 1에서는 현재 위치에서 다음 위치로 갈 수 있는 모든 경우를 고려 했을 때 cost가 가장 적은 방향으로 가게 하기 위한 value 행렬을 갱신하고 이에 따른 action을 저장하는 policy행렬을 갱신하도록 했다.

"""
            elif grid[(y, x)] == 0:
                # TODO 1:
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
"""

그 다음 TODO2에서는 저장한 value와 policy를 이용하여 주어진 cost를 바탕으로 cost가 최소인 경로를 그려내도록 코드를 구성했다.
"""
    while (y,x) != goal: # 좌표가 목적지에 도달할 때까지 반복
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



        #목적지에 도달하면 * 표시하고 종료하도록 함.
        if (y,x) == goal:
            policy2D[(y,x)] = '*'
            min_value = 999

    return policy2D
"""

