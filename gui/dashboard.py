# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines GUI elements that render the dashboard display area"""

from ipywidgets import Dropdown, Tab, Layout, HTML, VBox
from gui._shared import dataframe2html, HeightPlayground
from backend.prosperville import crntGame # loads the backend.Prosperville object that represents the current running game

# this function is called whenever the player dropdown box on either tab changes its selected value
def dropdown_on_change(chg):
    refresh_dashboard()

def refresh_dashboard():
    """Renders the dashboard display area"""
    
    # update the player choice table to reflect the currently selected player in the choice dropdown box
    htmlChoiceTable.value = dataframe2html(crntGame.players[dpdPlayerChoice.value].choice_table[['Stage','Turn','Random','Event','Choice']], style='border: 1px solid black; border-collapse: collapse; padding:0px 2px 0px 2px; text-align:center;')
    # find the Player object according to the selected player in the score dropdown box
    crntPlayer4Score = crntGame.players[dpdPlayerScore.value]
    # display the scores for the current player
    if crntPlayer4Score.score_table.shape[0] == 0: # if the player is not scored yet (eg first turn of the game)
        htmlScoreTable.value = '<p>Player is not scored yet.</p>'
    else: # if the current player is scored
        # display the player's score table
        htmlScoreTable.value = dataframe2html(crntPlayer4Score.score_table, style='border: 1px solid black; border-collapse: collapse; padding:0px 4px 0px 4px; text-align:center;')
    # display other player basic information on the score tab
    htmlPlayerAtt.value = htmlPlayerAttTemplate.format(name=crntPlayer4Score.name, bankrupt='Yes' if crntPlayer4Score.bankrupt else 'No', score=crntPlayer4Score.score)

# read the player basic info html, use it as a template to instruct how to display the play basic info on the score tab
with open('gui/html/player_att.html','r') as f:
    htmlPlayerAttTemplate = f.read()

# create HTML widgets for the choice and score display
htmlChoiceTable, htmlScoreTable = HTML(), HTML() 
# make a dropdown box for the choice tab to display and make choice of which player is to display
dpdPlayerChoice = Dropdown(options=[(crntGame.players[i].name, i) for i in range(len(crntGame.players))]
                           , value=0
                           , description='Player: '
                          )
# add change logic
dpdPlayerChoice.observe(dropdown_on_change)
# place the dropdown box and the display html widget in a vertical box
vbxChoices = VBox(children=[dpdPlayerChoice, htmlChoiceTable])


# make a dropdown box for the score tab to display and make choice of which player is to display
dpdPlayerScore = Dropdown(options=[(crntGame.players[i].name, i) for i in range(len(crntGame.players))]
                           , value=0
                           , description='Player: '
                          )
# add change logic
dpdPlayerScore.observe(dropdown_on_change)

htmlPlayerAtt = HTML()

# place the dropdown box and the display html widget in a vertical box
vbxScore = VBox(children=[dpdPlayerScore, htmlPlayerAtt, htmlScoreTable])

# defines the dashboard display area. 
# This is the widget that gets to be displayed in the playground (playground.py).
tabDashBoard = Tab(children=[vbxScore, vbxChoices]
                   , titles=['Score','Player Choices']
                   , layout=Layout(grid_area='tabDashBoard', height=HeightPlayground)
                  )

# refresh all GUI elements in the dashboard display area upon the first loading of this file
refresh_dashboard()



