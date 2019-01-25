
# coding: utf-8

# In[27]:


import pandas as pd
import re
pd.options.display.max_colwidth = 100


# In[28]:


df=pd.read_excel("mapped_dataset.xlsx")


# In[ ]:


# yeni sutunlar için toplam 3 fonksiyon yazıldı


# In[31]:


def amount_unit(element): 
    
    try:
        
        element=element.lower()
        
    except:
        
        element=element
    
    try:
                
        if ", " in element:
            
            k=re.findall(r"\w?\d+\,?\w?\d*", item)
            
            if not bool(k):
                
                element1= element.split(",")[1]
                
            else:
                element1= element
        else:
            element1 = element
            
    except:
        
        element1 = element
    
    try:
        
        elist = element1.split()
        
        new_list=[]
    
        for i,item in enumerate(elist):
            
            z=re.findall(r"\w?\d+\,?\w?\d*", item) 
            
            if bool(z) and item not in new_list:
                
                new_list.append(item)
                
                try:
                    
                    if len(elist[i+1]) <= 7 :
                    
                        new_list.append(elist[i+1])
                        
                    if elist[i+2].lower() == "x":
                        
                        new_list.append("x")
                        
                except:
                    
                    pass
                        
        return new_list
     
    except:
        
        return "NaN"
    
    
def seperate(alist):   
    
    new_cell2=[]
    
    for item in alist:

        ss = re.split(r"(\d+\/\d+\,?\d+)?([a-zA-Z]+)",item)
        
        new_cell2.append(ss)
                   
    return [x for ite in new_cell2 for x in ite if x != "" and x != " " and x !=None ] 


def tidy_cell(alist):
    
    new_cell=[]

    for item in alist:
            
        new_cell.append((item).replace("("," ").replace(")"," ").replace("+"," ").replace(" +"," ").replace("+ "," ").replace("-"," ").
                        replace(":","").replace("="," ").replace(" ="," ").replace("= "," "))
                
    return new_cell



# In[32]:


# miktar ve ilgili unitlerin (product_name) sutunundan alınarak (values) sutununun oluşturulması----> (amount_unit) fonksiyonu 

df["values"]=df.product_name.apply(amount_unit)


# In[33]:


# (seperated_values) sutunu---> üstteki fonksiyonla oluşturulan (values) sutunundaki bitişik kalan elemanları da alt elemanlarına ayırmak 
# ve aradaki gereksiz işaretleri "+,-,/" temizlemek için 	[200ml+]--->[200, ml]

df["seperated_values"]=df["values"].apply(seperate).apply(tidy_cell)


# In[16]:


#df.sample(10)


# In[34]:


# seperated_values sutunundan unique değerlerin çekilmesi 


from numpy import array
import collections, numpy

def unique_values_dict(element):

    unique_list = [x for item in element for x in item]

    unique_list_array = numpy.array(unique_list )

    unique_list_dict=collections.Counter(unique_list_array)
    
    return unique_list_dict



# In[35]:


len(unique_values_dict(df["seperated_values"]))


# In[19]:


#unique_list_sorted = sorted([(v,k) for (k,v) in new_dict.items()])


# In[38]:


df[["product_name","values","seperated_values"]].sample(5)

