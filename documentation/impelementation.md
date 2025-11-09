# Implementation document
(Draft)

## Program flow
```mermaid
stateDiagram-v2
    [*] --> UI
    state UI {
        [*] --> userInput
        userInput: Get user input
        checkWin: Check if player wins
        userInput --> checkWin
        state if_state <<choice>>
        checkWin --> if_state
        if_state --> playerWins: player has 5 pieces in row
        if_state --> continueGame: player doesn't have 5 pieces in row
        playerWins --> [*]
        continueGame: Game continues
        playerWins: Player wins
        checkWin2: Check if player wins
        state if_state2 <<choice>>
        checkWin2 --> if_state2
        if_state2 --> playerWins2: player has 5 pieces in row
        if_state2--> continueGame2: player doesn't have 5 pieces in row
        playerWins2 --> [*]
        playerWins2: Player wins
        continueGame2: Game continues
        continueGame2 --> userInput
    }

    continueGame --> Minimax: Get next move from AI. Input current game board and latest move
    Minimax: Minimax
    state Minimax {
        [*] --> moveCandidate
        moveCandidate: Create table of possible moves (AI)
        moveCandidate --> moveCandidateDepth: loop through possible moves.
        moveCandidateDepth: Create table of possible moves of next layer (user)
        moveCandidateDepth --> moveCandidateDepth2: loop through possible moves.
        moveCandidateDepth2: Create table of possible moves of next layer (AI)
        moveCandidateDepth2 --> moveEval2: There can be multiple more similar layers. Time limits the amount of layers.
        moveEval2: Evaluate moves statically
        moveEval2 --> moveEval1
        moveEval1: Select best move (user)
        moveEval1 --> moveEval
        moveEval: Select best move (AI)
        moveEval --> [*]
    }
    Minimax --> checkWin2: Return AIs next move
```
