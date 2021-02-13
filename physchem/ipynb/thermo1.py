#!/usr/bin/env python
# coding: utf-8

# # extract data from thermal conductivity diagrams
# 
# 

# ## overview
# * creates a project from raw PDFs
# * extracts images
# * creates octree 
# * filters by title (NYI)

# ### variables
# 
# Set variables which will be used later. Note that at present I can't get variables working in ami/picocli commands so we run the command from the project directory. This is probably a good thing anyway.
# 
# 

# In[1]:


# specific problem
THERMO = "thermo"

########### Remote raw data #############
# where is ami3? (assume you have checked out or copied `ami3` distrib)
# TODO - can we replace this by URL?

HOME = "/Users/pm286/"
WORKSPACE = HOME + "workspace/"
AMI3 = WORKSPACE + "cmdev/ami3/"

# general data resource within the `ami3` distrib
IPYNB = AMI3 + "src/ipynb/"
TEST_RESOURCES = AMI3 + "src/test/resources/"
AMI_DATA = TEST_RESOURCES + "org/contentmine/ami/"

# specific for thermal conductivity
THERMO_RAW = AMI_DATA + THERMO + "/"

print ("thermo raw: " + THERMO_RAW)

######### Local Resources #############

# local workspace
WORK = WORKSPACE + "work/"
THERMO_WORK = WORK + THERMO + "/"

### ami uses a CProject
PROJECT = THERMO_WORK


# In[2]:


## clean and copy 

get_ipython().system(' cd $THERMO_WORK')
# clean previous work
get_ipython().system(' rm -rf phys* make_project* logs*')
# clean copy of raw data
get_ipython().system(' cp -R $THERMO_RAW .')
get_ipython().system(' ls *.pdf')

# should be 6 files (may be less due to copyright)


# In[3]:


## make project

get_ipython().system(' ami -vv -p . makeproject --rawfiletypes pdf')


# In[4]:


ls phys*/


# In[5]:


# save original files (underscore convention means that it is not a CTree)
get_ipython().system(' mv *.pdf _original/')
get_ipython().system(' ls')


# In[6]:


# CONVERT PDF to SVG and PNG
get_ipython().system(' ami -vv -p . pdfbox')


# In[7]:


# see what we have produced (SVG and PNG)
get_ipython().system(' tree ')


# In[8]:



# octree creates a discrete set of color levels in each image (here 8)
get_ipython().system(' ami -vv -p .  --inputname raw --output octree image --octree 8  --outputfiles binary channels histogram neighbours octree')
print ("============ FINISHED OCTREE ===========")


# In[ ]:




