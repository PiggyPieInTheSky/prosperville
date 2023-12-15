# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.

"""This file defines GUI elements in the header area of the game
"""
from ipywidgets import GridBox, Layout, Label, HBox
from backend.prosperville import crntGame # loads the backend.Prosperville object that represents the current running game
import gui._shared as ui # shared items across front end

# label to display current life stage
lblStageCt_ha = Label(f"Life Stage: {crntGame.iStage+1}/{crntGame.n_stages} {crntGame.crntStage.title}"
                        , layout=Layout(width='500px'
                                        , border_right='solid 1px')
                        , style={'background':ui.player_colorwheel[0]}
                     ) 
# lblStageCt_ha.style.background = '#A5DA46'

# label to display current turn number
lblTurnCt_ha = Label(f"Turn: {crntGame.iTurn+1}/{crntGame.n_turns}"
                     , layout=Layout(width='200px'
                                     , border_right='solid 1px')
                     , style={'background':ui.player_colorwheel[0]}
                    )
# lblTurnCt_ha.style.background = '#A5DA46'

# label to display current player's name
lblCrntPlayerName_ha = Label(f"Player: {crntGame.crntPlayer.name}"
                            , layout=Layout(width='2080px')
                            , style={'background':ui.player_colorwheel[0]}
                        ) 
# lblCrntPlayerName_ha.style.background = '#A5DA46'

# this horizontal box strings all GUI widgets together
hbxHeader = HBox([lblStageCt_ha,  lblTurnCt_ha, lblCrntPlayerName_ha]
                 , layout=Layout(grid_area='hbxHeader')
            )

# this is the grid that has everything in
tblHeaderArea = GridBox(children=[hbxHeader]
                        , layout=Layout(
                            grid_area='tblHeaderArea' #name the current object so the parent grid can recognize in layout.grid_template_areas
                            , grid_template_rows="auto" # 1 row, 100% allotted space given by the parent object
                            , grid_template_columns="auto" # 1 column, 100% allotted space given by the parent object
                            , grid_template_areas="""hbxHeader""" # place the child widgets
                            , height=ui.HeightHeader
                            , justify_content = 'flex-start' # horizontal alignment
                            , align_content = 'flex-start' # vertical alignment
                            , border_bottom = 'solid 1px'
                        
                        )
               )
tblHeaderArea.background = '#A5DA46'

def refresh_header():
    """Renders the header area"""

    # set the stage and turn display areas
    lblStageCt_ha.value = f'Life Stage: {crntGame.iStage+1}/{crntGame.n_stages} {crntGame.crntStage.title}'
    lblTurnCt_ha.value = f'Turn: {crntGame.iTurn+1}/{crntGame.n_turns}'

    # set the current player area
    if crntGame.is_end:
        lblCrntPlayerName_ha.value = 'Game Ended'
    elif crntGame.is_random_event_step:
        lblCrntPlayerName_ha.value = 'Random Event'
    elif crntGame.crntEvent is None:
        lblCrntPlayerName_ha.value = 'Life Stage'
    else:
        lblCrntPlayerName_ha.value = f'Player: {crntGame.crntPlayer.name}'
    
    # assigning header color based on the color on the color wheel according to the player who's currently playing
    # Separate aesthetics is made for the AI player
    if crntGame.crntPlayer.is_system or crntGame.is_end: # if AI player or the game is ended
        lblCrntPlayerName_ha.style.background = '#F9F6FC'
        lblTurnCt_ha.style.background = '#F9F6FC'
        lblStageCt_ha.style.background = '#F9F6FC'
    else: # if human player and the game is not ended
        lblCrntPlayerName_ha.style.background = ui.player_colorwheel[crntGame.iPlayer % len(ui.player_colorwheel)]
        lblTurnCt_ha.style.background = ui.player_colorwheel[crntGame.iPlayer % len(ui.player_colorwheel)]
        lblStageCt_ha.style.background = ui.player_colorwheel[crntGame.iPlayer % len(ui.player_colorwheel)]
        

