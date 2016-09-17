import json
from urllib import addbase
import os
import requests
from requests.auth import HTTPBasicAuth

class Topology:

    def __init__(self):
    
      self.node_id = [1,2,3,4]
      self.node_prop = ["A",200]
      self.number_of_tp = 200        
      self.tp_id = [100,200,300]
      self.termination_point = []
      
    def postJson(self):        
      postdata = {}
      termination_point_value = []
      node_prop_value = []
      node_value = []
      
      termination_point_value.append({
                         'tp-id': self.tp_id[0]
                         })
      if self.number_of_tp != '':
          postdata['number-of-tp'] = self.number_of_tp
    
      if self.termination_point != '':
          postdata['termination-point'] = termination_point_value
     
      node_prop_value.append(
                              self.node_prop[0]
                              )
      
      node_value.append({                        
                         'termination-points' :postdata,
                          'node-id' : self.node_id[0],
                          'node-prop':node_prop_value
                          
                         })
      postdata = {'node' :node_value}
      
      print("output")
      print(postdata)
      
      #return json.dumps(Dicdata,indent=4)
    
    
    
    def putJson(self):
        putdata = {}
        termination_point_value = []
        node_prop_value = []
        node_value = []
        
        for i in  range(3):
            termination_point_value.append({
                         'tp-id': self.tp_id[i]
                         }
                         )
        if self.number_of_tp != '':
            putdata['number-of-tp'] = self.number_of_tp
    
        if self.termination_point != '':
            putdata['termination-point'] = termination_point_value
     
        node_prop_value.append(
                              self.node_prop[0]
                              )
      
        node_value.append({                        
                         'termination-points' :putdata,
                          'node-id' : self.node_id[1],
                          'node-prop':node_prop_value
                          
                         })
        putdata= {'node' :node_value}
      
        print("output")
        print(putdata)
        
    
    def  Comments(self):
        print("**********************************************************************************\n")
        
        
j = Topology()
j.postJson()
j.putJson()        
