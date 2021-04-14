import numpy as np
from helpers import distance
from math import pi, sqrt, exp, sin, cos
from scipy.stats import multivariate_normal


class ParticleFilter:
    def __init__(self, num_particles):
        self.initialized = False
        self.num_particles = num_particles

    # Set the number of particles.
    # Initialize all the particles to the initial position
    #   (based on esimates of x, y, theta and their uncertainties from GPS)
    #   and all weights to 1.0.
    # Add Gaussian noise to each particle.
    def initialize(self, x, y, theta, std_x, std_y, std_theta): # 각 particle의 위치, 각도, association, 가중치 초기화
        self.particles = []
        for i in range(self.num_particles):
            self.particles.append({
                'x': np.random.normal(x, std_x),
                'y': np.random.normal(y, std_y),
                't': np.random.normal(theta, std_theta),
                'w': 1.0,
                'assoc': [],
            })
        self.initialized = True

    # Add measurements to each particle and add random Gaussian noise.
    def predict(self, dt, velocity, yawrate, std_x, std_y, std_theta):
        # Be careful not to divide by zero.
        v_yr = velocity / yawrate if yawrate else 0
        yr_dt = yawrate * dt
        for p in self.particles:
            # We have to take care of very small yaw rates;
            #   apply formula for constant yaw.
            if np.fabs(yawrate) < 0.0001:
                xf = p['x'] + velocity * dt * np.cos(p['t'])
                yf = p['y'] + velocity * dt * np.sin(p['t'])
                tf = p['t']
            # Nonzero yaw rate - apply integrated formula.
            else:
                xf = p['x'] + v_yr * (np.sin(p['t'] + yr_dt) - np.sin(p['t']))
                yf = p['y'] + v_yr * (np.cos(p['t']) - np.cos(p['t'] + yr_dt))
                tf = p['t'] + yr_dt
            p['x'] = np.random.normal(xf, std_x)
            p['y'] = np.random.normal(yf, std_y)
            p['t'] = np.random.normal(tf, std_theta)

    # Find the predicted measurement that is closest to each observed
    #   measurement and assign the observed measurement to this
    #   particular landmark.
    def associate(self, predicted, observations):
        associations = []
        # For each observation, find the nearest landmark and associate it.
        #   You might want to devise and implement a more efficient algorithm.
        for o in observations:
            min_dist = -1.0
            for p in predicted:
                dist = distance(o, p)
                if min_dist < 0.0 or dist < min_dist:
                    min_dist = dist
                    min_id = p['id']
                    min_x = p['x']
                    min_y = p['y']
            association = {
                'id': min_id,
                'x': min_x,
                'y': min_y,
            }
            associations.append(association)
        # Return a list of associated landmarks that corresponds to
        #   the list of (coordinates transformed) predictions.
        return associations

    # Update the weights of each particle using a multi-variate
    #   Gaussian distribution.
#     def gauss_pdf(self,x,mu,s):
#         return (1/(s*sqrt(2*pi)))*exp(-0.5*((x-mu)/s)**2)
    
    def update_weights(self, sensor_range, std_landmark_x, std_landmark_y,
                       observations, map_landmarks):
        # 1. Select the set of landmarks that are visible
        #    (within the sensor range).
        
        for p in self.particles:
            associate = []
            for idx,m in map_landmarks.items():
                if distance(p,m) < sensor_range:
                    associate.append({
                        'id' : idx,
                        'x' : m['x'],
                        'y' : m['y']
                        
                    })
                    
        # 2. Transform each observed landmark's coordinates from the
        #    particle's coordinate system to the map's coordinates.
            map_obs = []
            for obs in observations:
                map_obs.append({
                'x' : p['x'] + obs['x']*cos(p['t']) - obs['y']*sin(p['t']),
                'y' : p['y'] + obs['y']*sin(p['t']) + obs['y']*cos(p['t'])})
                
        # 3. Associate each transformed observation to one of the
        #    predicted (selected in Step 1) landmark positions.
        #    Use self.associate() for this purpose - it receives
        #    the predicted landmarks and observations; and returns
        #    the list of landmarks by implementing the nearest-neighbour
        #    association algorithm.
        
            if not associate : 
                continue
                
            near_associations = self.associate(associate, map_obs)

            
        # 4. Calculate probability of this set of observations based on
        #    a multi-variate Gaussian distribution (two variables being
        #    the x and y positions with means from associated positions
        #    and variances from std_landmark_x and std_landmark_y).
        #    The resulting probability is the product of probabilities
        #    for all the observations.
        # 5. Update the particle's weight by the calculated probability.
        
            p['w'] = 1.0
            p['assoc'] = []
            
            for i in range(len(near_associations)):
                p['w'] *= multivariate_normal([near_associations[i]['x'], near_associations[i]['y']],
                                              [[std_landmark_x, 0], [0, std_landmark_y]]).pdf([map_obs[i]['x'], map_obs[i]['y']])
                p['assoc'].append(near_associations[i]['id'])

            
                    
        

    # Resample particles with replacement with probability proportional to
    #   their weights.
    def resample(self):
        
        # TODO: Select (possibly with duplicates) the set of particles
        #       that captures the posteior belief distribution, by
        # 1. Drawing particle samples according to their weights.
        # 2. Make a copy of the particle; otherwise the duplicate particles
        #    will not behave independently from each other - they are
        #    references to mutable objects in Python.
        # Finally, self.particles shall contain the newly drawn set of
        #   particles.
        set_particles = []
        M_inv = 1/len(self.particles)
        r = np.random.uniform(0,M_inv)
        c = self.particles[0]['w']
        for idx,p in enumerate(self.particles):
#             print(idx)
            U = r + idx * M_inv
            while U > c:
                if (idx + 1) < len(self.particles):
                    idx = idx + 1
                    c = c + self.particles[idx]['w']
                else:
                    break    
                    
        set_particles.append(self.particles[idx])
        self.particles = set_particles
        
            
            

        

    # Choose the particle with the highest weight (probability)
    def get_best_particle(self):
        highest_weight = -1.0
        for p in self.particles:
            if p['w'] > highest_weight:
                highest_weight = p['w']
                best_particle = p
        return best_particle
