from util import entropy, information_gain, partition_classes
import numpy as np 
import ast
import numbers

class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        #self.tree = []
        self.tree = {}
        self.max_depth = 15 # limit how deep the tree is
        self.min_size = 40 #limit smallest count of records to build a node on
        self.current_depth = 0
        pass


    def find_split(self,X,y): # Recursive functions to return a decision tree
        index_best = 0
        split_val_best = X[0][0]
        gain = 0
      #  print("Current depth: ", self.current_depth)
        for index in range(0,len(X[0])):
            #print ("column ", index)
            for row in X:
                # split the data and find information gain
                X_left, X_right, y_left, y_right = partition_classes(X,y,index,row[index])
                new_gain = information_gain(y,[y_left,y_right])
             #   print("index: ", index, " val: ", row[index], " gain: ",new_gain)
              #  print("left: ", y_left, " right: ", y_right)
                if new_gain > gain:
                    gain = new_gain
                    X_left_best = X_left
                    X_right_best = X_right
                    y_left_best = y_left
                    y_right_best = y_right
                    index_best = index
                    split_val_best = row[index]
        if gain == 0 or self.current_depth == self.max_depth or len(X) < self.min_size: # or depth or min size ???
            if y.count(0) < y.count(1): # define leaf node
                label = 1
            else:
                label = 0
          
            return {"index":-1, "val": label} #mark leaf node with -1 split attribute index
        else:
         #   return {"index":index_best, "val": split_val_best,\
          #         "left_x": X_left_best, "right_x": X_right_best,\
           #        "left_y": y_left_best, "right_y": y_right_best}
            self.current_depth += 1
            return {"index":index_best, "val": split_val_best,\
                   "left": self.find_split(X_left_best, y_left_best), \
                   "right": self.find_split(X_right_best, y_right_best) \
                   }

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        self.tree = self.find_split(X,y)
        return

    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        node = self.tree
       # print(node)
        index = node['index']
        val = node['val']
        while index != -1:
            if isinstance(val, numbers.Number):
                if record[index] <= val:
                    node = node["left"]
                else:
                    node = node["right"]
            else:
                if record[index] == val:
                    node = node["left"]
                else:
                    node = node["right"]    
            index = node['index']
            val = node['val']            
        return val