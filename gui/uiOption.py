# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file implements the GUI elements that collectively display an event choice

Here we make all the elements into one GUI object with what's called inheritance. 
Inheritance is a mechanism commonly used in object-oriented programming. 
For more information on inheritance, you can refer to https://en.wikipedia.org/wiki/Inheritance_(object-oriented_programming)

By looking at the class definition below, can you tell which class is uiOption inherited from?
"""

from ipywidgets import Layout, GridBox, Image, VBox, Label, HTML, Button, ButtonStyle


class uiOption(GridBox):
    """A ipywidget class that represents the UI element for an event option."""

    # this is the constructor function of the uiOption class. 
    # for more info on constructor, please refer to https://en.wikipedia.org/wiki/Constructor_(object-oriented_programming)
    def __init__(self, grid_area='uiOption1'
                 , title='Option Title'
                 , description='Option description line 1\nOption description line 2'
                 , on_click=None
                 , image='res/bank_icon1.png', image_format='png'
                 , margin=''
                 , parent_event_ui=None
                 , option_value=None
                ):
        """
        """

        if image is None or image=='':
            image = 'res/bank_icon1.png'
        
        # load the image
        imgOption = Image(value=open(image,'rb').read(), format=image_format, width=84, height=84
                           , layout=Layout(
                               #name the current object so the parent grid can recognize it in layout.grid_template_areas
                               grid_area=grid_area+'_imgOption' 
                               # set the right margin to leave some white space before text area
                               , margin='0px 8px 0px 0px'
                      ))

        # create the text area. it consists of the option title followed by option description. 
        vbxTextArea = VBox([HTML(value= '<b style="word-wrap:break-word; margin:0px; font-size:14px; line-height:14px">'+ title.replace('\n','') +' </b>')
                            , HTML(value= '<p style="word-wrap:break-word; margin:0px; line-height:16px">'+ description.replace('\n','<br/>') +' </p>')] 
                 , layout=Layout(grid_area=grid_area+'_vbxTextArea')
            )

        # create the "Select" button
        btnSelect = Button(description='Select'
                           , layout=Layout(width='auto', grid_area=grid_area+'_btnSel')
                           , style=ButtonStyle(button_color='moccasin'))
        # add these additional fields to the button so that the click event can connect to the parent UI and the option's value
        btnSelect.parentEventObj = parent_event_ui
        btnSelect.addnl_click_logic = on_click
        btnSelect.option_value = option_value
        # add click event logic
        btnSelect.on_click(uiOption.uiOption_btnSelect_on_click)
        self._select_button = btnSelect

        # call the parent class constructor
        super().__init__(children=[imgOption, btnSelect, vbxTextArea]
                        , layout=Layout(
                            grid_area=grid_area #name the current object so the parent grid can recognize it in layout.grid_template_areas
                            , width="260px"
                            # here we are making a table with 3 rows and 2 columns. 
                            # the image takes up the first cell
                            # the text area takes up the second column from first to second rows. 
                            # the button takes up the entire last row. 
                            # is there anything that occupies the cell below the image?
                            , grid_template_rows="84px auto 32px" 
                            , grid_template_columns="84px 172px" 
                            , grid_template_areas=f"""
                            "{imgOption.layout.grid_area} {vbxTextArea.layout.grid_area}" 
                            ". {vbxTextArea.layout.grid_area}" 
                            "{btnSelect.layout.grid_area} {btnSelect.layout.grid_area}"
                            """
                            , justify_content = 'flex-start' # horizontal alignment
                            , align_content = 'flex-start' # vertical alignment
                            , border='solid 2px'
                            , margin=margin
                        )
        )

    # this is the logic that handles the click event
    def uiOption_btnSelect_on_click(b):
        if b.option_value is not None and b.parentEventObj is not None:
            b.parentEventObj.iChoice = b.option_value
        if b.addnl_click_logic is not None:
            b.addnl_click_logic(b)

    @property
    def disabled(self):
        """Gets or sets if the option is disabled. A disabled option sets its Select button's disabled property to True."""
        return self._select_button.disabled

    # setter of disabled property
    @disabled.setter
    def disabled(self, value):
        """Sets if the option is disabled. A disabled option sets its Select button's disabled property to True."""
        self._select_button.disabled = (value == True)


