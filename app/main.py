#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 12:22:00 2019

@author: Home
"""

import pandas as pd
import numpy as np
import os
import time

from bokeh.models import ColumnDataSource, Panel, Tabs
from bokeh.models.widgets import PreText, FileInput, Button, TableColumn, DataTable, Select, Paragraph, Div
from bokeh.layouts import column, row, Spacer
from bokeh.plotting import curdoc, figure

from tornado import gen
from threading import Thread
from functools import partial

import base64
import io


main_path = os.getcwd()+'/app/data/'
check_file = pd.read_csv(main_path+'data_check.csv')

logo = Div(text="<img src= '/app/static/logo.png'>")



data64_1 = 'RGF0ZSxDYXRfVmFyMSxDYXRfVmFyMixCYXNlLEJhc2VfMTAsUmF3DQo3LzI3L\
        zA4IDE5OjA4LEEsWCwxLjc5MTc1OTQ2OSwwLjc3ODE1MTI1LDYNCjMvNi8wOCAxMzo1NixC\
        LFksMS45NDU5MTAxNDksMC44NDUwOTgwNCw3DQo0LzI5LzA4IDA6NTUsQyxaLDIuMDc5NDQ\
        xNTQyLDAuOTAzMDg5OTg3LDgNCjkvMTkvMDggNjoxNixELFgsMi4xOTcyMjQ1NzcsMC45NT\
        QyNDI1MDksOQ0KNy8yNC8wOCAyMDozOCxFLFksMi4zMDI1ODUwOTMsMSwxMA0KMS8yMC8wO\
        CAwOjQwLEYsWiwyLjM5Nzg5NTI3MywxLjA0MTM5MjY4NSwxMQ0KMTIvNi8wOCAyMzoyNCxH\
        LFgsMi40ODQ5MDY2NSwxLjA3OTE4MTI0NiwxMg0KNy8yNS8wOCAxNDoxNyxBLFgsMi41NjQ\
        5NDkzNTcsMS4xMTM5NDMzNTIsMTMNCjkvMy8wOCAyMDo1MCxCLFksMi42MzkwNTczMywxLj\
        E0NjEyODAzNiwxNA0KOC8yOS8wOCAxNTozNCxDLFosMi43MDgwNTAyMDEsMS4xNzYwOTEyN\
        TksMTUNCjIvMTYvMDggMTM6MDEsRCxYLDIuNzcyNTg4NzIyLDEuMjA0MTE5OTgzLDE2DQo0\
        LzEyLzA4IDE2OjUzLEUsWSwyLjgzMzIxMzM0NCwxLjIzMDQ0ODkyMSwxNw0KNi8xMi8wOCA\
        xNTowOCxGLFosMi44OTAzNzE3NTgsMS4yNTUyNzI1MDUsMTgNCjUvMTkvMDggOTozOSxHLF\
        gsMi45NDQ0Mzg5NzksMS4yNzg3NTM2MDEsMTkNCjQvMjIvMDggMjA6MTIsQSxYLDIuOTk1N\
        zMyMjc0LDEuMzAxMDI5OTk2LDIwDQo4LzMvMDggMTU6NTMsQixZLDMuMDQ0NTIyNDM4LDEu\
        MzIyMjE5Mjk1LDIxDQo3LzMwLzA4IDE4OjM0LEMsWiwzLjA5MTA0MjQ1MywxLjM0MjQyMjY\
        4MSwyMg0KNy83LzA4IDM6MjIsRCxYLDMuMTM1NDk0MjE2LDEuMzYxNzI3ODM2LDIzDQo4Lz\
        QvMDggNToxMCxFLFksMy4xNzgwNTM4MywxLjM4MDIxMTI0MiwyNA0KOC8xLzA4IDA6MjQsR\
        ixaLDMuMjE4ODc1ODI1LDEuMzk3OTQwMDA5LDI1DQo2LzE0LzA4IDE1OjI1LEcsWCwzLjI1\
        ODA5NjUzOCwxLjQxNDk3MzM0OCwyNg0KNS81LzA4IDIxOjM4LEEsWCwzLjI5NTgzNjg2Niw\
        xLjQzMTM2Mzc2NCwyNw0KNi8xLzA4IDExOjM3LEIsWSwzLjMzMjIwNDUxLDEuNDQ3MTU4MD\
        MxLDI4DQoxLzE0LzA4IDIzOjQ0LEMsWiwzLjM2NzI5NTgzLDEuNDYyMzk3OTk4LDI5DQoxM\
        i8yMy8wOCAxODo0MSxELFgsMy40MDExOTczODIsMS40NzcxMjEyNTUsMzANCjQvMTYvMDgg\
        MTU6MjksRSxZLDMuNDMzOTg3MjA0LDEuNDkxMzYxNjk0LDMxDQozLzgvMDggMTk6MjQsRix\
        aLDMuNDY1NzM1OTAzLDEuNTA1MTQ5OTc4LDMyDQozLzI3LzA4IDg6NDgsRyxYLDMuNDk2NT\
        A3NTYxLDEuNTE4NTEzOTQsMzMNCjEyLzEvMDggMTM6MjQsQSxYLDMuNTI2MzYwNTI1LDEuN\
        TMxNDc4OTE3LDM0DQo0LzE5LzA4IDE2OjIyLEIsWSwzLjU1NTM0ODA2MSwxLjU0NDA2ODA0\
        NCwzNQ0KNC8zLzA4IDI6NTQsQyxaLDMuNTgzNTE4OTM4LDEuNTU2MzAyNTAxLDM2DQo0LzE\
        wLzA4IDE6MjUsRCxYLDMuNjEwOTE3OTEzLDEuNTY4MjAxNzI0LDM3DQo3LzE0LzA4IDM6MT\
        IsRSxZLDMuNjM3NTg2MTYsMS41Nzk3ODM1OTcsMzgNCjEyLzI0LzA4IDE6MDMsRixaLDMuN\
        jYzNTYxNjQ2LDEuNTkxMDY0NjA3LDM5DQo0LzE2LzA4IDE5OjU2LEcsWCwzLjY4ODg3OTQ1\
        NCwxLjYwMjA1OTk5MSw0MA0KNi8yOS8wOCAxNjoyMSxBLFgsMy43MTM1NzIwNjcsMS42MTI\
        3ODM4NTcsNDENCjIvMTQvMDggNTo1MyxCLFksMy43Mzc2Njk2MTgsMS42MjMyNDkyOSw0Mg\
        0KMTIvMTEvMDggMTE6MzUsQyxaLDMuNzYxMjAwMTE2LDEuNjMzNDY4NDU2LDQzDQoxMS8yM\
        i8wOCA5OjAzLEQsWCwzLjc4NDE4OTYzNCwxLjY0MzQ1MjY3Niw0NA0KMy8yOC8wOCAxMjoz\
        MCxFLFksMy44MDY2NjI0OSwxLjY1MzIxMjUxNCw0NQ0KNi8zMC8wOCAxNzoxMixGLFosMy4\
        4Mjg2NDEzOTYsMS42NjI3NTc4MzIsNDYNCjYvNi8wOCAxMjo1NCxHLFgsMy44NTAxNDc2MD\
        IsMS42NzIwOTc4NTgsNDcNCjEvMjAvMDggMTc6MzEsQSxYLDMuODcxMjAxMDExLDEuNjgxM\
        jQxMjM3LDQ4DQoxMi82LzA4IDEwOjQzLEIsWSwzLjg5MTgyMDI5OCwxLjY5MDE5NjA4LDQ5\
        DQo1LzI5LzA4IDU6MTUsQyxaLDMuOTEyMDIzMDA1LDEuNjk4OTcwMDA0LDUwDQoxLzE3LzA\
        4IDIwOjQ1LEQsWCwzLjkzMTgyNTYzMywxLjcwNzU3MDE3Niw1MQ0KMS85LzA4IDIxOjM0LE\
        UsWSwzLjk1MTI0MzcxOSwxLjcxNjAwMzM0NCw1Mg0KNy8yMC8wOCA5OjQ0LEYsWiwzLjk3M\
        DI5MTkxNCwxLjcyNDI3NTg3LDUzDQoxMS8yMC8wOCAxOjQ5LEcsWCwzLjk4ODk4NDA0Nywx\
        LjczMjM5Mzc2LDU0DQo1LzE4LzA4IDEzOjQwLEEsWCw0LjAwNzMzMzE4NSwxLjc0MDM2MjY\
        4OSw1NQ0KMTEvNS8wOCAxMDoxMCxCLFksNC4wMjUzNTE2OTEsMS43NDgxODgwMjcsNTYNCj\
        gvNy8wOCA1OjMwLEMsWiw0LjA0MzA1MTI2OCwxLjc1NTg3NDg1Niw1Nw0KMTIvMTcvMDggM\
        Tc6MjMsRCxYLDQuMDYwNDQzMDExLDEuNzYzNDI3OTk0LDU4DQoxMC8yNi8wOCAyMDowOSxF\
        LFksNC4wNzc1Mzc0NDQsMS43NzA4NTIwMTIsNTkNCjIvMTcvMDggNjozMyxGLFosNC4wOTQ\
        zNDQ1NjIsMS43NzgxNTEyNSw2MA0KNS8yNC8wOCAxNDoxNCxHLFgsNC4xMTA4NzM4NjQsMS\
        43ODUzMjk4MzUsNjENCjEvMjUvMDggNDo1NyxBLFgsNC4xMjcxMzQzODUsMS43OTIzOTE2O\
        DksNjINCjExLzQvMDggNzo1MSxCLFksNC4xNDMxMzQ3MjYsMS43OTkzNDA1NDksNjMNCjQv\
        MjcvMDggMjA6MTAsQyxaLDQuMTU4ODgzMDgzLDEuODA2MTc5OTc0LDY0DQo0LzYvMDggMTI\
        6MDksRCxYLDQuMTc0Mzg3MjcsMS44MTI5MTMzNTcsNjUNCjQvMTQvMDggMTM6MTUsRSxZLD\
        QuMTg5NjU0NzQyLDEuODE5NTQzOTM2LDY2DQo1LzI3LzA4IDE0OjM4LEYsWiw0LjIwNDY5M\
        jYxOSwxLjgyNjA3NDgwMyw2Nw0KMS8yMC8wOCAxNTowMCxHLFgsNC4yMTk1MDc3MDUsMS44\
        MzI1MDg5MTMsNjgNCjQvMjAvMDggMjM6MzAsQSxYLDQuMjM0MTA2NTA1LDEuODM4ODQ5MDk\
        xLDY5DQoyLzUvMDggMjI6MjgsQixZLDQuMjQ4NDk1MjQyLDEuODQ1MDk4MDQsNzANCjcvMj\
        cvMDggMTg6NDQsQyxaLDQuMjYyNjc5ODc3LDEuODUxMjU4MzQ5LDcxDQo3LzYvMDggMDo0N\
        ixELFgsNC4yNzY2NjYxMTksMS44NTczMzI0OTYsNzINCjEyLzI2LzA4IDE6MjYsRSxZLDQu\
        MjkwNDU5NDQxLDEuODYzMzIyODYsNzMNCjIvMjEvMDggMzo1NSxGLFosNC4zMDQwNjUwOTM\
        sMS44NjkyMzE3Miw3NA0KMi8zLzA4IDQ6MTEsRyxYLDQuMzA0MDY1MDkzLDEuODY5MjMxNz\
        IsNzQNCjMvMTYvMDggMTk6NTgsQSxYLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjIvM\
        jMvMDggMTI6MDgsQixZLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjExLzI4LzA4IDk6\
        MjEsQyxaLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjExLzUvMDggMTY6MDksRCxYLDQ\
        uMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQ='
        
data64_2 = 'RGF0ZSxDYXRfVmFyMSxDYXRfVmFyMixCYXNlLEJhc2VfMTAsUmF3DQo3LzI3LzA4IDE\
    5OjA4LEEsWCwxLjc5MTc1OTQ2OSwwLjc3ODE1MTI1LDYNCjMvNi8wOCAxMzo1NixCLFksMS45NDU5MT\
    AxNDksMC44NDUwOTgwNCw3DQo0LzI5LzA4IDA6NTUsQyxaLDIuMDc5NDQxNTQyLDAuOTAzMDg5OTg3L\
    DgNCjkvMTkvMDggNjoxNixELFgsMi4xOTcyMjQ1NzcsMC45NTQyNDI1MDksOQ0KNy8yNC8wOCAyMDoz\
    OCxFLFksMi4zMDI1ODUwOTMsMSwxMA0KMS8yMC8wOCAwOjQwLEYsWiwyLjM5Nzg5NTI3MywxLjA0MTM\
    5MjY4NSwxMQ0KMTIvMTEvMDggMTE6MzUsQyxaLDMuNzYxMjAwMTE2LDEuNjMzNDY4NDU2LDQzDQoxMS\
    8yMi8wOCA5OjAzLEQsWCwzLjc4NDE4OTYzNCwxLjY0MzQ1MjY3Niw0NA0KMy8yOC8wOCAxMjozMCxFL\
    FksMy44MDY2NjI0OSwxLjY1MzIxMjUxNCw0NQ0KNi8zMC8wOCAxNzoxMixGLFosMy44Mjg2NDEzOTYs\
    MS42NjI3NTc4MzIsNDYNCjYvNi8wOCAxMjo1NCxHLFgsMy44NTAxNDc2MDIsMS42NzIwOTc4NTgsNDc\
    NCjEvMjAvMDggMTc6MzEsQSxYLDMuODcxMjAxMDExLDEuNjgxMjQxMjM3LDQ4DQoxMi82LzA4IDEwOj\
    QzLEIsWSwzLjg5MTgyMDI5OCwxLjY5MDE5NjA4LDQ5DQo1LzI5LzA4IDU6MTUsQyxaLDMuOTEyMDIzM\
    DA1LDEuNjk4OTcwMDA0LDUwDQoxLzE3LzA4IDIwOjQ1LEQsWCwzLjkzMTgyNTYzMywxLjcwNzU3MDE3\
    Niw1MQ0KMS85LzA4IDIxOjM0LEUsWSwzLjk1MTI0MzcxOSwxLjcxNjAwMzM0NCw1Mg0KNy8yMC8wOCA\
    5OjQ0LEYsWiwzLjk3MDI5MTkxNCwxLjcyNDI3NTg3LDUzDQoxMS8yMC8wOCAxOjQ5LEcsWCwzLjk4OD\
    k4NDA0NywxLjczMjM5Mzc2LDU0DQo1LzE4LzA4IDEzOjQwLEEsWCw0LjAwNzMzMzE4NSwxLjc0MDM2M\
    jY4OSw1NQ0KMTEvNS8wOCAxMDoxMCxCLFksNC4wMjUzNTE2OTEsMS43NDgxODgwMjcsNTYNCjgvNy8w\
    OCA1OjMwLEMsWiw0LjA0MzA1MTI2OCwxLjc1NTg3NDg1Niw1Nw0KMTIvMTcvMDggMTc6MjMsRCxYLDQ\
    uMDYwNDQzMDExLDEuNzYzNDI3OTk0LDU4DQoxMC8yNi8wOCAyMDowOSxFLFksNC4wNzc1Mzc0NDQsMS\
    43NzA4NTIwMTIsNTkNCjIvMTcvMDggNjozMyxGLFosNC4wOTQzNDQ1NjIsMS43NzgxNTEyNSw2MA0KN\
    S8yNC8wOCAxNDoxNCxHLFgsNC4xMTA4NzM4NjQsMS43ODUzMjk4MzUsNjENCjEvMjUvMDggNDo1NyxB\
    LFgsNC4xMjcxMzQzODUsMS43OTIzOTE2ODksNjINCjExLzQvMDggNzo1MSxCLFksNC4xNDMxMzQ3MjY\
    sMS43OTkzNDA1NDksNjMNCjQvMjcvMDggMjA6MTAsQyxaLDQuMTU4ODgzMDgzLDEuODA2MTc5OTc0LD\
    Y0DQo0LzYvMDggMTI6MDksRCxYLDQuMTc0Mzg3MjcsMS44MTI5MTMzNTcsNjUNCjQvMTQvMDggMTM6M\
    TUsRSxZLDQuMTg5NjU0NzQyLDEuODE5NTQzOTM2LDY2DQo1LzI3LzA4IDE0OjM4LEYsWiw0LjIwNDY5\
    MjYxOSwxLjgyNjA3NDgwMyw2Nw0KMS8yMC8wOCAxNTowMCxHLFgsNC4yMTk1MDc3MDUsMS44MzI1MDg\
    5MTMsNjgNCjQvMjAvMDggMjM6MzAsQSxYLDQuMjM0MTA2NTA1LDEuODM4ODQ5MDkxLDY5DQoyLzUvMD\
    ggMjI6MjgsQixZLDQuMjQ4NDk1MjQyLDEuODQ1MDk4MDQsNzANCjcvMjcvMDggMTg6NDQsQyxaLDQuM\
    jYyNjc5ODc3LDEuODUxMjU4MzQ5LDcxDQo3LzYvMDggMDo0NixELFgsNC4yNzY2NjYxMTksMS44NTcz\
    MzI0OTYsNzINCjEyLzI2LzA4IDE6MjYsRSxZLDQuMjkwNDU5NDQxLDEuODYzMzIyODYsNzMNCjIvMjE\
    vMDggMzo1NSxGLFosNC4zMDQwNjUwOTMsMS44NjkyMzE3Miw3NA0KMi8zLzA4IDQ6MTEsRyxYLDQuMz\
    A0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjMvMTYvMDggMTk6NTgsQSxYLDQuMzA0MDY1MDkzLDEuODY5M\
    jMxNzIsNzQNCjIvMjMvMDggMTI6MDgsQixZLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjExLzI4\
    LzA4IDk6MjEsQyxaLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjExLzUvMDggMTY6MDksRCxYLDQ\
    uMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQ=' 

       
def decode(base64_string):
    return pd.read_csv(io.StringIO(base64.b64decode(base64_string).decode('utf-8')), sep=',')


running_info = Div(text="""<b>Status Bar</b>: Dashboard running Demo Data. <b>Please select files to upload</b>""",\
                   width = 575,\
                   style={'font-size': '115%',\
                           'color': 'black',\
                           'border-bottom': '3px',\
                           'border-style': 'double',\
                           'border-radius': '5px',\
                           'border-color': '	#05BAC5',\
                           'background-color': 'white',\
                           'padding': '.5em'})
    


if check_file['check'][0] == 0:
    source = ColumnDataSource(data = {'File_1': [decode(data64_1)],
                                      'File_2': [decode(data64_2)]})
else:
    source = ColumnDataSource(data = {'File_1': [pd.read_csv(main_path+'file1_data.csv')],
                                      'File_2': [pd.read_csv(main_path+'file2_data.csv')]})
    running_info.text = '<b>Status Bar</b>: Datasource is Updated ->->-> <b>Blend</b>, <b>Reset</b>, or <b>Select</b> New Data.'
    

    
# This is important! Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()
@gen.coroutine
def update(data):
    source.stream(data)
   
def blocking_task():
    while True:
        # do some blocking computation
        time.sleep(10)        
                
        data64_1 = 'RGF0ZSxDYXRfVmFyMSxDYXRfVmFyMixCYXNlLEJhc2VfMTAsUmF3DQo3LzI3L\
                    zA4IDE5OjA4LEEsWCwxLjc5MTc1OTQ2OSwwLjc3ODE1MTI1LDYNCjMvNi8wOCAxMzo1NixC\
                    LFksMS45NDU5MTAxNDksMC44NDUwOTgwNCw3DQo0LzI5LzA4IDA6NTUsQyxaLDIuMDc5NDQ\
                    xNTQyLDAuOTAzMDg5OTg3LDgNCjkvMTkvMDggNjoxNixELFgsMi4xOTcyMjQ1NzcsMC45NT\
                    QyNDI1MDksOQ0KNy8yNC8wOCAyMDozOCxFLFksMi4zMDI1ODUwOTMsMSwxMA0KMS8yMC8wO\
                    CAwOjQwLEYsWiwyLjM5Nzg5NTI3MywxLjA0MTM5MjY4NSwxMQ0KMTIvNi8wOCAyMzoyNCxH\
                    LFgsMi40ODQ5MDY2NSwxLjA3OTE4MTI0NiwxMg0KNy8yNS8wOCAxNDoxNyxBLFgsMi41NjQ\
                    5NDkzNTcsMS4xMTM5NDMzNTIsMTMNCjkvMy8wOCAyMDo1MCxCLFksMi42MzkwNTczMywxLj\
                    E0NjEyODAzNiwxNA0KOC8yOS8wOCAxNTozNCxDLFosMi43MDgwNTAyMDEsMS4xNzYwOTEyN\
                    TksMTUNCjIvMTYvMDggMTM6MDEsRCxYLDIuNzcyNTg4NzIyLDEuMjA0MTE5OTgzLDE2DQo0\
                    LzEyLzA4IDE2OjUzLEUsWSwyLjgzMzIxMzM0NCwxLjIzMDQ0ODkyMSwxNw0KNi8xMi8wOCA\
                    xNTowOCxGLFosMi44OTAzNzE3NTgsMS4yNTUyNzI1MDUsMTgNCjUvMTkvMDggOTozOSxHLF\
                    gsMi45NDQ0Mzg5NzksMS4yNzg3NTM2MDEsMTkNCjQvMjIvMDggMjA6MTIsQSxYLDIuOTk1N\
                    zMyMjc0LDEuMzAxMDI5OTk2LDIwDQo4LzMvMDggMTU6NTMsQixZLDMuMDQ0NTIyNDM4LDEu\
                    MzIyMjE5Mjk1LDIxDQo3LzMwLzA4IDE4OjM0LEMsWiwzLjA5MTA0MjQ1MywxLjM0MjQyMjY\
                    4MSwyMg0KNy83LzA4IDM6MjIsRCxYLDMuMTM1NDk0MjE2LDEuMzYxNzI3ODM2LDIzDQo4Lz\
                    QvMDggNToxMCxFLFksMy4xNzgwNTM4MywxLjM4MDIxMTI0MiwyNA0KOC8xLzA4IDA6MjQsR\
                    ixaLDMuMjE4ODc1ODI1LDEuMzk3OTQwMDA5LDI1DQo2LzE0LzA4IDE1OjI1LEcsWCwzLjI1\
                    ODA5NjUzOCwxLjQxNDk3MzM0OCwyNg0KNS81LzA4IDIxOjM4LEEsWCwzLjI5NTgzNjg2Niw\
                    xLjQzMTM2Mzc2NCwyNw0KNi8xLzA4IDExOjM3LEIsWSwzLjMzMjIwNDUxLDEuNDQ3MTU4MD\
                    MxLDI4DQoxLzE0LzA4IDIzOjQ0LEMsWiwzLjM2NzI5NTgzLDEuNDYyMzk3OTk4LDI5DQoxM\
                    i8yMy8wOCAxODo0MSxELFgsMy40MDExOTczODIsMS40NzcxMjEyNTUsMzANCjQvMTYvMDgg\
                    MTU6MjksRSxZLDMuNDMzOTg3MjA0LDEuNDkxMzYxNjk0LDMxDQozLzgvMDggMTk6MjQsRix\
                    aLDMuNDY1NzM1OTAzLDEuNTA1MTQ5OTc4LDMyDQozLzI3LzA4IDg6NDgsRyxYLDMuNDk2NT\
                    A3NTYxLDEuNTE4NTEzOTQsMzMNCjEyLzEvMDggMTM6MjQsQSxYLDMuNTI2MzYwNTI1LDEuN\
                    TMxNDc4OTE3LDM0DQo0LzE5LzA4IDE2OjIyLEIsWSwzLjU1NTM0ODA2MSwxLjU0NDA2ODA0\
                    NCwzNQ0KNC8zLzA4IDI6NTQsQyxaLDMuNTgzNTE4OTM4LDEuNTU2MzAyNTAxLDM2DQo0LzE\
                    wLzA4IDE6MjUsRCxYLDMuNjEwOTE3OTEzLDEuNTY4MjAxNzI0LDM3DQo3LzE0LzA4IDM6MT\
                    IsRSxZLDMuNjM3NTg2MTYsMS41Nzk3ODM1OTcsMzgNCjEyLzI0LzA4IDE6MDMsRixaLDMuN\
                    jYzNTYxNjQ2LDEuNTkxMDY0NjA3LDM5DQo0LzE2LzA4IDE5OjU2LEcsWCwzLjY4ODg3OTQ1\
                    NCwxLjYwMjA1OTk5MSw0MA0KNi8yOS8wOCAxNjoyMSxBLFgsMy43MTM1NzIwNjcsMS42MTI\
                    3ODM4NTcsNDENCjIvMTQvMDggNTo1MyxCLFksMy43Mzc2Njk2MTgsMS42MjMyNDkyOSw0Mg\
                    0KMTIvMTEvMDggMTE6MzUsQyxaLDMuNzYxMjAwMTE2LDEuNjMzNDY4NDU2LDQzDQoxMS8yM\
                    i8wOCA5OjAzLEQsWCwzLjc4NDE4OTYzNCwxLjY0MzQ1MjY3Niw0NA0KMy8yOC8wOCAxMjoz\
                    MCxFLFksMy44MDY2NjI0OSwxLjY1MzIxMjUxNCw0NQ0KNi8zMC8wOCAxNzoxMixGLFosMy4\
                    4Mjg2NDEzOTYsMS42NjI3NTc4MzIsNDYNCjYvNi8wOCAxMjo1NCxHLFgsMy44NTAxNDc2MD\
                    IsMS42NzIwOTc4NTgsNDcNCjEvMjAvMDggMTc6MzEsQSxYLDMuODcxMjAxMDExLDEuNjgxM\
                    jQxMjM3LDQ4DQoxMi82LzA4IDEwOjQzLEIsWSwzLjg5MTgyMDI5OCwxLjY5MDE5NjA4LDQ5\
                    DQo1LzI5LzA4IDU6MTUsQyxaLDMuOTEyMDIzMDA1LDEuNjk4OTcwMDA0LDUwDQoxLzE3LzA\
                    4IDIwOjQ1LEQsWCwzLjkzMTgyNTYzMywxLjcwNzU3MDE3Niw1MQ0KMS85LzA4IDIxOjM0LE\
                    UsWSwzLjk1MTI0MzcxOSwxLjcxNjAwMzM0NCw1Mg0KNy8yMC8wOCA5OjQ0LEYsWiwzLjk3M\
                    DI5MTkxNCwxLjcyNDI3NTg3LDUzDQoxMS8yMC8wOCAxOjQ5LEcsWCwzLjk4ODk4NDA0Nywx\
                    LjczMjM5Mzc2LDU0DQo1LzE4LzA4IDEzOjQwLEEsWCw0LjAwNzMzMzE4NSwxLjc0MDM2MjY\
                    4OSw1NQ0KMTEvNS8wOCAxMDoxMCxCLFksNC4wMjUzNTE2OTEsMS43NDgxODgwMjcsNTYNCj\
                    gvNy8wOCA1OjMwLEMsWiw0LjA0MzA1MTI2OCwxLjc1NTg3NDg1Niw1Nw0KMTIvMTcvMDggM\
                    Tc6MjMsRCxYLDQuMDYwNDQzMDExLDEuNzYzNDI3OTk0LDU4DQoxMC8yNi8wOCAyMDowOSxF\
                    LFksNC4wNzc1Mzc0NDQsMS43NzA4NTIwMTIsNTkNCjIvMTcvMDggNjozMyxGLFosNC4wOTQ\
                    zNDQ1NjIsMS43NzgxNTEyNSw2MA0KNS8yNC8wOCAxNDoxNCxHLFgsNC4xMTA4NzM4NjQsMS\
                    43ODUzMjk4MzUsNjENCjEvMjUvMDggNDo1NyxBLFgsNC4xMjcxMzQzODUsMS43OTIzOTE2O\
                    DksNjINCjExLzQvMDggNzo1MSxCLFksNC4xNDMxMzQ3MjYsMS43OTkzNDA1NDksNjMNCjQv\
                    MjcvMDggMjA6MTAsQyxaLDQuMTU4ODgzMDgzLDEuODA2MTc5OTc0LDY0DQo0LzYvMDggMTI\
                    6MDksRCxYLDQuMTc0Mzg3MjcsMS44MTI5MTMzNTcsNjUNCjQvMTQvMDggMTM6MTUsRSxZLD\
                    QuMTg5NjU0NzQyLDEuODE5NTQzOTM2LDY2DQo1LzI3LzA4IDE0OjM4LEYsWiw0LjIwNDY5M\
                    jYxOSwxLjgyNjA3NDgwMyw2Nw0KMS8yMC8wOCAxNTowMCxHLFgsNC4yMTk1MDc3MDUsMS44\
                    MzI1MDg5MTMsNjgNCjQvMjAvMDggMjM6MzAsQSxYLDQuMjM0MTA2NTA1LDEuODM4ODQ5MDk\
                    xLDY5DQoyLzUvMDggMjI6MjgsQixZLDQuMjQ4NDk1MjQyLDEuODQ1MDk4MDQsNzANCjcvMj\
                    cvMDggMTg6NDQsQyxaLDQuMjYyNjc5ODc3LDEuODUxMjU4MzQ5LDcxDQo3LzYvMDggMDo0N\
                    ixELFgsNC4yNzY2NjYxMTksMS44NTczMzI0OTYsNzINCjEyLzI2LzA4IDE6MjYsRSxZLDQu\
                    MjkwNDU5NDQxLDEuODYzMzIyODYsNzMNCjIvMjEvMDggMzo1NSxGLFosNC4zMDQwNjUwOTM\
                    sMS44NjkyMzE3Miw3NA0KMi8zLzA4IDQ6MTEsRyxYLDQuMzA0MDY1MDkzLDEuODY5MjMxNz\
                    IsNzQNCjMvMTYvMDggMTk6NTgsQSxYLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjIvM\
                    jMvMDggMTI6MDgsQixZLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjExLzI4LzA4IDk6\
                    MjEsQyxaLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjExLzUvMDggMTY6MDksRCxYLDQ\
                    uMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQ='
        
        data64_2 = 'RGF0ZSxDYXRfVmFyMSxDYXRfVmFyMixCYXNlLEJhc2VfMTAsUmF3DQo3LzI3LzA4IDE\
                    5OjA4LEEsWCwxLjc5MTc1OTQ2OSwwLjc3ODE1MTI1LDYNCjMvNi8wOCAxMzo1NixCLFksMS45NDU5MT\
                    AxNDksMC44NDUwOTgwNCw3DQo0LzI5LzA4IDA6NTUsQyxaLDIuMDc5NDQxNTQyLDAuOTAzMDg5OTg3L\
                    DgNCjkvMTkvMDggNjoxNixELFgsMi4xOTcyMjQ1NzcsMC45NTQyNDI1MDksOQ0KNy8yNC8wOCAyMDoz\
                    OCxFLFksMi4zMDI1ODUwOTMsMSwxMA0KMS8yMC8wOCAwOjQwLEYsWiwyLjM5Nzg5NTI3MywxLjA0MTM\
                    5MjY4NSwxMQ0KMTIvMTEvMDggMTE6MzUsQyxaLDMuNzYxMjAwMTE2LDEuNjMzNDY4NDU2LDQzDQoxMS\
                    8yMi8wOCA5OjAzLEQsWCwzLjc4NDE4OTYzNCwxLjY0MzQ1MjY3Niw0NA0KMy8yOC8wOCAxMjozMCxFL\
                    FksMy44MDY2NjI0OSwxLjY1MzIxMjUxNCw0NQ0KNi8zMC8wOCAxNzoxMixGLFosMy44Mjg2NDEzOTYs\
                    MS42NjI3NTc4MzIsNDYNCjYvNi8wOCAxMjo1NCxHLFgsMy44NTAxNDc2MDIsMS42NzIwOTc4NTgsNDc\
                    NCjEvMjAvMDggMTc6MzEsQSxYLDMuODcxMjAxMDExLDEuNjgxMjQxMjM3LDQ4DQoxMi82LzA4IDEwOj\
                    QzLEIsWSwzLjg5MTgyMDI5OCwxLjY5MDE5NjA4LDQ5DQo1LzI5LzA4IDU6MTUsQyxaLDMuOTEyMDIzM\
                    DA1LDEuNjk4OTcwMDA0LDUwDQoxLzE3LzA4IDIwOjQ1LEQsWCwzLjkzMTgyNTYzMywxLjcwNzU3MDE3\
                    Niw1MQ0KMS85LzA4IDIxOjM0LEUsWSwzLjk1MTI0MzcxOSwxLjcxNjAwMzM0NCw1Mg0KNy8yMC8wOCA\
                    5OjQ0LEYsWiwzLjk3MDI5MTkxNCwxLjcyNDI3NTg3LDUzDQoxMS8yMC8wOCAxOjQ5LEcsWCwzLjk4OD\
                    k4NDA0NywxLjczMjM5Mzc2LDU0DQo1LzE4LzA4IDEzOjQwLEEsWCw0LjAwNzMzMzE4NSwxLjc0MDM2M\
                    jY4OSw1NQ0KMTEvNS8wOCAxMDoxMCxCLFksNC4wMjUzNTE2OTEsMS43NDgxODgwMjcsNTYNCjgvNy8w\
                    OCA1OjMwLEMsWiw0LjA0MzA1MTI2OCwxLjc1NTg3NDg1Niw1Nw0KMTIvMTcvMDggMTc6MjMsRCxYLDQ\
                    uMDYwNDQzMDExLDEuNzYzNDI3OTk0LDU4DQoxMC8yNi8wOCAyMDowOSxFLFksNC4wNzc1Mzc0NDQsMS\
                    43NzA4NTIwMTIsNTkNCjIvMTcvMDggNjozMyxGLFosNC4wOTQzNDQ1NjIsMS43NzgxNTEyNSw2MA0KN\
                    S8yNC8wOCAxNDoxNCxHLFgsNC4xMTA4NzM4NjQsMS43ODUzMjk4MzUsNjENCjEvMjUvMDggNDo1NyxB\
                    LFgsNC4xMjcxMzQzODUsMS43OTIzOTE2ODksNjINCjExLzQvMDggNzo1MSxCLFksNC4xNDMxMzQ3MjY\
                    sMS43OTkzNDA1NDksNjMNCjQvMjcvMDggMjA6MTAsQyxaLDQuMTU4ODgzMDgzLDEuODA2MTc5OTc0LD\
                    Y0DQo0LzYvMDggMTI6MDksRCxYLDQuMTc0Mzg3MjcsMS44MTI5MTMzNTcsNjUNCjQvMTQvMDggMTM6M\
                    TUsRSxZLDQuMTg5NjU0NzQyLDEuODE5NTQzOTM2LDY2DQo1LzI3LzA4IDE0OjM4LEYsWiw0LjIwNDY5\
                    MjYxOSwxLjgyNjA3NDgwMyw2Nw0KMS8yMC8wOCAxNTowMCxHLFgsNC4yMTk1MDc3MDUsMS44MzI1MDg\
                    5MTMsNjgNCjQvMjAvMDggMjM6MzAsQSxYLDQuMjM0MTA2NTA1LDEuODM4ODQ5MDkxLDY5DQoyLzUvMD\
                    ggMjI6MjgsQixZLDQuMjQ4NDk1MjQyLDEuODQ1MDk4MDQsNzANCjcvMjcvMDggMTg6NDQsQyxaLDQuM\
                    jYyNjc5ODc3LDEuODUxMjU4MzQ5LDcxDQo3LzYvMDggMDo0NixELFgsNC4yNzY2NjYxMTksMS44NTcz\
                    MzI0OTYsNzINCjEyLzI2LzA4IDE6MjYsRSxZLDQuMjkwNDU5NDQxLDEuODYzMzIyODYsNzMNCjIvMjE\
                    vMDggMzo1NSxGLFosNC4zMDQwNjUwOTMsMS44NjkyMzE3Miw3NA0KMi8zLzA4IDQ6MTEsRyxYLDQuMz\
                    A0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjMvMTYvMDggMTk6NTgsQSxYLDQuMzA0MDY1MDkzLDEuODY5M\
                    jMxNzIsNzQNCjIvMjMvMDggMTI6MDgsQixZLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjExLzI4\
                    LzA4IDk6MjEsQyxaLDQuMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQNCjExLzUvMDggMTY6MDksRCxYLDQ\
                    uMzA0MDY1MDkzLDEuODY5MjMxNzIsNzQ=' 
        
        
        if pd.read_csv(main_path+'data_check.csv')['check'][0] == 0:
            data = {'File_1': [decode(data64_1)],
                    'File_2': [decode(data64_2)]}
        else:
            data = {'File_1': [pd.read_csv(main_path+'file1_data.csv')],
                    'File_2': [pd.read_csv(main_path+'file2_data.csv')]}
                
        # but update the document from callback
        doc.add_next_tick_callback(partial(update, data))

def datetime(x):
    return np.array(x, dtype = np.datetime64)

def record_data(source):    
    #source.data = decode(data).to_dict(orient='list')
    return source
        
def record_linegraph(record_datasource, file):    
    
    def graph(table):    
        table_rc = table.groupby(pd.to_datetime(table['Date']).dt.strftime('%W'))['Date'].count()
        table_rc = table_rc.rename('Record Counts').reset_index()
        
        sd = np.std(table_rc['Record Counts'])
        mean = np.mean(table_rc['Record Counts'])        
        y_max = max(table_rc['Record Counts']) + sd*2
        y_min = min(table_rc['Record Counts']) - sd*2
        
        table_rc['Upper Bound'] = table_rc['Record Counts'].apply(lambda x : mean+(sd*2))
        table_rc['Mid-Upper Bound'] = table_rc['Record Counts'].apply(lambda x : mean+(sd))        
        table_rc['Lower Bound'] = table_rc['Record Counts'].apply(lambda x : mean-(sd*2))
        table_rc['Mid-Lower Bound'] = table_rc['Record Counts'].apply(lambda x : mean-(sd))
    
        records = figure(x_axis_type="datetime",\
                         title="File Record Counts: Data points above or below 2x STDev lines indicate an unusual number of weekly records.",\
                         width = 750, height= 200, 
                         y_range=(y_min, y_max),\
                         tools='pan,box_zoom,hover,reset')
        
        
        records.xaxis.axis_label = 'Weekly Data Points'
        records.yaxis.axis_label = 'Record Counts'    
        records.circle(datetime(table_rc['Date']), table_rc['Record Counts'], color='#005D7B', fill_alpha=0.8, size=10)    
        records.line(datetime(table_rc['Date']), table_rc['Upper Bound'], color='#008DA9')
        records.line(datetime(table_rc['Date']), table_rc['Lower Bound'], color='#008DA9')
    
        return records
    
    
    records_graph = graph(record_datasource.data[file][0])

    
    return records_graph
  

def create_rawtable(record_datasource, file, size): 
      
    data_table = record_datasource.data[file][0]
    
    column_list = data_table.columns.tolist()
    column_titles = list()
    
    for i in range(0, len(column_list)):
        column_titles.append(TableColumn(field=column_list[i], title=column_list[i]))
    
    datatable_ = DataTable(source = ColumnDataSource(data_table.to_dict(orient='list')),\
                                                   columns = column_titles,\
                                                   width = size, \
                                                   height= 275,
                                                   css_classes =['custom_header'])
    return datatable_


def create_typetable(record_datasource, file, size): 
      
    data_table = record_datasource.data[file][0]
    
    data_table = data_table.dtypes.astype(str).rename('Data-Types').reset_index()
    
    
    column_list = data_table.columns.tolist()
    column_titles = list()
    
    for i in range(0, len(column_list)):
        column_titles.append(TableColumn(field=column_list[i], title=column_list[i]))
    
    datatable_ = DataTable(source = ColumnDataSource(data_table.to_dict(orient='list')),\
                                                   columns = column_titles,\
                                                   width = size, \
                                                   height= 150,
                                                   css_classes =['custom_header'])
    return datatable_


def create_desctable(record_datasource, file, size): 
      
    data_table = record_datasource.data[file][0]
    
    data_table = data_table.describe().reset_index()
    
    
    #datatable_ = PreText(text = str(data_table), width = 375)
    
    column_list = data_table.columns.tolist()
    column_titles = list()
    
    for i in range(0, len(column_list)):
        column_titles.append(TableColumn(field=column_list[i], title=column_list[i]))
    
    datatable_ = DataTable(source = ColumnDataSource(data_table.to_dict(orient='list')),\
                                                   columns = column_titles,\
                                                   width = size, \
                                                   height= 275,
                                                   css_classes =['custom_header'])
    return datatable_




record_datasource = record_data(source) 



def update_datasource():
    input_table1 = decode(file_input1.value)
    input_table1.to_csv(main_path+'file1_data.csv', index=False)
    
    input_table2 = decode(file_input2.value)
    input_table2.to_csv(main_path+'file2_data.csv', index=False)
       
    pd.DataFrame({'check':{0:1}}).to_csv(main_path+'data_check.csv', index=False)

    
    running_info.text = '<b>Status Bar</b>: Datasource is Updated ->->-> Please <b>REFRESH</b> Page'


def reset_datasource():
    pd.DataFrame({'check':{0:0}}).to_csv(main_path+'data_check.csv', index=False)


    running_info.text = '<b>Status Bar</b>: Reseting Dashboard to Demo Data ->->-> Please <b>REFRESH</b> Page'


hello = Div(text="""<b>Hello!</b>""", \
              width = 300,\
              style = {'font-size':'115%'})

 
welcome = Div(text="""Please <u>upload two files</u> for harmonization.<br>Note that file must include a column titled 'Date'""", \
              width = 300)

inst_1 = Div(text="""After chosing two files, click the <u>Update Data Files</u> button and <u>Refresh</u> your browser.""",\
             width = 300)


inst_2 = Div(text="""Once refreshed explore the <u>Join Key</u> and <u>Metric Pairs</u> tabs.\
                       Select the combination of columns to join your dataset on, and \
                       the metrics to compare between each file.""",\
                       width = 300)

inst_3 = Div(text = """Once youve made your selections click \
                       <u>Lock Pairs to Blend Data & Download"</u>\
                       Your output file will be in your downloads folder.""",\
                       width = 300)                       
                       





