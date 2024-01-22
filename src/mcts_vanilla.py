from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log

num_nodes = 100
explore_faction = 2.

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    """ Traverses the tree until the end criterion are met.
    e.g. find the best expandable node (node with untried action) if it exist,
    or else a terminal node

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 1 or 2

    Returns:
        node: A node from which the next stage of the search can proceed.
        state: The state associated with that node

    """
    children = [] # list of dicts with node and ucb val
    explore_node = None
    is_opponent = False if board.current_player(state) == bot_identity else True

    if node.untried_actions: # node is expandable
        return node, state
    
    for child in node.child_nodes.values():
        children.append({'node' : child, 'val' : ucb(child, is_opponent)})

    explore_node = max(node['val'] for node in children)

    return traverse_nodes(explore_node, board, state, bot_identity)
    

def expand_leaf(node: MCTSNode, board: Board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node (if it is non-terminal).

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:
        node: The added child node
        state: The state associated with that node

    """
    action = choice(board.legal_actions(state)) # pick a random action
    next_state = board.next_state(state, action)
    child = MCTSNode(node, action, [board.legal_actions(next_state)])
    node.child_nodes.update({action : child}) # add child node
    node.untried_actions.remove(action) # action has been tried, remove from list

    return child, next_state


def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state

    """
    while not board.is_ended(state):
        me = board.current_player(state)
        moves = board.legal_actions(state)
        best_move = moves[0]
        best_expectation = float('-inf')
        for move in moves:
            total_score = 0.0
            for r in range(ROLLOUTS):
                rollout_state = board.next_state(state, move)
                for i in range(num_nodes):
                    if board.is_ended(rollout_state):
                        break
                    rollout_move = choice(board.legal_actions(rollout_state))
                    rollout_state = board.next_state(rollout_state, rollout_move)

            g_point = board.points_values(rollout_state)
            o_boxes = board.owned_boxes(rollout_state)
            if g_point is not None:
                r_score = g_point[1]*9
                b_score = g_point[2]*9
            else:
                r_score = len([v for v in o_boxes.values() if v == 1])
                b_score = len([v for v in o_boxes.values() if v == 2])

            outcome = r_score - b_score if me == 1 else b_score - r_score
            total_score += outcome

        expectaion = float(total_score)/ROLLOUTS

        if expectaion > best_expectation:
            best_expectation = expectaion
            best_move = move

        board.next_state(state, best_move)
#What is the ROLLOUT suppossed to be?
    return state


def backpropagate(node: MCTSNode|None, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    pass

def ucb(node: MCTSNode, is_opponent: bool):
    """ Calcualtes the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    """
    total_visits = 0
    for child in node.child_nodes.values():
        total_visits += child.visits
    winrate = (1 - node.wins/node.visits) if is_opponent else node.wins/node.visits
    value = winrate + explore_faction * sqrt(log(total_visits) / node.visits)

    return value

def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree

    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    
    """
    pass

def is_win(board: Board, state, identity_of_bot: int):
    # checks if state is a win state for identity_of_bot
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1

def think(board: Board, current_state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        current_state:  The current state of the game.

    Returns:    The action to be taken from the current state

    """
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
        state = current_state
        node = root_node

        # Do MCTS - This is all you!
        # ...
        expand_leaf(traverse_nodes(node, board, state, bot_identity))

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_action = get_best_action(root_node)
    
    print(f"Action chosen: {best_action}")
    return best_action
