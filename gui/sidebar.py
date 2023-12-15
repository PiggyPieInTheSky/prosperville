# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines GUI elements in the side bar area of the game
"""

from ipywidgets import GridBox, Layout, HTML, Label
import gui._shared as ui # shared items across front end
from backend.prosperville import crntGame # loads the backend.Prosperville object that represents the current running game

# the following three lines the defines the display area of the user stats. This is the are that sits on the top half of the side bar
# read the html file as a template to instruct how the player stats should be displayed
with open('gui/html/player_stats.html','r') as f:
    stats_template = f.read()
# define the widget that displays the player attributes
htmlCrntPlayerStats = HTML(value=stats_template, layout=Layout(grid_area='htmlCrntPlayerStats'))

# the rest of the file until tblSideBarArea defines the player ranking display area
# define the column names of the player ranking table
rank_table_columns = ['#', 'Score', 'Equity', 'Debt']
# these two holds the UI elements that sit in each cell of the ranking table. 
# They both have the same UI elements, but are organized differently. 
# lstRankLabelUIs2D is a list of lists. 
# The UI is properly placed in lstRankLabelUIs2D[iRow][iCol] based on the cell (iRow, iCol) the UI occupies in the table
# lstRankLabelUIs is a one-dimensional list that lays out all UIs in lstRankLabelUIs2D in a linear fashion
lstRankLabelUIs2D = []; lstRankLabelUIs = []
for iRow in range(crntGame.n_players+1): # loop through all human players
    player_labels = [] # represents a row, or the content to be saved in one spot of lstRankLabelUIs2D at the first dimension.
    for iCol in range(len(rank_table_columns)): # loop through each column of the ranking table
        # create a label widget, it will show the value of the cell. initially, it just displays the column name upon creation
        crntLabel = Label(rank_table_columns[iCol], layout=Layout(grid_area=f'lbl_player_rank_r{iRow}_c{iCol}'))
        # add the UI to the proper list
        player_labels.append(crntLabel)
        lstRankLabelUIs.append(crntLabel)
    # place the whole row of labels to the end of lstRankLabelUIs2D
    lstRankLabelUIs2D.append(player_labels)

# defines the display element for the tile above the ranking table that reads "Player Ranking"
htmlRankHeader = HTML(value='<p style="font-weight: bold; line-height: 12px; margin:0px 0px 4px 0px; vertical-align: bottom; text-decoration: underline;">Player Ranking</p>', layout=Layout(grid_area='sidebar_htmlRankHeader'))
# defines the ranking table, and places all the labels that are supposed to be in the cells of the ranking table into the ranking table. 
# This also places the table title (htmlRankHeader) into the first row. The first row spans all columns. 
# The whole table has 1 row for the title, 1 row for the header, and value rows whose quantity equals to number of human players in the game.
tblPlyrRank = GridBox(children=lstRankLabelUIs+[htmlRankHeader]
                     , layout=Layout(
                         grid_area='tblPlyrRank'
                         , grid_template_rows='32px' + ' '.join(["auto"] * (crntGame.n_players+1))
                         , grid_template_columns=' '.join(['auto']*len(rank_table_columns))
                         , grid_template_areas= '"'+ ' '.join([f'{htmlRankHeader.layout.grid_area}']*len(rank_table_columns)) + '"\n' + '\n'.join(['"'+ ' '.join([crntLbl.layout.grid_area for crntLbl in lstRankLabelUIs2D[i]]) + '"' for i in range(crntGame.n_players+1)])
                     )
                    ) 
             

# define the side bar display area. It is a table with two rows. 
# The first row has the player attribute display area (htmlCrntPlayerStats). 
# The second row has the player ranking table (tblPlyrRank). 
# This is the widget that gets to be displayed in the playground (playground.py).
tblSideBarArea = GridBox(children=[htmlCrntPlayerStats, tblPlyrRank]
                      , layout=Layout(
                            grid_area='tblSideBarArea' #name the current object so the parent grid can recognize it in layout.grid_template_areas
                            , grid_template_rows="160px auto" # 2 rows
                            , grid_template_columns="auto" # 1 column, 100% allotted space given by the parent object
                            , grid_template_areas=f"""
                                "{htmlCrntPlayerStats.layout.grid_area}"
                                "{tblPlyrRank.layout.grid_area}"
                            """ # place the child widgets
                            , height=f'{int(ui.HeightPlayground[:-2])+24}px'
                            , align_content = 'flex-start' # vertical alignment if oversized
                            , align_items = 'flex-start'
                            , border_left = 'solid 1px'
                            , padding='4px 4px 4px 4px'
                        )
             )

def refresh_sidebar():
    """Renders / refreshes UI elements in the side bar display area"""

    # refreshes user stats of the current player in the game if the player is not AI
    if not crntGame.crntPlayer.is_system:
        htmlCrntPlayerStats.value = stats_template.format(iplyr=crntGame.iPlayer+1 # player number
                                                          , hpns=crntGame.crntPlayer.happiness # player happiness score
                                                          , incm=crntGame.crntPlayer.income # player income
                                                          , spnd=crntGame.crntPlayer.spending # player spending
                                                          , debt_std=crntGame.crntPlayer.debt_std # player student debt amount
                                                          , debt_car=crntGame.crntPlayer.debt_car # player car debt amount
                                                          , debt_mort=crntGame.crntPlayer.debt_mort # player mortgage debt amount
                                                          , debt_other=crntGame.crntPlayer.debt_other # player debt amount for all other types of debt. should be zero.
                                                         )
    # display player ranking table based on the ranking provided by the backend game object crntGame.
    for i in range(crntGame.n_players): # loop through each spot on the ranking table. this is also the ranking order
        iRow = i+1 # get the row number in the table for the current ranking order. this is the row we will update
        iPlyr = crntGame.ranked_players[i] # find the player index for the current ranking order
        crntPlayer = crntGame.players[iPlyr] # find the player object for the current ranking order
        bankrupt_asterisk = '*' if crntPlayer.bankrupt else '' # add an asterisk to the player number (iPlyr+1) if the play is bankrupt
        
        # update the row of the ranking table
        lstRankLabelUIs2D[iRow][0].value=str(iPlyr+1)+bankrupt_asterisk # player number
        lstRankLabelUIs2D[iRow][1].value='{:,.0f}'.format(crntPlayer.score) # player score
        lstRankLabelUIs2D[iRow][2].value='{:,.0f}'.format(crntPlayer.equity) # player equity
        lstRankLabelUIs2D[iRow][3].value='{:,.0f}'.format(crntPlayer.debt) # player debt

        # add the row background color based on the color assigned to the player
        for icol in range(len(rank_table_columns)):
            lstRankLabelUIs2D[iRow][icol].style.background = ui.player_colorwheel[iPlyr % len(ui.player_colorwheel)]
        
# refresh all GUI elements in the side bar display area upon the first loading of this file
refresh_sidebar()