space_25 = Spacer(min_width = 25)
space_50 = Spacer(min_width = 50)  
space_80 = Spacer(min_width = 80) 
space_h10 = Spacer(min_height = 10)
space_h25 = Spacer(min_height = 25)
space_h50 = Spacer(min_height = 50)
 
class harmonize:
    
    def __init__(self, data):
               
        self.left_table = data['left_table']
        self.right_table = data['right_table']     
        self.left_keys = data['left_keys']
        self.right_keys = data['right_keys']
        self.metric_pairs = data['metric_lists']

        
        left_cols = ['left_' + x for x in self.left_table.columns.tolist()]
        right_cols = ['right_'+x for x in self.right_table.columns.tolist()]
        
        self.left_table.columns = left_cols
        self.right_table.columns = right_cols
        
        self.left_keys = ['left_' + x for x in self.left_keys]
        self.right_keys = ['right_' + x for x in self.right_keys]
        
        self.metric_pairs = [['left_'+x[0], 'right_'+x[1]] for x in self.metric_pairs]
        key_pairs = self.metric_pairs
        left_metrics = []
        right_metrics = []
        for i in range(0, len(key_pairs)):
            left_metrics.append(key_pairs[i][0])
            right_metrics.append(key_pairs[i][1])
        
        left_ = self.left_table.groupby(self.left_keys)[left_metrics].sum().reset_index()
        right_ = self.right_table.groupby(self.right_keys)[right_metrics].sum().reset_index()
        
        
        merged = pd.merge(left_, 
                          right_,
                          how = 'outer',
                          right_on = self.right_keys,
                          left_on = self.left_keys,
                          sort = False,
                          indicator = True)
                        
        split = dict(tuple(merged.groupby('_merge')))
        
        
        for df in merged:
            try:
                both_df = split['both']
                both_name = 'Merged on File'
            except KeyError:
                continue
            
        for df in merged:
            try:
                left_only = split['left_only']
                left_name = 'File 1'
            except KeyError:
                continue
            
        for df in merged:
            try:
                right_only = split['right_only']
                right_name = 'File 2'
            except KeyError:
                continue
       
        key_pairs = self.metric_pairs
        
        for i in range(0, len(key_pairs)):
            both_df['Difference '+str(key_pairs[i])] = both_df.apply(lambda x: x[key_pairs[i][0]] - x[key_pairs[i][1]],1)
            both_df['%Varaince '+ str(key_pairs[i])] = both_df.apply(lambda x: (x[key_pairs[i][0]] - x[key_pairs[i][1]])/np.mean([x[key_pairs[i][0]],x[key_pairs[i][1]]]),1)
        
        
        

        def get_download_path():
            """Returns the default downloads path for linux or windows"""
            if os.name == 'nt':
                import winreg
                sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
                downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                    location = winreg.QueryValueEx(key, downloads_guid)[0]
                return location    
            else:
                return os.path.join(os.path.expanduser('~'), 'downloads')
            
            
        with pd.ExcelWriter(get_download_path()+'/Comparison_File.xlsx') as writer:
            both_df.to_excel(writer, both_name)
            left_only.to_excel(writer, 'ONLY_'+left_name)
            right_only.to_excel(writer, 'ONLY'+right_name)
            


