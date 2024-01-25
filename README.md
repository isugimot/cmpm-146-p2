# CMPM 146 P2

### Teammates:
- Ichiro Sugimoto
- Cassidy Aydin

### Modifications to mcts_modified.py:
- During rollout:
  - Take 5 random moves from the legal moves and check if that move will be winning or not.
  - If it is winning, check if it is the enemy's move or not and prioritize it with different points. If we have a move where the enemy is winning more than us, we move on and continue. If the opponent isn't winning, make a random move
