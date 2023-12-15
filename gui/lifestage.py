# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines GUI elements for the main area when game is in play. 
"""
from ipywidgets import GridBox, Layout, Label, HBox, VBox, HTML
import gui._shared as ui # shared items across front end
from gui.uiLifeEvent import uiLifeEvent # GUI element for an event option
from backend.prosperville import crntGame # loads the backend.Prosperville object that represents the current running game

# this function registers user selected choice to the back end via event hook uiLifeEvent.on_select
def uiLifeEvent_on_select(b):
    crntGame.crntPlayer.choices[b.parentEventObj.evtDef.name] = b.parentEventObj.iChoice

# life stage title
lblStageTitle = Label('Life Stage Title'
                        , style={'font_size':'18px', 'font_weight':'bold'}
                        , layout=Layout(grid_area='lifestage_lblStageTitle'
                                      
                                     ))
# life stage description
htmlStageDesc = HTML() 
# choice tag line
lblStageChoiceTitle = Label('Life Stage Choices 1/5'
                            , style={'font_size':'12px'}
                            , layout=Layout(grid_area='lifestage_lblStageChoiceTitle', margin='0px 0px 0px 16px'))

vbxStageText = VBox([HBox([lblStageTitle, lblStageChoiceTitle], layout=Layout(align_items = 'flex-end')), htmlStageDesc], layout=Layout(grid_area='lifestage_vbxStageText'))

# a string to hold grid_area values for all event UI elements, delimited by white space. 
# this is used to put all event UI elements in the event holding area tblEvtArea
event_grid_names = ''

# load all event UI elements
for evtDefName in crntGame.event_by_name: # loop through each live stage event name
    # create a life stage event UI based on the current event definition
    crntUIEvent = uiLifeEvent(crntGame.event_by_name[evtDefName], on_select=uiLifeEvent_on_select)
    # index the UI to this dictionary by its event name so we can find it later when we want to make visibility changes
    ui.event_by_name[evtDefName] = crntUIEvent
    # hide this event UI 
    crntUIEvent.layout.visibility = 'hidden'
    # string this event UI's grid_area value
    event_grid_names+= ' ' + crntUIEvent.layout.grid_area

# display the first event UI
ui.event_by_name[crntGame.crntEvent.name].layout.visibility = 'visible'
# mark the event UI associated with the current event name as current
ui.crntEventUI = ui.event_by_name[crntGame.crntEvent.name]

# define a holding area for all life stage event UI
# for some reason, we need a dedicated 1x1 grid to hold overlapping items.
# we load all these UI elements into the holding area, and only make visible one element at any time.
tblEvtArea = GridBox(children=list(ui.event_by_name.values())
                        , layout=Layout(grid_area='lfstg_tblEvtArea'
                                        # the holding area is a grid box with 1 row and 1 column
                                        , grid_template_rows='auto', grid_template_columns="auto"
                                        # the content of the only cell of the table is all the event UI elements
                                        , grid_template_areas=f'{event_grid_names}')
                    )

# define the life stage page. T
# his page is one of the pages that can show in the playground. 
tblLifeStagePage = GridBox(children=[vbxStageText, tblEvtArea]
                            , layout=Layout(
                                #name the current object so the parent grid can recognize it in layout.grid_template_areas
                                grid_area='tblLifeStagePage'
                                # two rows. first 1 with 32 px height. second one takes the remaining height of the parent container (gui.playground.tblMainArea). 
                                , grid_template_rows="auto auto"
                                # 1 column, 100% allotted space given by the parent object
                                , grid_template_columns="auto" 
                                # defines how to place the UI elements
                                , grid_template_areas=f"""
                                    "{vbxStageText.layout.grid_area}"
                                    "{tblEvtArea.layout.grid_area}"
                                    """ 
                                , height=ui.HeightPlayground
                                , justify_content = 'flex-start' # horizontal alignment
                                , align_content = 'flex-start' # vertical alignment
                            )
                 )


def refresh_lifestage():
    """Renders the lifestage area based on all game attributes."""

    # hide the current event UI
    ui.crntEventUI.layout.visibility = 'hidden'
    
    if tblLifeStagePage.layout.visibility == 'hidden':
        return

    # display the life stage title and description
    lblStageTitle.value = crntGame.crntStage.title
    htmlStageDesc.value = '<p style="word-wrap:break-word; margin:0px; line-height:16px">'+ crntGame.crntStage.desc.replace('\n','<br/>') +'</p>'
    
    if crntGame.crntEvent is not None:
        # find the new event UI
        crntEvntUI = ui.event_by_name[crntGame.crntEvent.name]
        # show the new event UI, and mark it as current
        crntEvntUI.layout.visibility = 'visible'
        ui.crntEventUI = crntEvntUI
    
    # update the life stage page title
    if crntGame.is_random_event_step:
        lblStageChoiceTitle.value = 'Random Event {0}/{1}'.format(
            crntGame.step_table['ievent_in_stage'][crntGame.iStep]+1
            , crntGame.crntStage.n_random_event_turn
        )
    elif crntGame.crntEvent is None:
        lblStageChoiceTitle.value = ''
    else:
        lblStageChoiceTitle.value = 'Life Stage Choices {0}/{1}'.format(
        crntGame.step_table['ievent_in_stage'][crntGame.iStep]+1
        , len(crntGame.crntStage.life_event_seq)
    )
    if crntGame.crntOptionAvailability is not None:
        crntEvntUI.OptionAvailability = crntGame.crntOptionAvailability

    if ui.crntEventUI.has_options == False:
        return

    # display the selected choice
    iTentativeChoice = 0
    if ui.crntEventUI.evtDef.name in crntGame.crntPlayer.choices:
        # if the current player has made their choice already for the event, make this choice a tentative choice
        iTentativeChoice = crntGame.crntPlayer.choices[ui.crntEventUI.evtDef.name]
    # check if the tentative choice is actually available. Unavailability may happen when a player goes back to change their previous choice and causes the availablity chagne for downstream options.
    if crntGame.crntOptionAvailability[iTentativeChoice] == False:
        # if the tentative choice is not available, loop to find the first availiable choice as the default choice
        for iTentativeChoice in range(len(crntGame.crntOptionAvailability)):
            if crntGame.crntOptionAvailability[iTentativeChoice]:
                break
            
    ui.crntEventUI.iChoice = iTentativeChoice # default to the first available option of the event
    # add default choice for the player
    crntGame.crntPlayer.choices[ui.crntEventUI.evtDef.name] = iTentativeChoice

# refresh all GUI elements in the life stage display area upon the first loading of this file
refresh_lifestage()