def blend_download():
    running_info.text = '<b>Status Bar</b>: Datasources are being harmonized ->->-> <b>Please Wait</b>'
    #Files
    file1 = record_datasource.data['File_1'][0]
    file2 = record_datasource.data['File_2'][0]

    left_keys = [key1A.value, key2A.value, key3A.value, key4A.value, key5A.value]
    left_keys = [str(x) for x in left_keys if x != 'None']
    right_keys = [key1B.value, key2B.value, key3B.value, key4B.value, key5B.value]
    right_keys = [str(x) for x in right_keys if x != 'None']
    
    metric_pairs = [[key6A.value, key6B.value],
                    [key7A.value, key7B.value],
                    [key8A.value, key8B.value],
                    [key9A.value, key9B.value],
                    [key10A.value, key10B.value]]
    
    metric_pairs = [ x for x in metric_pairs if 'None' not in x]
    
    data_dict = {'left_table':file1,
                 'right_table':file2,
                 'left_keys':left_keys,
                 'right_keys':right_keys,
                 'metric_lists':metric_pairs}
    
    running_info.text = '<b>Status Bar</b>: Datasources are being analyzed ->->-> <b>Please Wait</b>'
    
    harmonize(data_dict)
    
    running_info.text = '<b>Status Bar</b>: Please check your <b>downloads folder</b> for ->->-> <b>Comparison_File.xlsx</b>'
    


