#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import pandas as pd
import numpy as np


# In[2]:


#set the theta(lambda) here
def theta(x):
    return 6 * (math.exp(-2 * x)) + 2 * x**2


# In[42]:


def theta_derivative(x):
    return 4 * x - 12 * (math.exp(-2 * x))


# In[39]:


print(theta_derivative(0.4))


# In[43]:


def theta_derivative_derivative(x):
    return 4 + 24 * (math.exp(-2 * x))


# In[4]:


def mod(x):
    if x < 0:
        return -1 * x
    else:
        return x


# In[17]:


def bisectionalSearch(a,b,length):
    
    l = (a + b)/2
    
    df = pd.DataFrame([], columns = list('abl1'))
    print("1")
    while(mod(b - a) > length):
        if theta_derivative(l) == 0:
            print(f"{l} is the minima")
            return
        
        elif theta_derivative(l) > 0:
            b = l
            l = (a + b)/2
        
        else:
            a = l
            l = (a + b)/2
        df = df.append(pd.DataFrame([[a,b,l,theta_derivative(l)]], columns = list('abl1')), ignore_index = True)
    
    print(df)


# In[57]:


#the while condition needs to be implemented
def newtonMethod(l, e):
    l1 = l - (theta_derivative(l)/theta_derivative_derivative(l))
    
    df = pd.DataFrame([[l,theta_derivative(l),theta_derivative_derivative(l),l1]], columns = list('l12u'))
    #print(f"{l},{l1}")
    
    for i in range(100):
    #while(mod(l - l1) > e or theta_derivative(l) > e):
        l = l1
        l1 = l - (theta_derivative(l)/theta_derivative_derivative(l)) 
        
        #print(f"{l},{l1}")
        df = df.append(pd.DataFrame([[l,theta_derivative(l),theta_derivative_derivative(l),l1]], columns = list('l12u')), ignore_index = True)
        
        if l == l1:
            break
    print(df)


# In[58]:


#bisectional search between -5 and 5 with required accuracy of atleast 0.1

bisectionalSearch(-5,5,0.1)


# In[59]:


#newtonmMethod search from 0 
newtonMethod(0,1)


# In[ ]:




