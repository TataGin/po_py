
# coding: utf-8

# In[5]:


import sqlalchemy as sql


# In[3]:


class SqlServer:
    
    """ Wrapper for connecting to SSMS, query and write data """
    
    def __init__(self, userID, password, dsn):
        self.id = userID
        self.pwd = password
        self.dsn = dsn
        self.status = False
        self.conn = sql.create_engine('mssql+pyodbc://'+self.id+':'+self.pwd+'@'+self.dsn)

