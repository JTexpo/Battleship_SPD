from typing import List
import asyncio

import matplotlib.pyplot as plt

import pyscript
from pyscript import Element, display

from battleship_spd import ai
from battleship_spd.game import BattleshipGame, EMPTY_TILE_ID

PLAYER_HTML_ELEMENTS: List[List[Element]] = []
AI_HTML_ELEMENTS: List[List[Element]] = []
BATTLESHIP_GAME: BattleshipGame = BattleshipGame()
BATTLESHIP_GAME.set_random_board(player_id=1)
BATTLESHIP_GAME.set_random_board(player_id=2)

AI_GRAPH_ID:str = "ai-mind-graph"
AI_MIND_GRAPH_ELEMENT = Element(AI_GRAPH_ID)

is_ai_turn: bool = False
lock_actions: bool = True
figure, axis = plt.subplots()
subplot = figure.add_subplot(111)

# CREATING HTML ELEMENTS
# ----------------------
for row in range(10):
    PLAYER_HTML_ELEMENTS.append([])
    AI_HTML_ELEMENTS.append([])
    for column in range(10):
        PLAYER_HTML_ELEMENTS[row].append(Element(f"player_board_{row}_{column}"))
        AI_HTML_ELEMENTS[row].append(Element(f"ai_board_{row}_{column}"))


def plot_graph():
    global BATTLESHIP_GAME, AI_GRAPH_ID, AI_MIND_GRAPH_ELEMENT, figure, subplot

    figure.clear()
    subplot = figure.add_subplot(111)

    ai_heat_map_board, _, _ = ai.find_best_move(
        board=BATTLESHIP_GAME.get_view_board_opponent(opponent_id=1),
        ship_lengths=[
            len(ship["tiles"])
            for ship_id, ship in BATTLESHIP_GAME.player_1_pieces.items()
            if not ship["is_sank"]
        ],
    )
    heatmap = subplot.imshow(ai_heat_map_board, cmap="hot_r", interpolation="nearest")

    cbar = figure.colorbar(heatmap)
    cbar.set_label(
        "Confidence",
        rotation=270,
    )

    subplot.figure.set_facecolor("gray")
    subplot.figure.suptitle("AI Move View")
    subplot.tick_params(
        axis="x",
    )
    subplot.tick_params(
        axis="y",
    )
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)

    AI_MIND_GRAPH_ELEMENT.clear()
    display(figure, target=AI_GRAPH_ID)


async def sync_backend_to_frontend() -> None:
    global BATTLESHIP_GAME
    for row in range(10):
        for column in range(10):
            if BATTLESHIP_GAME.player_1_board[row][column].is_hit:
                PLAYER_HTML_ELEMENTS[row][column].element.style = (
                    "background-image:url(./assets/images/water_hit.jpeg); background-size:cover;"
                    if BATTLESHIP_GAME.player_1_board[row][column].ship_id
                    == EMPTY_TILE_ID
                    else "background-image:url(./assets/images/ship_hit.jpeg); background-size:cover;"
                )
            else:
                PLAYER_HTML_ELEMENTS[row][column].element.style = (
                    "background-image:url(./assets/images/water.jpeg); background-size:cover;"
                    if BATTLESHIP_GAME.player_1_board[row][column].ship_id
                    == EMPTY_TILE_ID
                    else "background-image:url(./assets/images/ship.jpeg); background-size:cover;"
                )

            if BATTLESHIP_GAME.player_2_board[row][column].is_hit:
                AI_HTML_ELEMENTS[row][column].element.style = (
                    "background-image:url(./assets/images/water_hit.jpeg); background-size:cover;"
                    if BATTLESHIP_GAME.player_2_board[row][column].ship_id
                    == EMPTY_TILE_ID
                    else "background-image:url(./assets/images/ship_hit.jpeg); background-size:cover;"
                )
            else:
                AI_HTML_ELEMENTS[row][column].element.style = "background-image:url(./assets/images/water.jpeg); background-size:cover;"
                    
    plot_graph()


def select_tile(row: int, column: int):
    global BATTLESHIP_GAME, is_ai_turn, lock_actions

    if is_ai_turn or lock_actions:
        return
    
    go_again = BATTLESHIP_GAME.fire_at_tile(opponent_id=2, x_position=column, y_position=row)

    lock_actions = True
    is_ai_turn = not go_again

def reset():
    global BATTLESHIP_GAME, is_ai_turn, lock_actions

    BATTLESHIP_GAME = BattleshipGame()

    BATTLESHIP_GAME.set_random_board(player_id=1)
    BATTLESHIP_GAME.set_random_board(player_id=2)

    is_ai_turn = False
    lock_actions = True

async def main():
    global BATTLESHIP_GAME, is_ai_turn, lock_actions
    while True:

        if is_ai_turn and not lock_actions:

            _, column, row = ai.find_best_move(
                board=BATTLESHIP_GAME.get_view_board_opponent(opponent_id=1),
                ship_lengths=[
                    len(ship["tiles"])
                    for ship_id, ship in BATTLESHIP_GAME.player_1_pieces.items()
                    if not ship["is_sank"]
                ],
            )
            is_ai_turn = BATTLESHIP_GAME.fire_at_tile(opponent_id=1, x_position=column, y_position=row)
            lock_actions = True        

        if lock_actions:
            await sync_backend_to_frontend()
            lock_actions = False
        
        await asyncio.sleep(0.5)

    
pyscript.run_until_complete(main())