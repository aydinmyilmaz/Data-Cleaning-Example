
# coding: utf-8

# In[131]:


import pandas as pd
import re
import numpy as np
pd.options.display.max_colwidth = 100


# In[142]:


# 1. Step

def num_uniuni_1 (element):
    
    try:   
        t = re.findall(r"(\d+)\ ([a-z-A-Z]+\/[a-z-A-Z]+)", element) # pattern for; "100 Ui/Ml" to ----> 100 Ui/Ml----> 100 ml

        try:                      
            for item in t[0][1].split("/"):

                if item.lower()=="ml":
                    
                    element=element.replace(t[0][1],"ml")

                elif item=="G" or item=="M":
                    
                    element=element.replace(t[0][1],"mg")
        except:
        
            pass
    except:
        
        pass
    
    return element


# In[143]:


# function test
num_uniuni_1 ("100 Ui/Ml XYZ 80Ml")


# In[62]:


# 2. Step

def numuni_numuni_2(element):
    
    try:
        
        unit_list=["ML","Ml","mL","ml","MG","Mg","mG","mg","CM","Cm","cM","cm","M","Cps","L","G","Kg","KG","kg","G","GR","Gr"]
    
        list_element1= element.split(" ")
    
        for idx, item in enumerate(list_element1):
        
            z = re.match(r"([\d])+[a-zA-z]", item) # Pattern for; from ----> #300Ml/5ML  100Ml' to-----> [('300', 'Ml'), ('5', 'ML'), ('100', 'Ml')]
        
            if bool(z):
                          
                    zz=re.findall(r"(\d+)+([a-zA-Z]+)",item) # 300Ml/5ML  100Ml'-----> [('300', 'Ml'), ('5', 'ML'), ('100', 'Ml')]
                
                    del list_element1[idx]
                 
                    sep_elements = " ".join([element for tupl in zz for element in tupl])
                
                    list_element1.insert(idx,sep_elements.lower())   
                    
        element = " ".join(list_element1)
        
        return (element)    
    
    except:
        
        pass
    
        


# In[81]:


# function test
numuni_numuni_2("A-Derma Dermalib Cr 50Mg/30Ml Abcd 50ML")


# In[64]:


# 3.Step
   
def num_uni_3(element):
   
   try:
       
       unit_list=["ML","Ml","mL","ml","MG","Mg","mG","mg","CM","Cm","cM","cm","M","Cps","L","G","Kg","KG","kg","G","GR","Gr","Mcg", "MCG"]
       
       list_element2= element.split(" ")
   
       # pattern for; from ---> 300 ML to ----> 300 ML-----> 300 ml
       # (previous pattern (to keep just in case) (r"(\d+)\ ([A-Z]+[a-z-A-Z])" ) 
       
       t = re.findall(r"(\d+)\ (\w+)", element)  
       
       for item in t:
       
           try:
           
               if item[1] in unit_list:
               
                   idx = list_element2.index(item[1])
               
                   del list_element2[idx]
               
                   list_element2.insert(idx,item[1].lower()) 
               
           except:
           
               pass  
           
       element = " ".join(list_element2) 
       
       return (element)
   
   except:
       
       pass
   
            


# In[65]:


# function test
num_uni_3("Acarbose Bluepharma Mg, 100 Ml X 50 Comp")


# In[66]:


# 4.step 

def numnum_uni_4 (element):
    try:
        list_element= element.split(" ")
    
        t = re.findall(r"(\d+\/\d+)+([a-zA-Z]+)", element) # Pattern for; from ---> 50/150MG to ---> 50/150 mg
    
        try:
  
            for item in list_element:
        
                z = re.match(r"(\d+\/\d+)+([a-zA-Z]+)", item)
            
                if bool(z):
                
                    new_item = " ".join([x for tupl in t for x in tupl])
                
                    element = element.replace(item, new_item.lower() )

        except:
        
            pass
        
    except:
        
        pass
    
    return element


# In[67]:


# function test
numnum_uni_4 ("50/150MG")


# In[69]:


# gathering all functions in a single function 
def allfunc(element):
    
    e1 = num_uniuni_1 (element)
    e2 = numuni_numuni_2(e1)
    e3 = num_uni_3(e2)
    e4 = numnum_uni_4 (e3)
    
    return e4


# In[74]:


# function test
allfunc("Lauroderme Fraldas Tam 4 9-15 Kg X 50 Un")


# In[134]:


df=pd.read_excel("mapped_dataset.xlsx")


# In[135]:


df["newly_cleaned_product_name"] = df["clean_product_name"].apply(allfunc)


# In[136]:


df["newly_cleaned_product_name"].nunique()


# In[137]:


df.sample(5)


# In[138]:


import numpy as np
df["recently_cleaned_product_name"]=np.where( (df['newly_cleaned_product_name']==df["clean_product_name"])
                                                        , np.nan, df['newly_cleaned_product_name'])


# In[139]:


df.drop(columns=["newly_cleaned_product_name"], axis=1,inplace=True)


# In[140]:


df.sample(50)


# In[141]:


df.to_csv("cleaned_dataset.csv")

