# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
 Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.
""This file defines the common elements that are shared across files in the gui folder."""

HeightFooter='32px' # height of the footer 
HeightHeader='32px' # height of the header
HeightPlayground='540px' # height of the playground

# a dictionary that stores the event UI objects (uiLifeEvent.py). The key is the name of the event in the event definition (backend/design/eventdef.py)
# the content of this dictionary is created upon the first loading of lifestage.py
event_by_name = dict()

# points to the current event UI object that is being displayed.
crntEventUI = None

# an integer to indicate which display area should be rendered in the current game. 
# The values are
# 0: game play
# 1: knowldge tip
# 2: dash board
# 3: message box
# these values correspond to the index in tblMainArea.children defined in gui/playground.py.
DisplayMode = 0

# a color wheel that is used to cycle through players to set their representative color
player_colorwheel = ['#A5DA46','#8EDFFB','#E38EFB','#FB8EA4', '#FBC88E','#F2FB8E','#8FFF99','#8EA9FB', '#B98FFF','#FD5151','#E0A76C', '#E4F251']

def dataframe2html(df, style=''):
    """Converts a pandas dataframe to HTML table."""
    ncols = df.shape[1]
    
    
    if style != '':
        style_bits = f' style="{style}"'
    else:
        style_bits = ''

    rtn = f'<table{style_bits}>'

    # add header row
    crnt_row = "\n\t<tr>"
    for crntCol in df.columns:
        crnt_row += "\n\t\t<th{1}>{0}</th>".format(crntCol, style_bits)
    rtn += crnt_row + "\n\t</tr>"

    # add value rows
    for iRow, crntRow in df.iterrows():
        crnt_row = "\n\t<tr>"
        for iCol in range(ncols):
            crnt_row += "\n\t\t<td{1}>{0}</td>".format(crntRow.values[iCol], style_bits)
        # crnt_row += "\n</tr>"
        rtn += crnt_row + "\n\t</tr>"

    return rtn + '</table>'

