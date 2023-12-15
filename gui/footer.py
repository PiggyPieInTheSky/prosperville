# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines GUI elements in the footer area of the game
"""

from ipywidgets import GridBox, Layout, Button, ButtonStyle, HBox
from backend.prosperville import crntGame # loads the backend.Prosperville object that represents the current running game
import gui._shared as ui # shared items across front end

# the following 4 methods are called when one of the following buttons is called: back button, next button, learning tip button, dashboard button.
def btnBack_on_click(b):
    crntGame.back() # instruct the game backend to step backward once
    refresh_gui()

def btnNext_on_click(b):
    crntGame.next() # instruct the game backend to step forward once
    refresh_gui()

def btnlearningtip_on_click(b):
    if ui.DisplayMode != 1: # if we are currently not displaying knowledge page
        ui.DisplayMode = 1 # set the display mode indicator to show the knowledge page
    else: # if we are currently displaying the knowledge page
        ui.DisplayMode = 0 # set the display mode indicator to show life stage area
    # render all gui pages / areas according to the display mode indicator
    refresh_gui()

def btnDashboard_on_click(b):
    if ui.DisplayMode != 2: # if we are currently not displaying dashboard page
        ui.DisplayMode = 2 # set the display mode indicator to show the dashboard page
    else: # if we are currently displaying the dashboard page
        ui.DisplayMode = 0 # set the display mode indicator to show life stage area
    # render all gui pages / areas according to the display mode indicator
    refresh_gui()

# define the back button
btnBack = Button(description='<< Back', disabled=True
                 , layout=Layout(width='auto', grid_area='btnBack', margin='0px 8px 0px 0px')
                 , style=ButtonStyle(button_color='olive'))
btnBack.on_click(btnBack_on_click)

# define the next button
btnNext = Button(description='Next >>'
                 , layout=Layout(width='auto', grid_area='btnNext', margin='0px 20px 0px 0px')
                 , style=ButtonStyle(button_color='green'))
btnNext.on_click(btnNext_on_click)

# define the learning tip button
btnLearningTip = Button(description='Learning Tips'
                 , layout=Layout(width='auto', grid_area='btnLearningTip', margin='0px 20px 0px 0px')
                 , style=ButtonStyle(button_color='green'))
btnLearningTip.on_click(btnlearningtip_on_click)

# define the dashboard button
btnDashboard = Button(description='Dashboard'
                 , layout=Layout(width='auto', grid_area='btnDashboard', margin='0px 0px 0px 0px')
                 , style=ButtonStyle(button_color='olive'))
btnDashboard.on_click(btnDashboard_on_click)

# define a horizontal box that holds all the buttons, lines them up next to each other
hbxFooter = HBox([btnBack, btnNext,btnLearningTip,btnDashboard]
                 , layout=Layout(grid_area='hbxFooter')
            )

# defines the footer area. it contains the horizontal box that has all the buttons.
tblFooterArea = GridBox(children=[hbxFooter]
                      , layout=Layout(
                            grid_area='tblFooterArea' #name the current object so the parent grid can recognize it in layout.grid_template_areas
                            , grid_template_rows="auto" # 1 row, 100% allotted space given by the parent object
                            , grid_template_columns="auto" # 1 column, 100% allotted space given by the parent object
                            , grid_template_areas=f"""{hbxFooter.layout.grid_area}""" # place the child widgets
                            , height=ui.HeightFooter
                            , justify_content = 'flex-start' # horizontal alignment
                            , align_content = 'center' # vertical alignment
                            , border_top = 'solid 1px'
                            , padding='0px 4px 0px 4px'
                        )
             )

# these two lists help us display UI elements properly. see details in refresh_gui function.
button_group = [[btnBack,btnNext], [btnLearningTip],[btnDashboard]]
visibility_values = ['hidden', 'visible']

def refresh_gui():
    """Renders the entire GUI"""

    from gui.header import refresh_header # load header refresh function
    from gui.playground import refresh_playground  # load playground refresh function
    from gui.sidebar import refresh_sidebar  # load sidebar refresh function

    # change button enability based on game progression
    btnBack.disabled = not crntGame.can_step_back
    btnNext.disabled = crntGame.is_end
    
    # if the game reached the end
    if crntGame.is_end: 
        from gui.msgbox import show_message # load the method to display the message area
        
        # determines what message to display based on how the player ranks.
        if crntGame.n_players_survived ==0:
            show_message('Game Ended', 'All players went bankrupt:( \n\nPlease click "OK" to see score.', next_mode=2)
        else:
            # find highest ranked non-bankrupt player
            for i in crntGame.ranked_players:
                if not crntGame.players[i].bankrupt:
                    break
            if crntGame.n_players == 1:
                if crntGame.players[0].score > crntGame.players[-1].score:
                    show_message('{0} is the winner!'.format(crntGame.players[i].name), 'Congratulations! \n\nYou beat AI! \n\nPlease click "OK" to see score.', next_mode=2)
                else:
                    show_message('Game Ended'.format(crntGame.players[i].name), 'Congratulations! \n\nYou built wealth and did not go bankrupt! \n\nPlease click "OK" to see score details.', next_mode=2)
            else:
                show_message('{0} is the winner!'.format(crntGame.players[i].name), 'Congratulations! \n\nPlease click "OK" to see scores and compare to AI.', next_mode=2)

    # refreshes the GUI areas
    refresh_header()
    refresh_playground()
    refresh_sidebar()
    
    # change button face based on display mode
    if ui.DisplayMode == 1: # currently displaying knowledge tips
        btnLearningTip.description = 'Return'
    else:
        btnLearningTip.description = 'Learning Tips'
        
    if ui.DisplayMode == 2: # currently displaying dash board
        btnDashboard.description = 'Return'
    else:
        btnDashboard.description = 'Dashboard'

    # change button visibility based on the display mode
    if ui.DisplayMode != 0: # if currently not displaying game play area, only show the button tied to the display area
        for ibtn_group in range(len(button_group)):
            visibility_value = visibility_values[int(ibtn_group == ui.DisplayMode)]           
            for crntBtn in button_group[ibtn_group]:
                    crntBtn.layout.visibility = visibility_value
    else: # if currently not displaying game play area, show all buttons
        for ibtn_group in range(len(button_group)):
            for crntBtn in button_group[ibtn_group]:
                crntBtn.layout.visibility = 'visible'

    if crntGame.is_end: 
        btnDashboard.layout.visibility = 'hidden'
        
    

