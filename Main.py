import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Arm.Bernoulli import BernoulliArm as Bernoulli
from Arm.Normal import NormalArm as Normal
from Thompson.ThompsonSampler import ThompsonSampler as ts
from Model.Model import Model


def compute_optimal(arms):
    return max([a.mu for a in arms])

def createArms():

    a1 = Normal(np.random.randint(-2,3), np.random.randint(1,4), 0)
    a2 = Normal(np.random.randint(-2,3), np.random.randint(1,4), 1)
    a3 = Normal(np.random.randint(-2,3), np.random.randint(1,4), 2)
    a4 = Normal(np.random.randint(-2,3), np.random.randint(1,4), 3)
    a5 = Normal(np.random.randint(-2,3), np.random.randint(1,4), 4)

    return [a1, a2, a3, a4, a5]

if __name__ =="__main__":

    f_random = lambda x: np.random.randint(-5,6)
    f = lambda x: x**5 + 3*x**3 + x - 1

    model = Model()

    E = []
    res = []
    means = []
    mus = []
    avg_mus = []
    mus_chosen = []
    avg_mus_chosen = []
    optimals = []
    optimals_total = []
    totals = []
    choices = []
    sampler = ts()
    
    
    for itr in range(1000):
        chosen = 0
        arms = createArms()
        n_arms = len(arms)

        mus.append(float(sum([a.mu for a in arms]))/len(arms))
        
        nE = len(E)
        E_prime = []
        
        #sample from experience set E and choose best arm from estimated probabilities
        if nE > 0:
            sample = sampler.sample(E, E_prime, nE)
            states = sample[0]
            rewards = sample[1]
            actions = sample[2]

            curr_model = model.create_model([[f(s) for s in state] for state in states], actions, rewards)
            predictions = model.predict(curr_model, [a.mu for a in arms], f)

            predictions_list = sorted(predictions.iteritems(), key=lambda (k,v): (v,k))
            chosen = predictions_list[-1][0]
            print 'CHOSEN: ' + str((chosen, predictions[chosen]))
        else:
            chosen = np.random.randint(0,5)

        chosen_arm = arms[chosen]
        reward = chosen_arm.select()
        print 'REWARD WAS: ' + str(reward)
        E.append([chosen, reward, [a.mu for a in arms]])
        res.append(reward)
        mus_chosen.append(chosen_arm.mu)
        print 'MU WAS: ' + str(mus_chosen[-1])
        avg_mus_chosen.append(float(sum(mus_chosen))/len(mus_chosen))
        totals.append(sum(res))
        means.append(float(sum(res))/len(res))
        avg_mus.append(float(sum(mus))/len(mus))
        optimals.append(compute_optimal(arms))
        optimals_total.append(sum(optimals))

    print
    print 'AVG MU: ' + str(float(sum(mus))/len(mus))
    print 'AVG MU CHOSEN: ' + str(avg_mus_chosen[-1])
    print 'AVG REWARD: ' + str(means[-1])
    print 'TOTAL REWARD: ' + str(sum(res))

    plt.plot(means, label="mean reward")
    plt.plot(avg_mus_chosen, label="avg mu chosen")
    plt.plot(avg_mus, label="avg mu")
    plt.legend(bbox_to_anchor=(0.5, 1), loc=1)
    plt.show()
    
    plt.plot(totals, label="total reward")
    plt.plot(optimals_total, label="total optimal")
    plt.show()

    plt.plot([optimals_total[x] - totals[x] for x in range(len(totals))], label='regret')
    plt.show()
            
