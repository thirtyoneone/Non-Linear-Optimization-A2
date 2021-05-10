#!/usr/bin/env python
# coding: utf-8

# In[1]:


#line search without derivative


# In[2]:


import math
import pandas as pd
import numpy as np


# In[46]:


#set the theta(lambda) here
def theta(x):
    return 6 * (math.exp(-2*x)) + 2 * x**2


# In[4]:


def mod(x):
    if x < 0:
        return -1 * x
    else:
        return x


# In[5]:


def goldenSection(a,b,length):
    alpha = 0.618
    
    #order on the line a, l, u, b
    l = a + (1 - alpha) * (b - a)
    u = a + alpha * (b-a)
    tl = theta(l)
    tu = theta(u)
    
    n = 1
    
    df = pd.DataFrame([[a,b,l,u,tl,tu]], columns = list('ablu12'))
    
    while((mod(b-a) > length) and (n < 101)):
        #print(df)
        if(tl > tu):
            #the interval reduced from a,b to l,b
            a = l
            
            #lk+1 = uk
            l = u
            tl = tu #this step is key because this saves us one theta computation each iter
            
            #uk+1 =  ak+1 + alpha * (bk+1-ak+1)
            u =  a + alpha * (b-a)
            tu = theta(u)
                                
        else:
            #the interval reduces to a,u
            b = u
            
            #uk+1 = lk
            u = l
            tu = tl #this step is key because this saves us one theta computation each iter
            
            #lk+1 = ak+1 + (1 - alpha) * (bk+1 - ak+1)
            l = a + (1 - alpha) * (b - a)
            tl = theta(l)
            
        #updating iter
        n += 1
        df = df.append(pd.DataFrame([[a,b,l,u,tl,tu]], columns = list('ablu12')), ignore_index = True)
    print(df)


# In[6]:


def fib(n):
    l = np.zeros([n,1])
    #print(l)
    for i in range(n):
        if i == 0 or i == 1:
            l[i] = 1
        else:
            l[i] = (l[i-1] + l[i-2])
    return l


# In[37]:


print(fib(10)[8])


# In[68]:


#some error
def fibonacciSearch(a,b,n):
    flist = fib(n)
    
    #print(a)
    l = a + (flist[n-1-2]/flist[n-1]) * (b - a)
    u = a + (flist[n-1-1]/flist[n-1]) * (b - a)
    tl = theta(l)
    tu = theta(u)
    
    
    df = pd.DataFrame([[a,b,l,u,tl,tu]], columns = list('ablu12'))
    #print(f"{a}, {b}, {l}, {u}, {tl}, {tu}")
    for k in range(1,n-1):
        
        if(tl > tu):
            #the interval reduced from a,b to l,b
            a = l
            
            #lk+1 = uk
            l = u
            tl = tu #this step is key because this saves us one theta computation each iter
            
        
            u =  a + (flist[n-1 - k - 1]/flist[n-1 - k]) * (b - a)
            #print(u)
            tu = theta(u)
                       
        else:
            #the interval reduces to a,u
            b = u
            
            #uk+1 = lk
            u = l
            tu = tl #this step is key because this saves us one theta computation each iter
            
           
            l = a + (flist[n-1 - k - 2]/flist[n-1 - k]) * (b - a)
            tl = theta(l)
        
        #print(f"{a}, {b}, {l}, {u}, {tl}, {tu}")
        df = df.append(pd.DataFrame([[a,b,l,u,tl,tu]], columns = list('ablu12')), ignore_index = True)
    print(df)


# In[69]:


fibonacciSearch(-5,5,12)


# In[72]:


print(theta(0.6944))


# In[8]:


def dichotomousSearch(a,b,e,length):
    df = pd.DataFrame([], columns = list('ablu12'))
    
    while(mod(b-a) > length):
        l = (a+b)/2 - e
        u = (a+b)/2 + e
        
        if(theta(l) > theta(u)):
            a = l
        else:
            b = u
        df = df.append(pd.DataFrame([[a,b,l,u,theta(l),theta(u)]], columns = list('ablu12')), ignore_index = True)
    print(df)


# In[12]:


#goldenSection search between -5 and 5 with required accuracy of atleast 0.1 or at most 100 iterations

goldenSection(-5,5,0.1)


# In[13]:


#dichotomous search between -5 and 5 with required accuracy of atleast 0.1 and epsilon = 0.01

dichotomousSearch(-5,5,0.01,0.1)


# In[ ]:




