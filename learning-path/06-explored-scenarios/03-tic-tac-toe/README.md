# The Tic-Tac-Toe scenario
## Scenario description
We tried to train an agent in order to learn how to play Tic-tac-toe against a simulated player. The agent would fill the role of player 1 whereas the environment would simulate player 2 that played randomly.

## State definition
The state of the game could be defined as just the current status of the board (which player is occupying each space).

However, other variables were added in order to provide more information to help in the calculation of the reward function:
* repeated_move: Boolean value indicating if the last move was invalid (trying to use an occupied space).
* winner: The winner of the match (if it has been decided yet).
* num_available_numbers: Amount of moves available to the agent.

```
type TicTacToeValue Number.Int8<player2 = -1, empty = 0, player1 = 1>
type Board TicTacToeValue[3][3]

type GameState { 
    board: Board,   
    repeated_move: Number.Bool,
    winner: TicTacToeValue,
    num_available_moves: number
}
```

## Action definition
The action that the agent can take is deciding on which of the 9 spaces of the board to put its next mark:
```
type Move Number.Int8<1, 2, 3, 4, 5, 6, 7, 8, 9> 

type Action {
    move: Move
}
```

## Reward function
Multiple reward functions were tried, below you can see one of them in which winning is rewarded and losing or making invalid moves is penalized:
```
type TicTacToeValue Number.Int8<player2 = -1, empty = 0, player1 = 1>

function Reward(obs: GameState, act: Action) {
    if(obs.repeated_move) {
        return -50
    } else if(obs.winner == TicTacToeValue.player1) { 
        # If win player 1 (bonsai) positive reward  
        return 100
    } else {
        return 0
    }
}

function Terminal(obs:GameState, act: Action){
    return obs.repeated_move or obs.num_available_moves == 0 or
obs.winner != TicTacToeValue.empty
}
```

## Results
After trying to train the model with this reward function we did not manage to make the agent play tic-tac-toe correctly. The model continued executing invalid moves and no significant improvements were possible after trying multiple variants of the reward function.

## Conclusion
This example shows that the techniques used by the Bonsai platform are not always able to adapt to every possible scenario. In this case, we believe that having an opponent player that uses random moves makes it hard for the agent to learn how to play since the evolution of the state does not only depend on the previous state and the agent’s action but also on factors (the other player’s moves) outside of the control of the agent.

[Continue reading..](../../07-issues-and-limitations/README.md)
