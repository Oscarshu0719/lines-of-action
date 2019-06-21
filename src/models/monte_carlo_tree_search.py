# -*- coding: utf-8 -*-

from math import log, sqrt
from src.models.chessboard import State
from src.models.node_state import NodeState
from src.models.tree_node import TreeNode
from sys import maxsize

COMPUTATION_LIMIT = 100

def monteCarloTreeSearch(chessboard):
    """
    Main function of Monte Carlo Tree Search (MCTS).
    """
    init_state = NodeState(chessboard)
    init_state.setCurrentTurn(State.BLACK)
    init_node = TreeNode(init_state)

    for _ in range(COMPUTATION_LIMIT):
        expanded_node = treePolicy(init_node)
        reward = defaultPolicy(expanded_node)
        backPropagation(expanded_node, reward)
        
    best_child_node = findBestChild(init_node, False)
    return best_child_node.getState().getBestMovement()
        
def treePolicy(node):
    """
    Tree policy (Selection and expansion steps).
    """
    while not node.getState().checkTerminal():
        if node.checkFullyExpanded():
            node = findBestChild(node, True)
        else:
            return expandNode(node)
    return node
    
def defaultPolicy(node):
    """
    Default policy (Simulation step).
    """
    current_state = node.getState()
    
    children_nodes_num = 1
    while not current_state.checkTerminal():
        children_nodes_num += 1
        tmp = current_state.getNextState()
        if tmp is None:
            break
        else:
            current_state = tmp
            
    reward = current_state.computeReward() / children_nodes_num
    
    return reward
    
def expandNode(node):
    """
    Expand nodes.
    """
    tried_children_nodes_states = [child_node.getState() for child_node in node.getChildrenNodes()]

    new_state = node.getState().getNextState()
    
    while new_state in tried_children_nodes_states:
        new_state = node.getState().getNextState()
    
    child_node = TreeNode(new_state)
    node.addChild(child_node)
    
    return child_node
    
def backPropagation(node, reward):
    """
    Backpropagation step.
    """
    while node is not None:
        node.setVisitedTimes(node.getVisitedTimes() + 1)
        node.setQualityValue(node.getQualityValue() + reward)
        node = node.getParentNode()
    
def findBestChild(node, is_exploration):
    """
    Find the best children node by Upper Confident Bound (UCB) algorithm.
    """
    best_score = -maxsize
    best_child_node = None
    for child_node in node.getChildrenNodes():
        if is_exploration:
            const_c = 1 / sqrt(2)
        else:
            const_c = 0
        
        score = child_node.getQualityValue() / child_node.getVisitedTimes() + \
        const_c * sqrt(2 * log(node.getVisitedTimes()) / child_node.getVisitedTimes())
        
        if score > best_score:
            best_score = score
            best_child_node = child_node

    return best_child_node
