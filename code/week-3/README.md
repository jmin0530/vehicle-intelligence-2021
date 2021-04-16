# Week 3 - Kalman Filters, EKF and Sensor Fusion
Extended Kalman Filter는 기존의 Kalman Filter가 선형 시스템에서만 구현이 가능한 것을 극복하기 위하여 비선형모델을 평균 근처에서 선형으로 근사시키는 방법을 이용해 비선형 모델에서도 구현할 수 있도록 하는 방법이다. 그 기울기는 곧 편미분이므로 Jacobian Matrix로 gradient를 나타내고 그 matrix를 이용하여 Kalman Filter에 적용시킨다.

코드를 구현한 후 결과 plot은 아래와 같으며 그 아래에 코드를 나타내도록 했다.
![EKF_Example](https://user-images.githubusercontent.com/72537757/115050293-90100d00-9f16-11eb-8709-820d35aba79a.png)

```
        # TODO: Implement EKF update for radar measurements
        # 1. Compute Jacobian Matrix H_j
        
        H_j = Jacobian(self.x)
        px, py, vx, vy = self.x
        
        # 2. Calculate S = H_j * P' * H_j^T + R
        S = np.dot(H_j, np.dot(self.P, H_j.T)) + self.R
        
        # 3. Calculate Kalman gain K = H_j * P' * Hj^T + R
        K = np.dot(self.P, np.dot(H_j.T, np.linalg.inv(S)))
        
        # 4. Estimate y = z - h(x')
        y = z - [sqrt(px**2 + py**2), atan2(py,px), (px*vx + py*vy)/sqrt(px**2 + py**2)]
        
        
        # 5. Normalize phi so that it is between -PI and +PI
        while y[1] > pi :
            y[1] = y[1] - 2 * pi
            
        while y[1] < -pi:
            y[1] = y[1] + 2 * pi
            
        
        # 6. Calculate new estimates
        #    x = x' + K * y
        #    P = (I - K * H_j) * P
        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(K, np.dot(H_j,self.P))
```

---

## Assignment - EFK & Sensor Fusion Example

In directory [`./EKF`](./EKF), template code is provided for a simple implementation of EKF (extended Kalman filter) with sensor fusion. Run the following command to test:

```
$ python run.py
```

The program consists of five modules:

* `run.py` is the modele you want to run. It reads the input data from a text file ([data.txt](./EKF/data.txt)) and feed them to the filter; after execution summarizes the result using a 2D plot.
* `sensor_fusion.py` processees measurements by (1) adjusting the state transition matrix according to the time elapsed since the last measuremenet, and (2) setting up the process noise covariance matrix for prediction; selectively calls updated based on the measurement type (lidar or radar).
* `kalman_filter.py` implements prediction and update algorithm for EKF. All the other parts are already written, while completing `update_ekf()` is left for assignment. See below.
* `tools.py` provides a function `Jacobian()` to calculate the Jacobian matrix needed in our filter's update algorithm.
*  `plot.py` creates a 2D plot comparing the ground truth against our estimation. The following figure illustrates an example:

![Testing of EKF with Sensor Fusion][EKF-results]

### Assignment

Complete the implementation of EKF with sensor fusion by writing the function `update_ekf()` in the module `kalman_filter`. Details are given in class and instructions are included in comments.
