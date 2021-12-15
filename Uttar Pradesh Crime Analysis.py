#!/usr/bin/env python
# coding: utf-8

# # Uttar Pradesh Crime Analysis
# #By- Shubham Kumar
# #Dated: July 12,2021

# In[1]:


from IPython.display import Image
Image(url='https://www.gannett-cdn.com/-mm-/4a94aaab8e826ca8563bd0e434c9fe36f1dc920f/c=0-0-399-300&r=x404&c=534x401/local/-/media/2016/07/20/FortMyers/FortMyers/636046215443097272-CRIME-gen-NP.jpg')


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
sns.set()


# In[3]:


df=pd.read_csv(r'/home/aarush100616/Downloads/Projects/Uttar Pradesh Crime Analysis/MR data - Compiled Data Set.csv')


# In[4]:


df


# In[5]:


#droping title and text columns
x_full = df.drop(axis = 1, labels = ['Title','Text'])


# In[6]:


#Renaming big column names(cleaning)
x_full = x_full.rename(columns = {'Murder Happened with reason:\n1:Property/Land Disputes,\n2:Family Dispute\n3:Petty Quarrels,\n4:Money Disputes, \n5:Personal Vendetta, \n6:Love Affairs, \n7:Casteism\n8: Unknown/other':'Murder Reason', 'Crime Against Women ( Combined ):\n1. Murder with Rape \n2. Dowry Deaths(Sec. 3048)\n3. Suicide(sec 305/306)\n4. Kidnapping(All)\n5. Acid Attack(Sec. 326A IPC)\n6. Cruelty by Husband/in-laws((Sec.498 A IPC)\n7. Rape only(Sec. 376 or 511 IPC)\n8. Assault on Women with Intent to Outrage her Modesty (Sec. 354 IPC)\n9. Cyber Crimes against Women\n10. Protection of Children from Sexual Offences Act':'crime against women(Act)'})
x_full.columns


# In[7]:


#drop rows with all null values apart from 'City '( cleaning )
x_full = x_full.dropna(axis = 0, subset= ['City '], how = 'all')


# In[8]:


#checking Null Values
x_full.isnull().sum()


# In[9]:


#replacing NaN values in "number of" type and NaN values in crime agaisnt women column with 0 
x_full = x_full.fillna(0)


# In[10]:


#seperating acts
crime_acts = x_full['crime against women(Act)'].astype('string').values
for i in range(1,11):
    x_full.insert(8+i,"Act {}".format(i),0)
for j in range(len(crime_acts)):
    splitted = crime_acts[j].split(',')
    for x in splitted:
        if x=='0':
            continue
        x_full.loc[int(j),'Act {}'.format(x.strip())]=1
x_full


# ## City-wise Crime Report

# In[11]:


sns.countplot(x = 'City ', data = x_full, palette = 'mako').set(title = 'city-wise crime count')


# ## Reasons For Murder

# In[12]:


plt.figure(figsize = (10,10))
reason = x_full['Murder Reason'].value_counts().to_dict()
reason.pop(0)
val = list(reason.values())
label = list(reason.keys())
plt.title('Distribution of Reasons for Murder',fontsize = 20)
plt.pie(x = val,labels = label)
plt.show()


# ## Love Affair victims Gender Distribution

# In[13]:


#love affairs victims
mv = x_full.loc[x_full['Murder Reason'] == 'Love Affairs', "Number of male victims(adult)"].sum()
fv = x_full.loc[x_full['Murder Reason'] == 'Love Affairs', "Number of female victims(adult)"].sum()
plt.figure(figsize = (10,10))
plt.title('Love Affair victims',fontsize = 20)
plt.pie(x = [mv,fv],labels = ['females','males'],colors = ['pink','blue'])
plt.show()


# ## What crimes are causing women's death?

# In[14]:


#what is the biggest cause of women's death
wmr = x_full.loc[x_full['Number of female victims(adult)']>0]
plt.figure(figsize = (15,7))
sns.countplot(x = 'Murder Reason', data = wmr)


# ## Cause of men's death

# In[15]:


wmr = x_full.loc[x_full['Number of male victims(adult)']>0]
plt.figure(figsize = (15,7))
sns.countplot(x = 'Murder Reason', data = wmr)


# ## Distribution of Crime Againt Women on basis of Acts

# In[16]:


s = x_full.iloc[:,9:(9+10)].sum()
plt.figure(figsize = (15,5))
plt.bar(s.index,s.values)


# ## Reasons:
# -Murder with Rape
# -Dowry Deaths(Sec. 3048)
# -Suicide(sec 305/306)
# -Kidnapping(All)
# -Acid Attack(Sec. 326A IPC)\n6. Cruelty by Husband/in-laws((Sec.498 A IPC)
# -Rape only(Sec. 376 or 511 IPC)
# -Assault on Women with Intent to Outrage her Modesty (Sec. 354 IPC)
# -Cyber Crimes against Women
# -Protection of Children from Sexual Offences Act

# ## Property Disputes

# In[17]:


mv = x_full.loc[x_full['Murder Reason'] == 'Property Disputes', "Number of male victims(adult)"].sum()
fv = x_full.loc[x_full['Murder Reason'] == 'Property Disputes', "Number of female victims(adult)"].sum()
plt.figure(figsize = (10,10))
plt.title('Property Disputes victims',fontsize = 20)
plt.pie(x = [mv,fv],labels = ['females','males'],colors = ['pink','blue'])
plt.show()


# ## Female vs Male involvement

# In[18]:


#females vs males crime
sns.set_palette("BrBG",1)
females = x_full['Number of female(adult)'].sum()
males = x_full['Number of male(adult) '].sum()
sns.barplot(x= ['femlaes','males'], y= [females, males]).set(title = 'Involved in Crime')


# ## Children vs Adulit Victims

# In[19]:


#Children vs Adults victims in crime city-wise
sns.set_palette("RdBu",)
females = x_full['Number of female victims(adult)'].sum()
males = x_full['Number of male victims(adult)'].sum()
child = x_full['Number of child victims'].sum()
sns.barplot(x= ['femlaes(adults)','males(adult)','children'], y= [females, males, child]).set(title = 'Victims of UP Crime')


# ## City-wise Child victims

# In[20]:


#child victims city-wise
sns.set_palette("YlOrBr", 1)
gbd = x_full.loc[x_full['City '] == 'Ghaziabad' , 'Number of child victims' ].sum()
lkw = x_full.loc[x_full['City '] == 'Lucknow' , 'Number of child victims' ].sum()
knp = x_full.loc[x_full['City '] == 'Kanpur' , 'Number of child victims' ].sum()
sns.barplot(y = [gbd,lkw,knp], x = ['Ghaziabad','Lucknow', 'Kanpur']).set(title = 'city-wise child victims')


# In[21]:


sns.set_palette("YlOrBr", 1)
gbd = x_full.loc[x_full['City '] == 'Ghaziabad' , 'Kidnnaping:\nNumber of child victims' ].sum()
lkw = x_full.loc[x_full['City '] == 'Lucknow' , 'Kidnnaping:\nNumber of child victims' ].sum()
knp = x_full.loc[x_full['City '] == 'Kanpur' , 'Kidnnaping:\nNumber of child victims' ].sum()
sns.barplot(y = [gbd,lkw,knp], x = ['Ghaziabad','Lucknow', 'Kanpur']).set(title = 'city-wise child kidnappings')

