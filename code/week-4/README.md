# Week 4 - Motion Model & Particle Filters

Particle Filter는 사용자가 정하는 개수 M만큼 샘플을 normal distribution을 이용하여 초기화 시킨 후, 가중치를 계산하여 계산한 가중치들 중 높은것들만 선택해서 particle set을 만듦으로써 localization을 하는 방법이다.

def update_weights : 가중치를 갱신하는 함수. 현 위치에서 sensor_range 범위 내에있는 랜드마크를 선택하고 particle이 관측한 observation을 map coordinate로 바꿔주어 association을 구한다. 그리고 구한 association을 이용하여 particle의 가중치와 particle의 association을 구한다. 
```
        for p in self.particles:
            associate = []
            for idx,m in map_landmarks.items():
                if distance(p,m) < sensor_range:
                    associate.append({
                        'id' : idx,
                        'x' : m['x'],
                        'y' : m['y']
                        
                    })
                    

            map_obs = []
            for obs in observations:
                map_obs.append({
                'x' : p['x'] + obs['x']*cos(p['t']) - obs['y']*sin(p['t']),
                'y' : p['y'] + obs['y']*sin(p['t']) + obs['y']*cos(p['t'])})
                

        
            if not associate : 
                continue
                
            near_associations = self.associate(associate, map_obs)
        
            p['w'] = 1.0
            p['assoc'] = []
            
            for i in range(len(near_associations)):
                p['w'] *= multivariate_normal([near_associations[i]['x'], near_associations[i]['y']],
                                              [[std_landmark_x, 0], [0, std_landmark_y]]).pdf([map_obs[i]['x'], map_obs[i]['y']])
                p['assoc'].append(near_associations[i]['id'])
```
def resample : low variance sampling을 이용하여 높은 가중치들만 선택하여 particle set을 구하도록 한다.
```
        set_particles = []
        M_inv = 1/len(self.particles)
        r = np.random.uniform(0,M_inv)
        c = self.particles[0]['w']
        for idx,p in enumerate(self.particles):
            U = r + idx * M_inv
            while U > c:
                if (idx + 1) < len(self.particles):
                    idx = idx + 1
                    c = c + self.particles[idx]['w']
                else:
                    break    
                    
        set_particles.append(self.particles[idx])
        self.particles = set_particles
```
---

[//]: # (Image References)
[empty-update]: ./empty-update.gif
[example]: ./example.gif

## Assignment

You will complete the implementation of a simple particle filter by writing the following two methods of `class ParticleFilter` defined in `particle_filter.py`:

* `update_weights()`: For each particle in the sample set, calculate the probability of the set of observations based on a multi-variate Gaussian distribution.
* `resample()`: Reconstruct the set of particles that capture the posterior belief distribution by drawing samples according to the weights.

To run the program (which generates a 2D plot), execute the following command:

```
$ python run.py
```

Without any modification to the code, you will see a resulting plot like the one below:

![Particle Filter without Proper Update & Resample][empty-update]

while a reasonable implementation of the above mentioned methods (assignments) will give you something like

![Particle Filter Example][example]

Carefully read comments in the two method bodies and write Python code that does the job.
