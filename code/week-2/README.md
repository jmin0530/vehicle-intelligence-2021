# Week 2 - Markov Localization

1. motion model
이전 타임 스텝의 모든 위치에서의 사전(prior) 확률을 normal distribution을 이용하여 구한 i위치에서 position으로 이동할 확률을 곱하여 motion probability를 구한다.

<code>
  for i in range(map_size):
        position_prob += norm_pdf(position - i, mov ,stdev**2) * priors[i]
</code>

2. observation model


## Assignment

You will complete the implementation of a simple Markov localizer by writing the following two functions in `markov_localizer.py`:

* `motion_model()`: For each possible prior positions, calculate the probability that the vehicle will move to the position specified by `position` given as input.
* `observation_model()`: Given the `observations`, calculate the probability of this measurement being observed using `pseudo_ranges`.

The algorithm is presented and explained in class.

All the other source files (`main.py` and `helper.py`) should be left as they are.

If you correctly implement the above functions, you expect to see a plot similar to the following:

![Expected Result of Markov Localization][plot]

If you run the program (`main.py`) without any modification to the code, it will generate only the frame of the above plot because all probabilities returned by `motion_model()` are zero by default.
