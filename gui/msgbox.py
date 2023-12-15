# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file displays the message area of the game."""

from ipywidgets import Button, ButtonStyle, Layout, Label, VBox, HTML
import gui._shared as ui

def btnMsgOK_on_click(b):
    from gui.playground import refresh_playground
    ui.DisplayMode = b.next_mode
    refresh_playground()
    

# define message title display
lblMsgTitle = Label(value='msgbox_lblMsgTitle', style={'font_size':'16px'}, layout=Layout(grid_area='msgbox_lblMsgTitle'))
# define message description display
htmlMsgDesc = HTML(value='<p style="word-wrap: break-word; line-height: 12px; font-size: 12px; margin: 0px"></p>', layout=Layout(grid_area='msgbox_htmlMsgDesc'))
# define the OK button
btnMsgOK = Button(description='OK', layout=Layout(width='64px', grid_area='msgbox_btnMsgOK', margin='32px 0px 0px 0px')
                  , style=ButtonStyle(button_color='#BCBCBE')
                 )
btnMsgOK.on_click(btnMsgOK_on_click)

# put all the 3 widgets into a vertical box. This is the widget that gets to be displayed in the playground (playground.py).
vbxMsg = VBox([lblMsgTitle, htmlMsgDesc, btnMsgOK], layout=Layout(grid_area='msgbox_vbxMsg'))

def show_message(title, mes, next_mode=0):
    """Displays a message in the playground area and pauses the game."""
    lblMsgTitle.value = title
    htmlMsgDesc.value = '<p style="word-wrap: break-word">{0}</p>'.format(mes.replace('\n','<br/>'))
    btnMsgOK.next_mode = next_mode

    from gui.playground import refresh_playground
    ui.DisplayMode = 3
    refresh_playground()
    

