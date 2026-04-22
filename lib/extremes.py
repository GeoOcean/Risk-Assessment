# basics
import sys
import os
import os.path as op

# arrays
import numpy as np

# config
import warnings
warnings.simplefilter("ignore")

colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']  

def qqplot(x, y, quantiles=100, method='nearest'):
    
    quantiles = np.linspace(start=0, stop=0.99, num=int(quantiles))        
    x_quantiles = np.quantile(x, quantiles, method=method)
    y_quantiles = np.quantile(y, quantiles, method=method)
    
    return(x_quantiles, y_quantiles)

def ACOV(f, theta, x):
    '''
    Returns asyntotyc variance matrix using Fisher Information matrix inverse
    Generalized functions, parameters and data.

    f      - function to evaluate: GEV, GUMBELL, ...
    theta  - function parameters: for GEV (shape, location, scale)
    x      - data used for function evaluation

    Second derivative evaluation - variance and covariance
    dxx = (f(x+dt_x) - 2f(x) + f(x-dt_x)) / (dt_x**2)
    dxy = (f(x,y) - f(x-dt_x,y) - f(x,y-dt_y) + f(x-dt_x, u-dt_y)) / (dt_x*dt_y)
    '''

    # parameters differential
    pm = 0.00001
    params = np.asarray(theta)
    dt_p = pm * params

    # Fisher information matrix holder 
    ss = len(params)
    FI = np.ones((ss,ss)) * np.nan

    if np.isinf(f(theta, x)):
        print ('ACOV error: nLogL = Inf. {0}'.format(theta))
        return np.ones((ss,ss))*0.0001

    # variance and covariance
    for i in range(ss):

        # diferential parameter FI evaluation
        p1 = np.asarray(theta); p1[i] = p1[i] + dt_p[i]
        p2 = np.asarray(theta); p2[i] = p2[i] - dt_p[i]

        # variance
        FI[i,i] = (f(tuple(p1), x) - 2*f(theta,x) + f(tuple(p2), x))/(dt_p[i]**2)

        for j in range(i+1,ss):

            # diferential parameter FI evaluation
            p1 = np.asarray(theta); p1[i] = p1[i] - dt_p[i]
            p2 = np.asarray(theta); p2[j] = p2[j] - dt_p[j]
            p3 = np.asarray(theta); p3[i] = p3[i] - dt_p[i]; p3[j] = p3[j] - dt_p[j]

            # covariance
            cov = (f(theta,x) - f(tuple(p1),x) - f(tuple(p2),x) + f(tuple(p3),x)) \
                    / (dt_p[i]*dt_p[j])
            FI[i,j] = cov
            FI[j,i] = cov

    # asynptotic variance covariance matrix
    acov = np.linalg.inv(FI)

    return acov

def t_rp(time_y):
    'Return Period Calculation'
    ny = len(time_y)
    return np.array([1/(1-(n/(ny+1))) for n in np.arange(1,ny+1)])
