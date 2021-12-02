import math
import numpy as np
import scipy.stats as sps


class Monte_Carlo:
    t_interv_numb = 100  #  number of interval
    iterations = 50  #  number of different considered ways 


    def __init__(self, mu, b, Aux):
        self.mu = mu
        self.b = b
        if (Aux):
          self.extremum = np.minimum
        else:
          self.extremum = np.maximum
        self.v_get_S_sample = np.vectorize(self.get_S_sample, otypes=[object])
    

    def get_S_sample(self, So, T, K):
        delta_t = T/self.t_interv_numb
        norm_sample = sps.norm().rvs(size=(self.iterations, self.t_interv_numb))
        S_sample = So*np.exp(np.sum((self.mu-0.5*self.b**2)*delta_t + self.b*
                 (delta_t**0.5)*sps.norm().rvs(size=(self.t_interv_numb+1, self.iterations)), axis=0))
        return self.extremum(S_sample - K, 0)



    #  T, K - option expiry, strike
    #  To, Ko - compound option expiry, strike
    def get_VC(self, So, T, K, To, Ko):  #  use Monte-Carlo algorithm for calculating
        sample_o = self.get_S_sample(So, To, Ko)
        sample = self.v_get_S_sample(sample_o, T - To, K)
        return math.exp(-mu*T) * np.mean(np.mean(sample))


if __name__ == '__main__':
    print("Enter begin value of assets:")
    So = float(input())
    print("Enter mu:")
    mu = float(input())
    print("Enter b:")
    b = float(input())
    print("Enter expiry of option:")
    T = float(input())
    print("Enter strike of option:")
    K = float(input())
    print("Enter expiry of compound option:")
    To = float(input())
    print("Enter strike of compound option:")
    Ko = float(input())
    print("Aux option (min/max):")
    Aux_str = str(input())
    mc = Monte_Carlo(mu, b, Aux_str == "min")
    print(mc.get_VC(So, T, K, To, Ko))