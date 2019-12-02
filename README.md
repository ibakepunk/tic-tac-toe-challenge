# Anaconda: Tic-Tac-Toe Coding Challenge
Your mission, should you choose to accept it, is to implement a two-player game of Tic-tac-toe in the web browser.

## Rules

HONOR RULES: You must do this challenge on your own, without assistance or review from others, and without copying from the Internet. You will be asked to affirm that you developed your work independently.

TIME LIMIT: You have 3 days from the date you receive a link to this site. You may submit your work earlier.

TASK: Your task it implement a simple but comprehensive REST API for a [tic-tac-toe game](https://en.wikipedia.org/wiki/Tic-tac-toe)

## Requirements

The basic requirements for the game are:

store a game board data structure that contains the game information
allow two players to enter their names, and automatically assign one of them the circle and the other the 'x'allow each to play a turn, one at a time, during which the player selects a square of the board and it is filled in with their symbol
indicate when one of the players has won, or the game is a draw
In addition to implementing basic gameplay, the user must be able to save their game to the server.

Since this is a coding challenge, the success of your mission depends on building a good rest API implementation. 

Make sure to provide instruction about how to setup, run and consume your REST API.

## Technologies

We prefer Python and the tornado framework, but they are not required. You can use whatever technology you prefer.

Game data structure
A game consists of:

two players, represented by their names as strings
a board data structure (we are leaving you the choice of what data structure is more appropriate for the task). Keep in mind that this data structure needs to trak the status of each board element. Each element is null if the square is blank, or either 0 or 1 to indicate which player controls the square. 

Server API

- `GET /api/games`: Return a list of the Games known to the server, as JSON.
```json
{
    "objects": [
        {
            "id": 1,
            "status": "in_progress",
            "updated_by": "karl",
            "x_player": "karl",
            "o_player": "paul",
            "board": [["x", null, null],
                      [null, "o", null],
                      [null, "x", null]
            ]
        },
        {
            "id": 2,
            "status": "in_progress",
            "updated_by": "bob",
            "x_player": "alice",
            "o_player": "bob",
            "board": [[null, null, null],
                      [null, null, null],
                      [null, null, null]
            ]
        }
    ],
    "count": 2
}
```

- `POST /api/games`: Create a new `Game`, assigning it an ID and returning the newly created `Game`. To start a new game one must send the players names. The first name in the list plays Xs.

Request payload:
```json
{"players": ["karl", "paul"]}
```
Response:
```json
{
    "id": 2,
    "status": "in_progress",
    "updated_by": "bob",
    "x_player": "alice",
    "o_player": "bob",
    "board": [[null, null, null],
              [null, null, null],
              [null, null, null]]
}
```
- `GET /api/games/<id>`: Retrieve a `Game` by its ID, returning a `404` status
  code if no game with that ID exists.
```json
{
    "id": 1,
    "status": "in_progress",
    "updated_by": "karl",
    "x_player": "karl",
    "o_player": "paul",
    "board": [["x", null, null],
              [null, "o", null],
              [null, "x", null]]
}
```

- `POST /api/games/<id>`: Update the `Game` with the given ID, replacing its data with the newly `POST`ed data. To make a turn player must send their username and an updated board with player's mark (X or O).

Request payload:
```json
{
    "updated_by": "karl",
    "board": [["x", null, null],
              [null, null, null],
              [null, null, null]]
}
```
Response:
```json
{
    "id": 1,
    "status": "in_progress",
    "updated_by": "karl",
    "x_player": "karl",
    "o_player": "paul",
    "board": [["x", null, null],
              [null, null, null],
              [null, null, null]]
}
```

### Statuses
There are several possible statuses of the game:
- `in_progress` indicates that the game is not finished yet.
- `draw` indicates that the game is finished in a draw.
- `x` and `o` mean that the game is over and specify the winner.

## Running the app
In order to run the API you're going to need docker-compose installed. There are two containers: `python` runs the Django app and `postgres` stores the game data.
- `make run` to start the containers and apply initial migrations. The app is ready to use.
- `docker-compose exec python ./manage.py test game.tests` to run the tests.