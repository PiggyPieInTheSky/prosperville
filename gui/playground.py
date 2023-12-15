# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines GUI elements in the main game area that we may also refer to as the playground
"""
from ipywidgets import GridBox, Layout
from gui.lifestage import tblLifeStagePage # main playing area
from gui.knowledge import tabKnowlege # display area of learning tips
from gui.dashboard import tabDashBoard # display area of the dashboard
from gui.msgbox import vbxMsg # display area of message box
import gui._shared as ui # shared items across front end

# use a table widget to render the playground. The playground has 4 "pages" as children. 
# At any given time, only one of them is displayed / visible.
tblMainArea = GridBox(children=[tblLifeStagePage,tabKnowlege,tabDashBoard, vbxMsg]
                      , layout=Layout(
                            grid_area='tblMainArea' #name the current object so the parent grid can recognize it in layout.grid_template_areas
                            , grid_template_rows="auto" # 1 row, 100% allotted space given by the parent object
                            , grid_template_columns="auto" # 1 column, 100% allotted space given by the parent object
                            # we are placing two areas within the same cell. however, only one will be visible at any time.
                            , grid_template_areas=f"""{tblLifeStagePage.layout.grid_area} {tabKnowlege.layout.grid_area} {tabDashBoard.layout.grid_area} {vbxMsg.layout.grid_area}""" 
                            , justify_content='flex-start' # horizontal alignment
                            , align_content='flex-start' # vertical alignment
                            , align_items='flex-start'
                            , padding = '10px'
                        )
             )

def refresh_playground():
    """Renders the playground based on all game attributes."""

    # loads the refresh functions for life stage and dashboard areas
    from gui.lifestage import refresh_lifestage
    from gui.dashboard import refresh_dashboard

    # based on display mode, make visible only one area
    for iPage in range(len(tblMainArea.children)):
        if iPage == ui.DisplayMode:
            tblMainArea.children[iPage].layout.visibility = 'visible'
        else:
            tblMainArea.children[iPage].layout.visibility = 'hidden'
    
    # this needs to be called to hide the event ui if the parent is hidden
    refresh_lifestage()
    
    if ui.DisplayMode == 2:
        refresh_dashboard()

refresh_playground()

