# Copyright (C) 2023, Bank of America.  The file below is licensed to LSC for use with HSoF.  All other rights are reserved.

"""This file defines the GUI elements that displays the learning tip area."""

from ipywidgets import HTML, Layout, Tab, Image, HBox, VBox
import gui._shared as ui # shared items across front end

# opening and reading HTML pages of the Learning Tip
# opening leanring tip html pages
with open('gui/html/learningtip1_1.html','r') as f1_1, open('gui/html/learningtip1_2.html','r') as f1_2 \
, open('gui/html/learningtip2_1.html','r') as f2_1,  open('gui/html/learningtip2_2.html','r') as f2_2 \
,open('gui/html/learningtip3_1.html','r') as f3_1 ,open('gui/html/learningtip3_2.html','r') as f3_2 \
, open('gui/html/image/Picture1.png','rb') as f1, open('gui/html/image/Picture2.png','rb') as f2 \
, open('gui/html/image/Picture3.png','rb') as f3, open('gui/html/image/Picture4.png','rb') as f4 \
, open('gui/html/image/Picture5.png','rb') as f5, open('gui/html/image/Picture6.png','rb') as f6: \

    # reading leanring tip html pages
    knowledge_template_1_1 = f1_1.read()
    knowledge_template_1_2 = f1_2.read()
    knowledge_template_2_1 = f2_1.read()
    knowledge_template_2_2 = f2_2.read()
    knowledge_template_3_1 = f3_1.read()
    knowledge_template_3_2 = f3_2.read()
    
    # reading images used in html pages for learning tip 1
    image_template_1= f1.read()
    ib_1=Image(value=image_template_1)
    ib_1.layout.object_fit='contain'

    # reading images used in html pages for learning tip 1
    image_template_2= f2.read()
    ib_2=Image(value=image_template_2)
    ib_2.layout.object_fit='contain'

    # reading images used in html pages for learning tip 2
    image_template_2= f3.read()
    ib_3=Image(value=image_template_2)
    ib_3.layout.object_fit='contain'

    # reading images used in html pages for learning tip 2
    image_template_2= f4.read()
    ib_4=Image(value=image_template_2)
    ib_4.layout.object_fit='contain'

    # reading images used in html pages for learning tip 3
    image_template_2= f5.read()
    ib_5=Image(value=image_template_2)
    ib_5.layout.object_fit='contain'

    # reading images used in html pages for learning tip 3
    image_template_2= f6.read()
    ib_6=Image(value=image_template_2)
    ib_6.layout.object_fit='contain'
    

# learning tip page 1 is divided into 2 html accompanying a widget for 2 images.

# creating a widget for learningtip 1 page - top part
learning_tip_1_1_pg = HTML(value=knowledge_template_1_1
                                 , layout=Layout(
                                     grid_area='learning_tip_1_1_pg'
                                     
                                     )
                                ) 
# creating a widget for learningtip 1 page - bottom part
learning_tip_1_2_pg = HTML(value=knowledge_template_1_2
                                 , layout=Layout(
                                     grid_area='learning_tip_1_2_pg'
                                     )
                                ) 

# creating a widget for the images in the learning tip1 - middle part
learning_tip_1_image=HBox(children=[ib_1,ib_2]
                          , layout=Layout(
                               grid_area='learning_tip_1_image'
                              )
                         )
                          
# creating a widget for combining the top,bottom and middle part for leaningt tip 1
learning_tip_1_pg_final=VBox(children=[learning_tip_1_1_pg,learning_tip_1_image, learning_tip_1_2_pg]
                               , layout=Layout(
                               grid_area='learning_tip_1_pg_final'
                                   ,grid_template_areas=f"""{learning_tip_1_1_pg.layout.grid_area} {learning_tip_1_image.layout.grid_area}  
                                                                                                {learning_tip_1_2_pg.layout.grid_area}""" 
                              
                                            )
                              )

# creating a widget for learningtip 2 page - top part
learning_tip_2_1_pg = HTML(value=knowledge_template_2_1
                                 , layout=Layout(
                                     grid_area='learning_tip_2_1_pg'
                                     )
                          )
# creating a widget for learningtip 2 page - bottom part                           )
learning_tip_2_2_pg = HTML(value=knowledge_template_2_2
                                 , layout=Layout(
                                     grid_area='learning_tip_2_2_pg'
                                     )
                                )
# creating a widget for the images in the learning tip2 - middle part
learning_tip_2_image=HBox(children=[ib_3,ib_4]
                          , layout=Layout(
                               grid_area='learning_tip_2_image'
                              )
                         )
# creating a widget for combining the top,bottom and middle part for leaningt tip 2
learning_tip_2_pg_final=VBox(children=[learning_tip_2_1_pg,learning_tip_2_image, learning_tip_2_2_pg]
                               , layout=Layout(
                               grid_area='learning_tip_2_pg_final'
                                   ,grid_template_areas=f"""{learning_tip_2_1_pg.layout.grid_area} {learning_tip_2_image.layout.grid_area}  
                                                                                                {learning_tip_2_2_pg.layout.grid_area}""" 
                              
                                            )
                              )

# creating a widget for learningtip 2 page - top part
learning_tip_3_1_pg = HTML(value=knowledge_template_3_1
                                 , layout=Layout(
                                     grid_area='learning_tip_3_1_pg'
                                     )
                          )
# creating a widget for learningtip 3 page - bottom part   
learning_tip_3_2_pg = HTML(value=knowledge_template_3_2
                                 , layout=Layout(
                                     grid_area='learning_tip_3_2_pg'
                                     )
                                )
# creating a widget for the images in the learning tip3 - middle part
learning_tip_3_image=HBox(children=[ib_5,ib_6]
                          , layout=Layout(
                               grid_area='learning_tip_3_image'
                              )
                         )
# creating a widget for combining the top,bottom and middle part for leaningt tip 3
learning_tip_3_pg_final=VBox(children=[learning_tip_3_1_pg,learning_tip_3_image, learning_tip_3_2_pg]
                               , layout=Layout(
                               grid_area='learning_tip_3_pg_final'
                                   ,grid_template_areas=f"""{learning_tip_3_1_pg.layout.grid_area} {learning_tip_3_image.layout.grid_area}  
                                                                                                {learning_tip_3_2_pg.layout.grid_area}""" 
                              
                                            )
                              )

# defines the knowledge display area. this is the widget that gets to be displayed in the playground (playground.py).
#combining all the widgets defined above into tab widget
tabKnowlege = Tab(
    children=[learning_tip_1_pg_final,learning_tip_2_pg_final,learning_tip_3_pg_final] 
   , titles=['Tip 1','Tip 2','Tip 3']
   , layout=Layout(grid_area='tabKnowlege', height=ui.HeightPlayground)
)

