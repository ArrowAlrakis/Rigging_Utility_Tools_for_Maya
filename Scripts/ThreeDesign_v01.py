# ================================
# Script Name: ThreeDesign_v01.py
# Author: Arrow Lyu
# Date: 2019/06/26
# Description: Maya Tool - UI for generating three design patterns:
#              - Phyllotactic (spiral) pattern of spheres
#              - Circle pattern of curves
#              - Square pattern of NURBS squares
# Usage:
#   - Run the script in Maya to open a window with three designs.
# ================================

import maya.cmds as cmds
import math as math


# create main window
def ui():
    # make sure there is no window exist before create a new one
    if cmds.window('Three Design', ex=True):
        cmds.deleteUI('Three Design')
    win=cmds.window('Three Design')
    # center the layout
    cmds.columnLayout(adj=True)
    
    # content for the first design Phtllotactic pattern
    cmds.separator(height=20)
    cmds.text('First Design Creates Phtllotactic Pattern')
    cmds.separator(height=10)
    # give 3 textfield for user input
    cmds.text('How many sphere do you want? (Recommend 300)')
    cmds.textField('t1', h=30)
    cmds.text('Put the radius of your sphere(Recommend 4):')
    cmds.textField('radius1', h=30)
    cmds.text('Put the space between your sphere(Recommend 4):')
    cmds.textField('cspread1', h=30)
    cmds.button('Phtllotactic Design', h=40, c='drawPhyllotacticPattern()', bgc=[0.5,0.1,0.2])
    
    # content for the second design circle Pattern
    cmds.separator(height=50)
    cmds.text('Second Design Creates Circle Pattern')
    cmds.separator(height=10)
    # give 1 textfield for user input
    cmds.text('How wide your circle spread? (Recommend 180)')
    cmds.textField('circleDegree1', h=30)
    cmds.button('Circle Design', h=40, c='CirclePattern()',  bgc=[0.2,0.1,0.3])
    
    # content for the third design square Pattern
    cmds.separator(height=50)
    cmds.text('Third Design Creates Square Pattern')
    cmds.separator(height=10)
    # give 2 textfield for user input
    cmds.text('How many square do you want? (Recommend 100)')
    cmds.textField('numSquare1', h=30)
    cmds.text('How big your square in the center is? (Recommend 2)')
    cmds.textField('size1', h=30)
    cmds.button('Square Design', h=40, c='SquarePattern()',  bgc=[0.8,0.2,0.8])
    
    # create window "win"
    cmds.showWindow(win)
    
###################################################################################################
'''
1. create 3 designs
'''
# a function that makes a Phtllotactic Pattern
# t=how many sphere you want, radius=radius of sphere, cspread=space between spheres
def drawPhyllotacticPattern():
    # assign variables
    radius=int(cmds.textField('radius1', q=True, text=True))
    cspread=int(cmds.textField('cspread1', q=True, text=True))
    t=int(cmds.textField('t1', q=True, text=True))
    angle = 137.508
    phi = angle * ( math.pi / 180.0 ) 
    xcenter = 0.0
    ycenter = 0.0
    # create group node
    design1grp=cmds.createNode("transform", name='Phtllotactic_Pattern')
    # for loops iterate from the first value until < 4 
    for n in range(t): 
        r = cspread * math.sqrt(n) 
        theta = n * phi 
        # equation for transform x and z                  
        x = r * math.cos(theta) + xcenter 
        y = r * math.sin(theta) + ycenter       
        # draw sphere  
        drawSphere = cmds.sphere(r=radius)[0]
        cmds.xform(drawSphere, t=(x,0,y))
        # put the whole pattern in a group
        cmds.parent(drawSphere, design1grp)
        
###################################################################################################
# a function that draws a circle pattern
# circleDegree=the degree those circle spread 
def CirclePattern():
    # assign variables
    circleDegree=int(cmds.textField('circleDegree1', q=True, text=True))
    # create group node
    design2grp=cmds.createNode("transform", name='Circle_Pattern')
    #cmds.createNode("transform", name='Circle_Pattern2')
    # a loop to rotate and scale circles
    for i in range(circleDegree):
        degree=i
        # equation to draw a circle
        radian=i/180.0*math.pi
        x=math.cos(radian)
        y=math.sin(radian)
        z=i*0.01
        # draw circles on y axis side
        drawCircle1=cmds.circle(r=1+i*0.01)[0]
        cmds.xform(drawCircle1, t=(x,y,z))
        # put circles in a group
        cmds.parent(drawCircle1, design2grp)
        # draw circles on -y axis side
        drawCircle2=cmds.circle(r=1+i*0.01)[0]
        cmds.xform(drawCircle2, t=(-x,-y,-z))
        # put circles in a second group
        cmds.parent(drawCircle2, design2grp)

###################################################################################################
# a function that draws a square pattern
# numSquare=the number of squares, size=size of the center square
def SquarePattern():
    # assign variables
    numSquare=int(cmds.textField('numSquare1', q=True, text=True))
    size=int(cmds.textField('size1', q=True, text=True))
    # create group node
    design3grp=cmds.createNode("transform", name='Square_Pattern')
    # a loop to rotate and scale squares
    for i in range(numSquare):
        z=2*math.sin(i)
        drawSquare=cmds.nurbsSquare(sl1=size*0.1+i*0.01, sl2=size*0.1+i*0.01)[0]
        cmds.xform(drawSquare, r=True, ro=(0,0,5*i), t=(0,0,z))
        # put squares in a group
        cmds.parent(drawSquare, design3grp)


###################################################################################################
# call functions
ui()