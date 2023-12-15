# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines the UI element that represents an event.

Here we make all the elements into one GUI object with what's called inheritance. 
Inheritance is a mechanism commonly used in object-oriented programming. 
For more information on inheritance, you can refer to https://en.wikipedia.org/wiki/Inheritance_(object-oriented_programming)

By looking at the class definition below, can you tell which class is uiLifeEvent inherited from?
"""

from ipywidgets import Layout, GridBox, Box, Label, HTML, HBox, VBox
from gui.uiOption import uiOption

class uiLifeEvent(GridBox):
    """Represents a UI element for an event."""

    # this is the constructor function of the uiOption class. 
    # for more info on constructor, please refer to https://en.wikipedia.org/wiki/Constructor_(object-oriented_programming)
    def __init__(self, evtDef, on_select=None):
        """Represents a UI element for an event.
        
        Input Argument
        --------------
        evtDef:     required dictionary that contains the event definition. It is an object in backend.design.eventdef.pvEvents.
        on_select:  a function that is called when the select button on an option is clicked. None or callable.
        """

        # save the raw event definition
        self.evtDef = evtDef

        # title of the event
        lblChoiceTitle = Label(evtDef.title
                               , style={'font_size':'14px'}
                               , layout=Layout(grid_area=evtDef.name+'_lblChoiceTitle', margin='0px')
                              )

        # description display
        divDesc = HTML(value= '<p style="word-wrap:break-word; margin:0px; line-height:16px">'+ evtDef.desc.replace('\n','<br/>') +' </p>') 
        
        if self.has_options==False: # if the event has no options
            lstOptions = []
            self._iChoice = -1
            vbxEvtTitleArea = lblChoiceTitle
        else: # if the event has options
            self._iChoice = 0 # default the current choice to the first option
            # make a list of option GUI elements based on each option defined in the event definition evtDef
            lstOptions = [uiOption(title=evtDef.options[i].title
                                    , description=evtDef.options[i].desc
                                    , image=evtDef.options[i].image
                                    , margin= '8px 8px 0px 0px' if i!=len(evtDef.options)-1 else '8px 0px 0px 0px'
                                    , on_click=on_select
                                    , grid_area=f'{evtDef.name}_{evtDef.options[i].name}'
                                    , parent_event_ui=self
                                    , option_value=i
                                ) 
                          for i in range(len(evtDef.options))]
            
            #  label that displays the selected choice
            lblChoiceAnswer = Label(evtDef.options[0].title
                               , style={'font_size':'12px'}
                               , layout=Layout(grid_area=evtDef.name+'_lblChoiceAnswer')
                              )
            # an HBox that represents the area that displays the selected choice
            hbxEvtAnsArea = HBox([HTML(value= '<span style="margin-right:8px; line-height:14px">Selected Choice:</span>')
                                , lblChoiceAnswer]
                               , layout=Layout(grid_area=evtDef.name+'_hbxEvtAnsArea')
                           )
            # a VBox that has the title and the selected choice
            vbxEvtTitleArea = VBox([lblChoiceTitle, hbxEvtAnsArea], layout=Layout(grid_area=evtDef.name+'_vbxEvtTitleArea'))
            self.lblChoiceAnswer = lblChoiceAnswer

        # a wrapped flow box with all the option UIs
        bxOptions = Box(lstOptions, layout=Layout(
            grid_area = f'{evtDef.name}_optionsec'
            , display='flex'
            , flex_flow='row wrap'
        ))

        # save the list of option uis so that we may reference / access them later
        self.option_ui = lstOptions
        # a list of booleans that will track if each option is available
        self._opt_availability = [True] * len(self.option_ui)

        
        # call the parent GridBox constructor to get all the elements in place
        super().__init__(
            children=[vbxEvtTitleArea, divDesc, bxOptions]
            , layout=Layout(
                grid_area=evtDef.name
                , grid_template_rows='64px auto auto' # 3 rows
                , grid_template_columns="auto" # 1 column, 100% allotted space given by the parent object
                , grid_template_areas=f"""
                    "{vbxEvtTitleArea.layout.grid_area}"
                    "{divDesc.layout.grid_area}"
                    "{bxOptions.layout.grid_area}"
                """
            ))

    @property
    def has_options(self):
        """Gets a boolean value that indicates if the event this UI widget represents has options."""
        return (self.evtDef.options is not None) and len(self.evtDef.options) != 0
    
    @property
    def iChoice(self):
        """Gets or sets the index of the option that is selected for the event."""
        return self._iChoice

    # setter of the iChoice property
    @iChoice.setter
    def iChoice(self, value):
        """Sets the index of the option that is selected for the event. 
        The value should be the index of the option as shown in options field of an event definition. See backend/design/eventdef.py for more info."""
        # if the event has no options, do nothing
        if self.evtDef.options is None or len(self.evtDef.options) == 0:
            return
        # if the value to be set is out of bound, raise error
        if value >= len(self.evtDef.options) or value < 0:
            raise Exception('iChoice value is out of bound.')
        # remember which option is selected
        self._iChoice = value
        # display the title of the option that is selected
        self.lblChoiceAnswer.value = self.evtDef.options[value].title
        
    @property
    def OptionAvailability(self):
        """Gets or sets the option availability for the event. 
        The returned value is a list of booleans, each of which indicates if an option of the event is available for selection. 
        An unavailable option still displays but has its Select button disabled."""
        return self._opt_availability
    
    # setter of the OptionAvailability property
    @OptionAvailability.setter
    def OptionAvailability(self, value):
        """Sets the option availability for the event. 
        The value should be a list of booleans, each of which indicates if an option of the event is available for selection. 
        An unavailable option still displays but has its Select button disabled.
        """
        if not isinstance(value, list):
            raise Exception('OptionAvailability can only be set to a list.')
        if len(value) != len(self.option_ui):
            raise Exception(f'The number of elements given (={len(value)}) to OptionAvailability must be the same as the number of options (={len(self.option_ui)}) for the event.')
        for i in range(len(self.option_ui)):
            # disable an option UI element. 
            self.option_ui[i].disabled = value[i] == False
        # remember the availability settings
        self._opt_availability = value


