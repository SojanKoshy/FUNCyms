import json
from urllib import addbase
import os
import requests
from requests.auth import HTTPBasicAuth

class Topology:

    def __init__(self):
        
        self.node_id = [1, 2, 3, 4]
        self.node_prop = ["A", 200, -1, ""]
        self.number_of_tp = [1, 2, 3, 4]        
        self.tp_id = [100, 200, 300, 400]
      
    def create(self):      
        data = {
            "node": [
                {
                    "node-prop": [
                        self.node_prop[0]
                    ],
                    "termination-points": {
                        "number-of-tp": self.number_of_tp[0],
                        "termination-point": [
                            {
                                "tp-id": self.tp_id[0]
                            }
                        ]
                    },
                    "node-id": self.node_id[0]
                }
            ]
        }
        return json.dumps(data, indent=4)
    
    def update(self):
        data = {
            "node": [
                {
                    "node-prop": [
                        self.node_prop[0]
                    ],
                    "termination-points": {
                        "number-of-tp": self.number_of_tp[1],
                        "termination-point": [
                            {
                                "tp-id": self.tp_id[1]
                            },
                            {
                                "tp-id": self.tp_id[2]
                            }
                        ]
                    },
                    "node-id": self.node_id[1]
                }
            ]
        }      
        return json.dumps(data, indent=4)
        
    def replace(self):
        data = {
            "node": [
                {
                    "node-prop": [
                        self.node_prop[0]
                    ],
                    "termination-points": {
                        "number-of-tp": self.number_of_tp[2],
                        "termination-point": [
                            {
                                "tp-id": self.tp_id[1]
                            }
                        ]
                    },
                    "node-id": self.node_id[0]
                },
                {
                    "node-prop": [
                        self.node_prop[1]
                    ],
                    "termination-points": {
                        "number-of-tp": self.number_of_tp[0],
                        "termination-point": [
                            {
                                "tp-id": self.tp_id[3]
                            }
                        ]
                    },
                    "node-id": self.node_id[1]
                }
            ]
        }      
        return json.dumps(data, indent=4)
        
