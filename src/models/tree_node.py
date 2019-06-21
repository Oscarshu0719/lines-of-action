# -*- coding: utf-8 -*-

class TreeNode(object):
    """ Class
    Describe a tree node of Monte Carlo tree.
    """
    
    MAX_CHILDREN_NUM = 100
    CONST_C = 1.96
    
    def __init__(self, state=None):
        self._state = state
        self._parent_node = None
        self._children_nodes = []
        self._quality_value = 0
        self._times_visited = 0
    
    def getState(self):
        """
        Return the state of this node.
        """
        return self._state
    
    def getParentNode(self):
        """
        Return the parent node of this node.
        """
        return self._parent_node
    
    def getChildrenNodes(self):
        """
        Return the children nodes of the this node.
        """
        return self._children_nodes

    def getQualityValue(self):
        """
        Return the quality value of this node.
        """
        return self._quality_value
    
    def getVisitedTimes(self):
        """
        Return the visited times of this node.
        """
        return self._times_visited
    
    def setState(self, state):
        """
        Setup the state of this node.
        """
        self._state = state
        
    def setParentNode(self, parent_node):
        """
        Setup the parent node of this node.
        """
        self._parent_node = parent_node
        
    def addChild(self, child_node):
        """
        Add a children node to this node.
        """
        child_node.setParentNode(self)
        self._children_nodes.append(child_node)
        
    def setQualityValue(self, quality_value):
        """
        Setup quality value of this node.
        """
        self._quality_value = quality_value
        
    def setVisitedTimes(self, times_visited):
        """
        Setup the visited times.
        """
        self._times_visited = times_visited
        
    def checkFullyExpanded(self):
        """
        Check if this node is fully expanded.
        """
        return len(self.getChildrenNodes()) == TreeNode.MAX_CHILDREN_NUM
     
    def __repr__(self):
        return "< Node = State: {}, ParentNode: {}, ChildrenNodes: {}, QualityValue: {}, VisitedTimes: {} >" \
    .format(self.getState(), self.getParentNode(), self.getChildrenNodes(), self.getQualityValue(), self.getVisitedTimes())
