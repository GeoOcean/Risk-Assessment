from scipy.optimize import fsolve
import numpy as np
import math
import matplotlib.pyplot as plt

def waves_dispersion(T, h):
    'Resuleve la ecuación de dispersión'
    L1 = 1
    L2 = ((9.81*T**2)/2*np.pi) * np.tanh(h*2*np.pi/L1)
    umbral = 1

    while umbral > 0.01:
        L2 = ((9.81*T**2)/(2*np.pi)) * np.tanh((h*2*np.pi)/L1)
        umbral = np.abs(L2-L1)

        L1 = L2

    L = L2
    k = (2*np.pi)/L
    c = np.sqrt(9.8*np.tanh(k*h)/k)

    return(L, k, c)

def Goda(L0, hb, m):
    'Criterio de rotura de Goda'
    return(L0 * 0.17 * (1 - np.exp(-1.5 * np.pi * (hb/L0) * (1 + 15 * m**(4/3)))))

def Ks(Cg0, Cg1):
    'Coeficiente de Asomeramiento'
    return(np.sqrt(Cg0/Cg1))

def Kr(theta_0, theta_1):
    'Coeficiente de Refración'
    return(np.sqrt(np.cos(np.deg2rad(theta_0))/np.cos(np.deg2rad(theta_1))))

def cg(L, T, h):
    'Group Celerity'
    k = 2 * np.pi / L
    n = 0.5 * (1 + 2*k*h / np.sinh(2*k*h))
    C = L/T
    return (C * n)

def Iro(m, H, L0):
    'Iribarren NUmber'
    return(m /(H /L0)**0.5)

def theta(C0, C1, theta_0):
    'Snells law'
    return(np.rad2deg(np.arcsin(C1/C0 * np.sin(theta_0))))

def theta_b(hb, theta_0, T):
    return(np.arcsin(np.sqrt(g*hb)*np.sin(theta_0)/(g*T/(2*np.pi))))