"""Widget Tab 1"""
file_input1 = FileInput(accept = '.csv')
file_1 = Paragraph(text='First File:')

file_input2 = FileInput(accept = '.csv')
file_2 = Paragraph(text='Second File:')

#lock model parameters
update_button = Button(label="Update Data Files", css_classes =['upload_button'], width=300)
update_button.on_click(update_datasource)

file_inputs = column(hello,
                     welcome,
                     Spacer(max_height=10),
                     row(file_1,file_input1), 
                     row(file_2, file_input2),
                     space_h10, inst_1,
                     row(update_button),
                     space_h25, inst_2, Spacer(min_height=20), inst_3,
                     max_width = 300)


widget_tab1 = Panel(child=file_inputs, title="   Start Here   ")

"""Widget Tab 2"""
column_list1 = ['None'] + record_datasource.data['File_1'][0].columns.tolist()
column_list2 = ['None'] + record_datasource.data['File_2'][0].columns.tolist()  


key1A = Select(title="Key 1A:", value=column_list1[0], options=column_list1, width =125)
key1B = Select(title="Key 1B:", value=column_list1[0], options=column_list1,width =125)

key2A = Select(title="Key 2A:", value=column_list1[0], options=column_list1, width =125)
key2B = Select(title="Key 2B:", value=column_list1[0], options=column_list1, width =125)

key3A = Select(title="Key 3A:", value=column_list1[0], options=column_list1, width=125)
key3B = Select(title="Key 3B:", value=column_list1[0], options=column_list1, width =125)

key4A = Select(title="Key 4A:", value=column_list1[0], options=column_list1, width=125)
key4B = Select(title="Key 4B:", value=column_list1[0], options=column_list1, width =125)

key5A = Select(title="Key 5A:", value=column_list1[0], options=column_list1, width =125)
key5B = Select(title="Key 5B:", value=column_list1[0], options=column_list1, width=125)

key6A = Select(title="Metric 1A:", value=column_list1[0], options=column_list1, width =125)
key6B = Select(title="Metric 1B:", value=column_list1[0], options=column_list1, width=125)

key7A = Select(title="Metric 2A:", value=column_list1[0], options=column_list1, width =125)
key7B = Select(title="Metric 2B:", value=column_list1[0], options=column_list1, width =125)

key8A = Select(title="Metric 3A:", value=column_list1[0], options=column_list1, width=125)
key8B = Select(title="Metric 3B:", value=column_list1[0], options=column_list1, width =125)

key9A = Select(title="Metric 4A:", value=column_list1[0], options=column_list1, width=125)
key9B = Select(title="Metric 4B:", value=column_list1[0], options=column_list1, width =125)

key10A = Select(title="Metric 5A:", value=column_list1[0], options=column_list1, width =125)
key10B = Select(title="Metric 5B:", value=column_list1[0], options=column_list1, width =125)

#start_date = DatePicker(width=150)
#end_date = DatePicker(width=150)





keys_title = Div(text= """Chose matched pairs to join data tables.""", 
                 width=300)

metrics_title = Div(text= """Chose matched pairs of metrics to analyze.""",
                    width=300)

Matching_Keys = column(keys_title,
                       row(key1A,key1B),
                       row(key2A,key2B),
                       row(key3A,key3B),
                       row(key4A,key4B),
                       row(key5A,key5B))

widget_tab2 = Panel(child=Matching_Keys, title="   Join Keys   ")

Matching_Metrics = column(metrics_title,
                          row(key6A,key6B),
                          row(key7A,key7B),
                          row(key8A,key8B),
                          row(key9A,key9B),
                          row(key10A,key10B))


widget_tab3 = Panel(child=Matching_Metrics, title='  Metric Pairs  ')

tabs_controls= Tabs(tabs=[widget_tab1, widget_tab2, widget_tab3])


#lock model parameters
lock_button = Button(label="Lock Pairs to Blend Data & Download", css_classes =['lock_button'], width=300)
lock_button.on_click(blend_download)

#lock model parameters
reset_button = Button(label="Reset Backend Data", css_classes =['reset_button'], width=100)
reset_button.on_click(reset_datasource)







#Data Tab 1
records_graph_1 = record_linegraph(record_datasource, 'File_1') 
raw_table_1 = create_rawtable(record_datasource, 'File_1', 725)

file_info_1 = column(records_graph_1,
                     space_h25,
                     raw_table_1)
 


#Data Tab 2
records_graph_2 = record_linegraph(record_datasource, 'File_2') 
raw_table_2 = create_rawtable(record_datasource, 'File_2', 725)


file_info_2 = column(records_graph_2,
                     space_h25,
                     raw_table_2)


#Data Tab 3
t1 = Div(text="""<b>File 1</b> Data Types and Descriptive Statistics""",
         style={'font-size': '100%',\
                'color': 'black',\
                'border-bottom': '3px',\
                 'border-style': 'solid',\
                 'border-color': '	#05BAC5',\
                 'background-color': 'white',\
                 'padding': '.75em'})
    
    
    
data_types1 = create_typetable(record_datasource, 'File_1', 300)
desc_data1 = create_desctable(record_datasource, 'File_1', 300)


t2 = Div(text="""<b>File 2</b> Data Types and Descriptive Statistics""",
         style={'font-size': '100%',\
                'color': 'black',\
                'border-bottom': '3px',\
                 'border-style': 'solid',\
                 'border-color': '	#05BAC5',\
                 'background-color': 'white',\
                 'padding': '.75em'})
    
data_types2 = create_typetable(record_datasource, 'File_2', 300)
desc_data2 = create_desctable(record_datasource, 'File_2', 300)

descriptive_data = row(space_25,
                       column(space_h25,
                              t1,
                              space_h10,
                              data_types1,
                              space_h25,
                              desc_data1),
                       space_25,
                       space_25,
                       column(space_h25,
                              t2,
                              space_h10,
                              data_types2,
                              space_h25,
                              desc_data2))
                       



tab1 = Panel(child=file_info_1, title="   First File   ")
tab2 = Panel(child=file_info_2, title='  Second File  ')
tab3 = Panel(child = descriptive_data, title = 'Descriptive Data')
tabs = Tabs(tabs=[ tab1,tab2, tab3])




date_1 = Paragraph(text='Start Date:')
date_2 = Paragraph(text='End Date   :')



control_layout = column(logo,
                        tabs_controls,

                        Spacer(min_height=25),
                 
                        lock_button)
                 

data_layout = column(Spacer(min_height=10),
                     row(running_info, 
                     Spacer(min_width = 25),
                     column(space_h10,
                            reset_button)),
                     Spacer(min_height=35),
                     tabs)
           




dash = row(space_80, control_layout, space_80, data_layout, space_50)


doc.add_root(dash)
doc.title = 'Blend & Analyze'

thread = Thread(target=blocking_task)
thread.start()