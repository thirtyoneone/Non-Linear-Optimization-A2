#!/usr/bin/env python
# coding: utf-8

# In[3]:


import math
import numpy as np
import pandas as pd


# In[3]:


def modv(x1,x2,y1,y2):
    return ((x1-y1)**2 + (x2-y2)**2)**1/2


# In[4]:


def mod(x):
    if x < 0:
        return -1 * x
    else:
        return x


# In[14]:


def theta(x1,x2,l0,l1):
    return (1 - (x1 + l0))**2 + 100 * ((x2 + l1) - (x1 + l0)**2)**2


# In[17]:


theta(1,1,0,0)


# In[132]:


#for 2 variable not properly vectorized

def cyclicCoordinate(x1,x2,e):  
    y1 = x1
    y2 = x2
    
    df = pd.DataFrame([[x2,y2,theta(x2,y2,0,0)]], columns = list('xyf'))
    for i in range(27):
    #while(modv(y1,y2,x1,2) > e):
        #along i
        a = 0
        b = 10
        
        while(mod(b-a) > 0.2):
            l = (a+b)/2 - 0.01
            u = (a+b)/2 + 0.01
            
            if(theta(y1,y2,l,0) > theta(y1,y2,u,0)):
                a = l
            else:
                b = u
                
            #print((a+b)/2)
                
        y1 += (a+b)/2
    
        #along j
        a = 0
        b = 10
        
        while(mod(b-a) > 0.2):
            l = (a+b)/2 - 0.01
            u = (a+b)/2 + 0.01
            
            if(theta(y1,y2,0,l) > theta(y1,y2,0,u)):
                a = l
            else:
                b = u
            
            #print((a+b)/2)
                
        y2 += (a+b)/2
        
        df = df.append(pd.DataFrame([[y1,y2,theta(y1,y2,0,0)]], columns = list('xyf')), ignore_index = True)
    print(df)


# In[133]:


#cyclic coordinate method starting from (0,0) using a line search method
cyclicCoordinate(0,0,0.1)


# In[9]:


#for 2 variable not properly vectorized

def hookeJeeve(x1,x2,e):  
    y1 = x1
    y2 = x2
    
    for i in range(50):
    #while(modv(y1,y2,x1,2) > e):
        #exploratory search
        #along i
        a = -5
        b = 5
        
        while(mod(b-a) > 0.002):
            l = (a+b)/2 - 0.0001
            u = (a+b)/2 + 0.0001
            
            if(theta(y1,y2,l,0) > theta(y1,y2,u,0)):
                a = l
            else:
                b = u
                
            #print((a+b)/2)
                
        y1 += (a+b)/2
    
        #along j
        a = -5
        b = 5
        
        while(mod(b-a) > 0.002):
            l = (a+b)/2 - 0.0001
            u = (a+b)/2 + 0.0001
            
            if(theta(y1,y2,0,l) > theta(y1,y2,0,u)):
                a = l
            else:
                b = u
            
            #print((a+b)/2)
                
        y2 += (a+b)/2
        
        #patten search
        if(1):
            a = -5
            b = 5

            while(mod(b-a) > 0.002):
                l = (a+b)/2 - 0.0001
                u = (a+b)/2 + 0.0001

                if(theta(y1,y2,l*(y1-x1),l*(y2-x2)) > theta(y1,y2,u*(y1-x1),u*(y2-x2))):
                    a = l
                else:
                    b = u

                #print((a+b)/2)

            y1 += (a+b)/2 * (y1-x1)
            y2 += (a+b)/2 * (y2-x2)

            x1 = y1
            x2 = y2    
        
        print(f"{theta(y1,y2,0,0)} {y1},{y2}")


# In[18]:


def hjDiscrete(x1,y1,a,d,e):
    x2 = x1
    y2 = y1
    
    #temp var
    x0 = x1
    y0 = y1
    
    df = pd.DataFrame([[x2,y2,d,theta(x2,y2,0,0)]], columns = list('xydf'))
    #for i in range(16):
    while(d > e):
        #along i
        if(theta(x2,y2,d,0) < theta(x2,y2,0,0)):
            x2 += d

        else:
            if(theta(x2,y2,-d,0) < theta(x2,y2,0,0)):
                x2 -= d
        #print(f"{x2},{y2}")
        
        #along j
        if(theta(x2,y2,0,d) < theta(x2,y2,0,0)):
            y2 += d

        else:
            if(theta(x2,y2,0,-d) < theta(x2,y2,0,0)):
                y2 -= d
        #print(f"{x2},{y2}")       
        
        #evaluating the pattern step
        if(theta(x2,y2,0,0) < theta(x1,y1,0,0)):
            #step3
            x0 = x2
            y0 = y2
            
            x2 += a*(x0 - x1)
            y2 += a*(y0 - y1)
            
            x1 = x0
            y1 = y0
            
        else:
            d /= 2
            
            x2 = x1
            y2 = y1
        df = df.append(pd.DataFrame([[x2,y2,d,theta(x2,y2,0,0)]], columns = list('xydf')), ignore_index = True)
        #print(theta(x1,y1,0,0))
    print(df)


# In[29]:


print(theta(0.2,-0.1,0,0))


# In[19]:


#hooke and jeeves method from 0,0 with acceleration factor 1 and step size 0.2
hjDiscrete(0,0,1,0.2,0.01)


# In[195]:


def rosenbrockDiscrete(x1,y1,a,b,d,l,e):
    x2 = x1
    y2 = y1
       
    d1 = np.copy(d)
    flag = 0
    
    df = pd.DataFrame([[x2,y2,d[0],d[1],theta(x2,y2,0,0)]], columns = list('xy12f'))
    for i in range(78):
    #while
        if flag == 3:
            d = np.copy(d1)

        flag = 0
        #along i
        if(theta(x2,y2,d[0]*l[0][0],d[0]*l[0][1]) < theta(x2,y2,0,0)):
            x2 += d[0]*l[0][0]
            y2 += d[0]*l[0][1]
            d[0] *= a
        else:
            flag += 1
            d[0] *= b
        
        #along j
        if(theta(x2,y2,d[1]*l[1][0],d[1]*l[1][1]) < theta(x2,y2,0,0)):
            x2 += d[1]*l[1][0]
            y2 += d[1]*l[1][1]
            d[1] *= a
        else:
            flag += 1
            d[1] *= b
        #df = df.append(pd.DataFrame([[x2,y2,d[0],d[1],theta(x2,y2,0,0)]], columns = list('xy12f')), ignore_index = True)
        if flag == 2:
            #df = df.append(pd.DataFrame([[i,0,0,0,0]], columns = list('xy12f')), ignore_index = True)
            if(x1 == x2) and (y1 == y2):
                continue
            
            #print(f"dir change {i}")
            l[0][0] = (x2 - x1)/math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            l[0][1] = (y2 - y1)/math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            l[1][0] = l[0][1]
            l[1][1] = -1 * l[0][0]
            
            flag = 3
            
            x1 = x2
            y1 = y2
        df = df.append(pd.DataFrame([[x2,y2,d[0],d[1],theta(x2,y2,0,0)]], columns = list('xy12f')), ignore_index = True)
        
    pd.set_option('display.max_rows', df.shape[0]+1)
    print(df)


# In[14]:


print(theta(1.65,1.35,0,0))


# In[196]:


#rosenbrock method with initial point (0,0) step (0.5,0.3) and d1 (1,1) and d2 (-1,1)
rosenbrockDiscrete(0,0,2,-0.5,np.array([0.5,0.3]),np.array([[1.0,1.0],[-1.0,1.0]]),0.01)


# In[ ]:





# In[ ]:




