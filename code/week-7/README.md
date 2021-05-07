# Week 7 - Hybrid A* Algorithm & Trajectory Generation

---

[//]: # (Image References)
[has-example]: ./hybrid_a_star/has_example.png
[ptg-example]: ./PTG/ptg_example.png

## Assignment: Hybrid A* Algorithm

In directory [`./hybrid_a_star`](./hybrid_a_star), a simple test program for the hybrid A* algorithm is provided. Run the following command to test:

```
$ python main.py
```

The program consists of three modules:

* `main.py` defines the map, start configuration and end configuration. It instantiates a `HybridAStar` object and calls the search method to generate a motion plan.
* `hybrid_astar.py` implements the algorithm.
* `plot.py` provides an OpenCV-based visualization for the purpose of result monitoring.

You have to implement the following sections of code for the assignment:

* Trajectory generation: in the method `HybridAStar.expand()`, a simple one-point trajectory shall be generated based on a basic bicycle model. This is going to be used in expanding 3-D grid cells in the algorithm's search operation.
* Hybrid A* search algorithm: in the method `HybridAStar.search()`, after expanding the states reachable from the current configuration, the algorithm must process each state (i.e., determine the grid cell, check its validity, close the visited cell, and record the path. You will have to write code in the `for n in next_states:` loop.
* Discretization of heading: in the method `HybridAStar.theta_to_stack_num()`, you will write code to map the vehicle's orientation (theta) to a finite set of stack indices.
* Heuristic function: in the method `HybridAStar.heuristic()`, you define a heuristic function that will be used in determining the priority of grid cells to be expanded. For instance, the distance to the goal is a reasonable estimate of each cell's cost.

You are invited to tweak various parameters including the number of stacks (heading discretization granularity) and the vehicle's velocity. It will also be interesting to adjust the grid granularity of the map. The following figure illustrates an example output of the program with the default map given in `main.py` and `NUM_THETA_CELLS = 360` while the vehicle speed is set to 0.5.

![Example Output of the Hybrid A* Test Program][has-example]

---

## Assignment result
이번 과제는 A_star 알고리즘에서 실제 차량의 motion을 고려한 Hybrid A_star 알고리즘을 구현하여 drivable parth를 생성하도록 코드를 구현하는 것이다.
하지만 hybrid A_star 알고리즘은 연속성을 보장할 수는 있어도 completeness, optimal을 보장 못한다.

TODO 1: omega 최대와 최소를 이용하여 변하는 각도 delta를 구하고 delta를 이용해 각속도를 구한다. 그리고 다음 좌표 위치와 다음 각도를 계산해내고 A_star 알고리즘에서와 마찬가지로 heuristic function을 이용하여 다음 위치까지의 거리를 계산하도록 한다.
```
def expand(self, current, goal):
        g = current['g']
        x, y, theta = current['x'], current['y'], current['t']

        # The g value of a newly expanded cell increases by 1 from the
        # previously expanded cell.
        g2 = g + 1
        next_states = []

        # Consider a discrete selection of steering angles.
        for delta_t in range(self.omega_min, self.omega_max+1, self.omega_step):

            # TODO: implement the trajectory generation based on
            # a simple bicycle model.
            # Let theta2 be the vehicle's heading (in radian)
            # between 0 and 2 * PI.
            # Check validity and then add to the next_states list.
            delta = np.pi/180.0 * delta_t
            # delta = delta_t * np.pi/180.0
            omega = self.speed / self.length * np.tan(delta)
            x2 = x + self.speed * np.cos(theta)
            y2 = y + self.speed * np.sin(theta)
            theta2 = theta + omega

            if theta2 < 0:
                theta2 += 2*np.pi
            elif theta2 > 2*np.pi:
                theta2 -= 2*np.pi 

            if 0 <= self.idx(x2)  \
              and self.idx(x2) < self.dim[1] \
              and 0 <= self.idx(y2) \
              and self.idx(y2) < self.dim[2]:
                f2 = g2 + self.heuristic(x2, y2, goal)
                current = {
              'f': f2,
              'g': g2,
              'x': x2,
              'y': y2,
              't': theta2,                
            }
                next_states.append(current)


        return next_states
```

TODO 2: theta_to_stack_num 함수는 주어진 각도 theta를 받아 theta cell의 개수에서 몇번째 인덱스인지 출력해준다.
```
 def theta_to_stack_num(self, theta):
        # TODO: implement a function that calculate the stack number
        # given theta represented in radian. Note that the calculation
        # should partition 360 degrees (2 * PI rad) into different
        # cells whose number is given by NUM_THETA_CELLS.
        angle = theta * (180/np.pi)
        interval = 360 / self.NUM_THETA_CELLS
        stack_num = angle // interval

        if stack_num == self.NUM_THETA_CELLS:
            stack_num = 0
        return int(stack_num)
```

TODO 3: search 함수는 지도인 grid, 시작위치와 목표위치를 받아서 hybrid a_star 알고리즘을 바탕으로한 breadth-search를 수행하는 함수이다. while문 안에서 현재 위치에서 cost가 가장 적은 방향으로 가도록 설정하고 다음 상태를 저장하는 과정을 반복한다. 다음 상태를 불러오기 위해 expand 함수를 이용한다.
```
def search(self, grid, start, goal):
        # Initial heading of the vehicle is given in the
        # last component of the tuple start.
        theta = start[-1]
        # Determine the cell to contain the initial state, as well as
        # the state itself.
        stack = self.theta_to_stack_num(theta)
        g = 0
        s = {
            'f': self.heuristic(start[0], start[1], goal),
            'g': g,
            'x': start[0],
            'y': start[1],
            't': theta,
        }
        self.final = s
        # Close the initial cell and record the starting state for
        # the sake of path reconstruction.
        self.closed[stack][self.idx(s['x'])][self.idx(s['y'])] = 1
        self.came_from[stack][self.idx(s['x'])][self.idx(s['y'])] = s
        total_closed = 1
        opened = [s]
        # Examine the open list, according to the order dictated by
        # the heuristic function.
        while len(opened) > 0:
            # TODO: implement prioritized breadth-first search
            # for the hybrid A* algorithm.
            opened.sort(key=lambda s : s['f'], reverse=True)
            curr = opened.pop()
            x, y = curr['x'], curr['y']
            if (self.idx(x), self.idx(y)) == goal:
                self.final = curr
                found = True
                break

            # Compute reachable new states and process each of them.
            next_states = self.expand(curr, goal)
            for n in next_states:
                x2 = self.idx(n['x'])
                y2 = self.idx(n['y'])
                stack = self.theta_to_stack_num(n['t'])
              
                if grid[x2][y2] == 0:
                    distance_x = abs(self.idx(x) - x2)
                    distance_y = abs(self.idx(y) - y2)
                    min_x = min(self.idx(x), x2)
                    min_y = min(self.idx(y), y2)
                
                    flag = True

                for dist_x in range(distance_x+1):
                    for dist_y in range(distance_y+1):
                        if grid[min_x+dist_x][min_y+dist_y] != 0:
                            flag = False
                
                if flag and self.closed[stack][x2][y2] == 0:
                    self.closed[stack][x2][y2] = 1
                    total_closed += 1
                    self.came_from[stack][x2][y2] = curr
                    opened.append(n)
        else:
            # We weren't able to find a valid path; this does not necessarily
            # mean there is no feasible trajectory to reach the goal.
            # In other words, the hybrid A* algorithm is not complete.
            found = False

        return found, total_closed
```
TODO 4: heuristic function은 단순하게 현재 위치에서 goal까지의 거리를 계산한다.
```
    def heuristic(self, x, y, goal):
        # TODO: implement a heuristic function.
        L2_distance = np.sqrt((goal[0]-x)*(goal[0]-x)
                             + (goal[1]-y)*(goal[1]-y))
        return L2_distance
```

## Plot

현재 plot자체가 안되는 오류가 발생하고 있어서 수정되면 plot결과 올리도록 하겠습니다.
```
No valid path found after 16493 expansions
: cannot connect to X server :0.0
```


