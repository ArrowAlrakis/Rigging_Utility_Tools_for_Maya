# ================================
# Script Name: Python_Tools_Utilities_v01.py
# Author: Arrow Lyu
# Date: 2024/09/30
# Description:
#   - A collection of multiple Maya tools in one UI module:
#       1. Object Snap
#       2. Show/Hide Local Axis
#       3. Add current project path to Maya python path
#       4. Combine many object shapes into one
#       5. Lock/Unlock Attributes UI
#       6. Create Ball control UI
#       7. Create Pole control UI
#       8. Create Label UI
# Usage:
#   - Use the functions directly or assign to shelf buttons.
#   - UI launchers are available for each tool inside this file.
# ================================

import sys; sys.dont_write_bytecode=True
import maya.cmds as cmds
import importlib
import time


#-------------------------------------------------------------------------
# Snap Object

def lyu_ObjSnap():
    tempConstraint = cmds.parentConstraint( weight=1 , maintainOffset=False )
    cmds.delete( tempConstraint )

#-------------------------------------------------------------------------
# Set python path to current maya project

def PPathUI():
    # - check if window already exists, if it does exists, delete it
    if (cmds.window( 'PythonPath_Window', exists = True )):
        print('found existing window, deleting')
        cmds.deleteUI( 'PythonPath_Window' )
    
    # - make a ui window
    myPythonPathWindow = cmds.window( 'PythonPath_Window' )
    
    # - make the window visible on screen
    cmds.showWindow( myPythonPathWindow )
    
    # - find the Maya workspace path
    myProjDir = cmds.workspace( q=True, rootDirectory=True )
    
    # - make the layout that maya demands to put the text into
    cmds.columnLayout( adjustableColumn=True )
    
    cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1,'right',10), columnWidth=((1, 240),(2, 480)) )
    
    # - make a place to put my new path string
    cmds.text( label='New Path to Add the Python Path' )
    myPathTextField = cmds.textField( text=myProjDir+'scripts/' )
    
    # - get back up one level to the single column layout
    cmds.setParent( '..' )
    
    # - make the command to print out the list of paths in the Python Path
    def printPythonPathList(foo):
        for s in sys.path:
            print( ' path --- ', s )
    
    # - make the command to add my custom path to the Python path
    def myCommand(foo):
        doCmd = True
        # - query the user input file path and capture the string as pathString
        pathString = cmds.textField( myPathTextField, q = True, text=True )
        # - find if my custom path exist in maya path lists, if it does, dont add the path and print WARNING
        for s in sys.path:
            if s == pathString:
                print( 'WARNING', pathString, 'already exists, not adding' )
                doCmd = False
        # - if my custom path does not exist in maya path lists, add my path
        if doCmd:
            sys.path.append( pathString )
    
    # - make a button to add my new path to the python sys path
    cmds.button( label='Add Projects Scripts Folder specified above to the python path', command=myCommand )
    
    # - make another button to print the list of path in Python Path
    cmds.button( label='Print Python Path', command=printPythonPathList )




#-------------------------------------------------------------------------
# Display local axis for all selected objects

def jly_showLocalAxis( yn=True ):
    # - find all selected objects, return full path name of each one (long=True)
    jly_objects = cmds.ls( selection=True, long=True )
    # - loop through every selected objects, display local axis for each one
    for obj in jly_objects:
        cmds.setAttr( obj+'.displayLocalAxis', yn )

# - make a window and buttons for Axis Ui

def AxisUI():
    # - check if window already exists, if it does exists, delete it
    if (cmds.window( 'ShowHideLocalAxis_Window', exists = True )):
        print('found existing window, deleting')
        cmds.deleteUI( 'ShowHideLocalAxis_Window' )
    # - make the window
    ShowHideLocalAxisWindow = cmds.window( 'ShowHideLocalAxis_Window' )
    # - make a column layout
    cmds.columnLayout( adjustableColumn=True )
    # - make buttons for display/hide local axis
    cmds.button( label='display local axis', command='jly_showLocalAxis(yn=True)' )
    cmds.button( label='hide local axis', command='jly_showLocalAxis(yn=False)' )
    
    # - make the window visible on screen
    cmds.showWindow( ShowHideLocalAxisWindow )




#-------------------------------------------------------------------------
# Combine many shapes into one object

def jly_CombineShapesIntoOneNode( worldSpace=False ):

    # - get a list of all the select objects
    jly_SelectedNodes = cmds.ls( selection=True, long=True )
    
    # - find the last selected node, which will be our new Ctrl object
    jly_CtrlNode = cmds.ls( selection=True, long=True, tail=True )[0]
    
    # - loop through all the selected objects
    for jly_node in jly_SelectedNodes:
        # - check if the jly_node is the last selected node, if not, then grab the shape
        if jly_node != jly_CtrlNode:
            # - find the shape nodes under the jly_node
            origShapeNodes = cmds.listRelatives( jly_node, children=True, shapes=True, fullPath=True )
            # - make a temporary group for duplication
            tempGrp = cmds.group( empty=True, name='temp_Grp' )
            
            # - make the tempGroup match the jly_node transform, keep the objects' orignal transform and world space information (maintainOffset=mo)
            tempParentCon = cmds.parentConstraint( jly_node, tempGrp, mo=False)
            tempScaleCon = cmds.scaleConstraint( jly_node, tempGrp, mo=False)
            cmds.delete( tempParentCon, tempScaleCon )
            
            # - temperarily move the shape under the tempGrp
            origShapeNodes = cmds.parent( origShapeNodes, tempGrp, shape=True, relative=True )
            # - find the full node path of the relocated shape node
            origShapeNodes = cmds.listRelatives( tempGrp, children=True, shapes=True, fullPath=True )
            # - make a duplicate of the tempGrp with the borrowed shape
            tempDupe = cmds.duplicate( tempGrp, name='dup_Grp' )
            # - get the path of the duplicate shape node
            newShapeNodes = cmds.listRelatives( tempDupe, children=True, shapes=True, fullPath=True )
            # -- put the original shape node back where it belongs
            cmds.parent( origShapeNodes, jly_node, shape=True, relative=True )
            
            # - parent the duplicate nodes under the jly_CtrlNode
            # - if worldSpace=True, reset the transform so the new shapes stay in the same place; else, move the shape to jly_CtrlNode
            if worldSpace:
                cmds.makeIdentity( tempDupe, apply=True )
                cmds.parent( newShapeNodes, jly_CtrlNode, shape=True, relative=True )
            else:
                cmds.parent( newShapeNodes, jly_CtrlNode, shape=True, relative=True )
            # - clean up the now empty temp groups
            cmds.delete( tempGrp, tempDupe )
            
        else:
            print( jly_node, 'IS', jly_CtrlNode )


# - make a window UI to use the combine shapes command
def Many1UI():
    # - check if window already exists, if it does exists, delete it
    if (cmds.window( 'CombineShapesIntoOneNode_Window', exists=True )):
        print( 'found existing UI, deleting' )
        cmds.deleteUI( 'CombineShapesIntoOneNode_Window' )
    
    # - make a new window 
    CombineShapesIntoOneNodeWindow = cmds.window( 'CombineShapesIntoOneNode_Window' )
    
    # - make a single column layout inside the window object
    cmds.columnLayout( adjustableColumn=True )
    
    # - make a 2 row column layout for the text label and do True/False of the world space
    one = cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 10), columnWidth=[(1, 160), (2, 100)] )
    cmds.text( label='use World Space' )
    worldSpace_YN = cmds.intField()
    cmds.setParent('..')
    
    # - make a command that works for the Ctrl
    def makeCmd(ignore):
        # - query the interger field user input is 0 or 1 
        worldSpaceValue = cmds.intField( worldSpace_YN, query=True, value=True)
        # - run combine shape command with the input interger
        jly_CombineShapesIntoOneNode( worldSpace=worldSpaceValue )
    
    # - make a button to run the command
    cmds.button ( label='Combine Shapes', command=makeCmd )
    
    # - make the window visible on screen
    cmds.showWindow( CombineShapesIntoOneNodeWindow )


#-------------------------------------------------------------------------
# Lock/Unlock attribute for Translate, Rotate, Scale, and Visibility

# - Lock attribute
def jly_LockAttr(jlyT=True,jlyR=True,jlyS=True,jlyV=True):
    # - make a list of selected object (True = run command, False = dont do anything)
    objs = cmds.ls (sl=True)
    # - loop through the list, check if T, R, S, V is true or false, if true then lock the attribute
    for obj in objs:
        if jlyT:
            cmds.setAttr (obj+'.tx', lock=True, keyable=False, channelBox=False)
            cmds.setAttr (obj+'.ty', lock=True, keyable=False, channelBox=False)
            cmds.setAttr (obj+'.tz', lock=True, keyable=False, channelBox=False)
        if jlyR:
            cmds.setAttr (obj+'.rx', lock=True, keyable=False, channelBox=False)
            cmds.setAttr (obj+'.ry', lock=True, keyable=False, channelBox=False)
            cmds.setAttr (obj+'.rz', lock=True, keyable=False, channelBox=False)
        if jlyS:
            cmds.setAttr (obj+'.sx', lock=True, keyable=False, channelBox=False)
            cmds.setAttr (obj+'.sy', lock=True, keyable=False, channelBox=False)
            cmds.setAttr (obj+'.sz', lock=True, keyable=False, channelBox=False)
        if jlyV:
            cmds.setAttr (obj+'.v', lock=True, keyable=False, channelBox=False)


# - Unlock attribute
def jly_UnLockAttr(jlyT=True,jlyR=True,jlyS=True,jlyV=True):
    objs = cmds.ls (sl=True)
    # - loop through the list, check if T, R, S, V is true or false, if false then unlock the attribute
    for obj in objs:
        if jlyT:
            cmds.setAttr (obj+'.tx', lock=False, keyable=True )
            cmds.setAttr (obj+'.ty', lock=False, keyable=True )
            cmds.setAttr (obj+'.tz', lock=False, keyable=True )
        if jlyR:
            cmds.setAttr (obj+'.rx', lock=False, keyable=True )
            cmds.setAttr (obj+'.ry', lock=False, keyable=True )
            cmds.setAttr (obj+'.rz', lock=False, keyable=True )
        if jlyS:
            cmds.setAttr (obj+'.sx', lock=False, keyable=True )
            cmds.setAttr (obj+'.sy', lock=False, keyable=True )
            cmds.setAttr (obj+'.sz', lock=False, keyable=True )
        if jlyV:
            cmds.setAttr (obj+'.v', lock=False, keyable=True )



def LockUI():
    # - check if window already exists, if it does exists, delete it
    if (cmds.window( 'LockUnlock_Window', exists=True )):
        print( 'found existing UI, deleting' )
        cmds.deleteUI( 'LockUnlock_Window' )
    # - make the window
    LockUnlockWindow = cmds.window( 'LockUnlock_Window' )
    # - make a 1 column layout
    cmds.columnLayout( adjustableColumn=True )
    # - make buttons for lock/unlock everything/translate/rotate/scale/visibility
    cmds.button( label='Lock All', command='jly_LockAttr()' )
    cmds.button( label='Unlock All', command='jly_UnLockAttr()' )
    cmds.button( label='Lock Translate', command='jly_LockAttr( jlyR=False, jlyS=False, jlyV=False )' )
    cmds.button( label='Unlock Translate', command='jly_UnLockAttr( jlyR=False, jlyS=False, jlyV=False )' )
    cmds.button( label='Lock Rotate', command='jly_LockAttr( jlyT=False, jlyS=False, jlyV=False )' )
    cmds.button( label='Unlock Rotate', command='jly_UnLockAttr( jlyT=False, jlyS=False, jlyV=False )' )
    cmds.button( label='Lock Scale', command='jly_LockAttr( jlyT=False, jlyR=False, jlyV=False )' )
    cmds.button( label='Unlock Scale', command='jly_UnLockAttr( jlyT=False, jlyR=False, jlyV=False )' )
    cmds.button( label='Lock Visibility', command='jly_LockAttr( jlyT=False, jlyR=False, jlyS=False )' )
    cmds.button( label='Unlock Visibility', command='jly_UnLockAttr( jlyT=False, jlyR=False, jlyS=False )' )
    
    # - make the window visible on screen
    cmds.showWindow( LockUnlockWindow )



#-------------------------------------------------------------------------
#### Control Objects
#-------------------------------------------------------------------------
# MakeBall

def jly_MakeBall (nodeName='Ball_Ctrl',pos=(0,0,0),radius=1,doT=False):
    # -- make a ball
    # - create a empty transform node called 'Ball_Ctrl'
    jly_Ctrl = cmds.createNode( 'transform', name=nodeName )
    # - only lock scale attribute for the empty transform node, leave translate/rotate/visibility unlocked
    jly_LockAttr(False,False,True,False)
    # - create 3 empty nurbCurve shape nodes, parent them under the empty transform node
    jly_Shape1 = cmds.createNode( 'nurbsCurve', parent=jly_Ctrl )
    jly_Shape2 = cmds.createNode( 'nurbsCurve', parent=jly_Ctrl )
    jly_Shape3 = cmds.createNode( 'nurbsCurve', parent=jly_Ctrl )
    # - create 3 makeNurbCircle nodes
    jly_Geo1 = cmds.createNode( 'makeNurbCircle' )
    jly_Geo2 = cmds.createNode( 'makeNurbCircle' )
    jly_Geo3 = cmds.createNode( 'makeNurbCircle' )
    
    # - notes: .cc = .outputCurve, .cr = .create, .nr = .normal, .c  = .center, .r  = .radius
    # - connect the created geometry nodes (makeNurbCircle) to the shape nodes (nurbsCurve), so the nurbsCurve show up
    cmds.connectAttr( str(jly_Geo1)+'.oc', str(jly_Shape1)+'.cr' )
    # - change the normal of the nurbsCurve orientation
    cmds.setAttr( str(jly_Geo1)+'.nr',1,0,0)
    # - offset the center position of the circle
    cmds.setAttr( str(jly_Geo1)+'.c',pos[0],pos[1],pos[2])
    # - set the radius for the circle
    cmds.setAttr( str(jly_Geo1)+'.r',radius)
    # - do the same for another 2 circles
    cmds.connectAttr( str(jly_Geo2)+'.oc', str(jly_Shape2)+'.cr' )
    cmds.setAttr( str(jly_Geo2)+'.nr',0,1,0)
    cmds.setAttr( str(jly_Geo2)+'.c',pos[0],pos[1],pos[2])
    cmds.setAttr( str(jly_Geo2)+'.r',radius)
    cmds.connectAttr( str(jly_Geo3)+'.oc', str(jly_Shape3)+'.cr' )
    cmds.setAttr( str(jly_Geo3)+'.nr',0,0,1)
    cmds.setAttr( str(jly_Geo3)+'.c',pos[0],pos[1],pos[2])
    cmds.setAttr( str(jly_Geo3)+'.r',radius)
    
    # - make a T control for the ball, create a line between the middle of the ball and the actual pivot
    if doT:
        # - make a curve by giving two point, one at the origin, the other at the middle of the ball
        tmp = cmds.curve( name=nodeName+'_crap', degree=1, p=[(0,0,0),(pos[0],pos[1],pos[2])])
        # - find the shape node
        jly_ShapeNodes = cmds.listRelatives( tmp, children=True, shapes=True, fullPath=True )
        # - parent the shape node under the main control group
        cmds.parent(jly_ShapeNodes, jly_Ctrl, shape=True, relative=True )
        # - delete the now empty transform node
        cmds.delete(tmp)
    # - leave the created main control group selected
    cmds.select(jly_Ctrl, replace=True )
    # - says in the output window what the control made
    return jly_Ctrl


# - Create a window UI for Make Ball
def BallUI():
    # - check if window already exists, if it does exists, delete it
    if (cmds.window( 'BallCtrl_Window', exists=True )):
        print( 'found existing UI, deleting' )
        cmds.deleteUI( 'BallCtrl_Window' )
    
    # - create the window
    BallCtrlWindow = cmds.window( 'BallCtrl_Window' )
    # - create a 1 column layout inside the window
    cmds.columnLayout( adjustableColumn=True )
    # - create a 2 row column layout for the name of the Ctrl
    nodeNameLayout = cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 10), columnWidth=[(1, 80), (2, 240)] )
    # - create a label with annotation
    cmds.text( label='Node Name', ann='Name of the Ball Control'  )
    # - create a textField with the actual node name you want to use, by default the name is 'Ball_Ctrl'
    nodeName_Ball = cmds.textField( text='Ball_Ctrl' )
    # - go up 1 level, out of this column layout
    cmds.setParent('..')
    
    # - create a 4 row column layout for the X, Y, Z position of the Ctrl
    poslayout = cmds.rowColumnLayout( numberOfColumns=4, columnAttach=(1, 'right', 10), columnWidth=[(1, 80), (2, 80), (3, 80), (4, 80)] )
    # - create text label with annotation (ann = annotation)
    cmds.text( label='Position', ann='Offset of the Ball Shape\n from its own center pivot\n (used for T style contros)'  )
    # - create 3 floatField for position X, Y, Z
    posX_Ball = cmds.floatField( value=0 )
    posY_Ball = cmds.floatField( value=0 )
    posZ_Ball = cmds.floatField( value=0 )
    # - go back up 1 level
    cmds.setParent('..')
    
    # - create a 2 row column layout for the radius and the doT of the Ctrl
    one = cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 10), columnWidth=[(1, 80), (2, 240)] )
    # - create text label with annotation
    cmds.text( label='Radius', ann='Size of the Ball Shape'  )
    # - create floatField for radius
    radius_Ball = cmds.floatField( value=1.0 )
    # - create text label with annotation
    cmds.text( label='Do T', ann='Add a line from the Control origin to the center of the Ball Shape\n to make a T style Control'  )
    # - create a integer field for doT 0 or 1, the default is 0
    doT_Ball = cmds.intField()
    # - go back up 1 level
    cmds.setParent('..')
    
    # -- create a command that builds the Ctrl
    def makeCmd(foo):
        # - query all the user input and get the information needed for the command
        nodeNameString = cmds.textField( nodeName_Ball, query=True, text=True )
        posValueX = cmds.floatField( posX_Ball, query=True, value=True )
        posValueY = cmds.floatField( posY_Ball, query=True, value=True )
        posValueZ = cmds.floatField( posZ_Ball, query=True, value=True )
        posValue = ( posValueX, posValueY, posValueZ )
        radiusValue = cmds.floatField( radius_Ball, query=True, value=True)
        doTValue = cmds.intField( doT_Ball, query=True, value=True)
        # - run the MakeBall command with all the user input
        jly_MakeBall( nodeName=nodeNameString, pos=posValue, radius=radiusValue, doT=doTValue )
    
    # - make a button to run the command, add annotation with it
    cmds.button ( label='Make Ball Control', command=makeCmd, ann='Make the Ball Control\n using the options spcified above' )
    
    # - make the window visible on screen
    cmds.showWindow( BallCtrlWindow )


#-------------------------------------------------------------------------
# MakePole

def jly_MakePole (nodeName='Pole_Ctrl',pos=(0,0,0),radius=1,doT=False):
    # -- make a pole
    # - create a empty transform node called 'Pole_Ctrl'
    jly_Ctrl = cmds.createNode( 'transform', name=nodeName )
    # - only lock scale attribute for the empty transform node, leave translate/rotate/visibility unlocked
    jly_LockAttr(False,False,True,False)
    # - create 3 empty nurbCurve shape nodes, parent them under the empty transform node
    jly_Shape1 = cmds.createNode( 'nurbsCurve', parent=jly_Ctrl )
    jly_Shape2 = cmds.createNode( 'nurbsCurve', parent=jly_Ctrl )
    jly_Shape3 = cmds.createNode( 'nurbsCurve', parent=jly_Ctrl )
    # - create 3 makeNurbCircle nodes
    jly_Geo1 = cmds.createNode( 'makeNurbCircle' )
    jly_Geo2 = cmds.createNode( 'makeNurbCircle' )
    jly_Geo3 = cmds.createNode( 'makeNurbCircle' )
    
    # - notes: .cc = .outputCurve, .cr = .create, .nr = .normal, .c  = .center, .r  = .radius
    # - connect the created geometry nodes (makeNurbCircle) to the shape nodes (nurbsCurve), so the nurbsCurve show up
    cmds.connectAttr( str(jly_Geo1)+'.oc', str(jly_Shape1)+'.cr' )
    # - change the normal of the nurbsCurve orientation
    cmds.setAttr( str(jly_Geo1)+'.nr',1,0,0)
    # - offset the center position of the curve
    cmds.setAttr( str(jly_Geo1)+'.c',pos[0],pos[1],pos[2])
    # - set the radius for the curve
    cmds.setAttr( str(jly_Geo1)+'.r',radius)
    # - set the degree of the curve to make the Pole shape
    cmds.setAttr( str(jly_Geo1)+'.degree',1)
    # - set the sections 4 to make the curve into a square shape
    cmds.setAttr( str(jly_Geo1)+'.sections',4)
    # - do the same for another 2 curves
    cmds.connectAttr( str(jly_Geo2)+'.oc', str(jly_Shape2)+'.cr' )
    cmds.setAttr( str(jly_Geo2)+'.nr',0,1,0)
    cmds.setAttr( str(jly_Geo2)+'.c',pos[0],pos[1],pos[2])
    cmds.setAttr( str(jly_Geo2)+'.r',radius)
    cmds.setAttr( str(jly_Geo2)+'.degree',1)
    cmds.setAttr( str(jly_Geo2)+'.sections',4)
    cmds.connectAttr( str(jly_Geo3)+'.oc', str(jly_Shape3)+'.cr' )
    cmds.setAttr( str(jly_Geo3)+'.nr',0,0,1)
    cmds.setAttr( str(jly_Geo3)+'.c',pos[0],pos[1],pos[2])
    cmds.setAttr( str(jly_Geo3)+'.r',radius)
    cmds.setAttr( str(jly_Geo3)+'.degree',1)
    cmds.setAttr( str(jly_Geo3)+'.sections',4)
    
    # - make a T control for the ball, create a line between the middle of the ball and the actual pivot
    if doT:
        # - make a curve by giving two point, one at the origin, the other at the middle of the ball
        tmp = cmds.curve( name=nodeName+'_crap', degree=1, p=[(0,0,0),(pos[0],pos[1],pos[2])])
        # - find the shape node
        jly_ShapeNodes = cmds.listRelatives( tmp, children=True, shapes=True, fullPath=True )
        # - parent the shape node under the main control group
        cmds.parent(jly_ShapeNodes, jly_Ctrl, shape=True, relative=True )
        # - delete the now empty transform node
        cmds.delete(tmp)
    # - leave the created main control group selected
    cmds.select(jly_Ctrl, replace=True )
    # - says in the output window what the control made
    return jly_Ctrl


# - Create a window UI for Make Pole
def PoleUI():
    # - check if window already exists, if it does exists, delete it
    if (cmds.window( 'PoleCtrl_Window', exists=True )):
        print( 'found existing UI, deleting' )
        cmds.deleteUI( 'PoleCtrl_Window' )
    
    # - create the window
    PoleCtrlWindow = cmds.window( 'PoleCtrl_Window' )
    # - create a 1 column layout inside the window
    cmds.columnLayout( adjustableColumn=True )
    # - create a 2 row column layout for the name of the Ctrl
    nodeNameLayout = cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 10), columnWidth=[(1, 80), (2, 240)] )
    # - create a label with annotation
    cmds.text( label='Node Name', ann='Name of the Pole Control'  )
    # - create a textField with the actual node name you want to use, by default the name is 'Pole_Ctrl'
    nodeName_Pole = cmds.textField( text='Pole_Ctrl' )
    # - go up 1 level, out of this column layout
    cmds.setParent('..')
    
    # - create a 4 row column layout for the X, Y, Z position of the Ctrl
    poslayout = cmds.rowColumnLayout( numberOfColumns=4, columnAttach=(1, 'right', 10), columnWidth=[(1, 80), (2, 80), (3, 80), (4, 80)] )
    # - create text label with annotation (ann = annotation)
    cmds.text( label='Position', ann='Offset of the Pole Shape\n from its own center pivot\n (used for T style contros)'  )
    # - create 3 floatField for position X, Y, Z
    posX_Pole = cmds.floatField( value=0 )
    posY_Pole = cmds.floatField( value=0 )
    posZ_Pole = cmds.floatField( value=0 )
    # - go back up 1 level
    cmds.setParent('..')
    
    # - create a 2 row column layout for the radius and the doT of the Ctrl
    one = cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 10), columnWidth=[(1, 80), (2, 240)] )
    # - create text label with annotation
    cmds.text( label='Radius', ann='Size of the Pole Shape'  )
    # - create floatField for radius
    radius_Pole = cmds.floatField( value=1.0 )
    # - create text label with annotation
    cmds.text( label='Do T', ann='Add a line from the Control origin to the center of the Pole Shape\n to make a T style Control'  )
    # - create a integer field for doT 0 or 1, the default is 0
    doT_Pole = cmds.intField()
    # - go back up 1 level
    cmds.setParent('..')
    
    # -- create a command that builds the Ctrl
    def makeCmd(foo):
        # - query all the user input and get the information needed for the command
        nodeNameString = cmds.textField( nodeName_Pole, query=True, text=True )
        posValueX = cmds.floatField( posX_Pole, query=True, value=True )
        posValueY = cmds.floatField( posY_Pole, query=True, value=True )
        posValueZ = cmds.floatField( posZ_Pole, query=True, value=True )
        posValue = ( posValueX, posValueY, posValueZ )
        radiusValue = cmds.floatField( radius_Pole, query=True, value=True)
        doTValue = cmds.intField( doT_Pole, query=True, value=True)
        # - run the MakePole command with all the user input
        jly_MakePole( nodeName=nodeNameString, pos=posValue, radius=radiusValue, doT=doTValue )
    
    # - make a button to run the command, add annotation with it
    cmds.button ( label='Make Pole Control', command=makeCmd, ann='Make the Pole Control\n using the options spcified above' )
    
    
    # - make the window visible on screen
    cmds.showWindow( PoleCtrlWindow )


#-------------------------------------------------------------------------
# MakeLabel


def jly_MakeLabel (nodeName='Label_Ctrl',pos=(0,0,0),radius=1,doT=False,label='abcdef',doCircle=True):
    # - create an empty transform group named after the input of the 'nodeName' 
    jly_Ctrl = cmds.createNode( 'transform', name=nodeName )
    # -- make contrl circle
    if doCircle == True:
        # - create a nurbsCurve node and parent it under the jly_Ctrl node
        jly_Shape1 = cmds.createNode( 'nurbsCurve', parent=jly_Ctrl )
        # - create a makeNurbCircle node
        jly_Geo1 = cmds.createNode( 'makeNurbCircle' )
        # - connect the output of the makeNurbCircle geometry node 'jly_Geo1' to the input of the shape node 'jly_Shape1'
        cmds.connectAttr( str(jly_Geo1)+'.oc', str(jly_Shape1)+'.cr' )
        # - set the normal so the nurbcircle is flat on the ground plane
        cmds.setAttr( str(jly_Geo1)+'.nr',0,1,0)
        # - set the radius of that circle to be the input of 'radius'
        cmds.setAttr( str(jly_Geo1)+'.r',radius)    
    
    # -- create a textCurve with font, actual text = the input of 'label', and capture this textCurve node as textNode
    textNode = cmds.textCurves( font='Arial', text=label, object=True )
    # - scale the text to be about the size of the size of the circle
    cmds.xform( s=(radius*0.25,radius*0.25,radius*0.25) )
    # - find out the boundingBox size of the text
    # - use textNode[0] to find the first in the list of the text group, bbx is in worldSpace. Print( bbx ) = ( x Min, y Min, Zmin, x Max, y Max, z Max )
    bbx = cmds.xform(textNode[0], q=True, bb=True, ws=True)
    # -- position the Text
    # - if doT, shift the text and make its center line up with the origin, else then put the text at the side of the origin
    if doT:
        # - take Xmax and Ymax of the bbx, roughly put it aside of the origin of X and Y axis
        cmds.xform( t=(bbx[3]*0.05,-bbx[4]*0.5,0) )
        # - shift the text according to the input position of 'pos', relative=True
        cmds.xform( t=(pos[0],pos[1],pos[2]), r=True )
    else:
        # - take Xmax and Ymax of the bbx, roughly center the text in X and Y axis
        cmds.xform( t=(-bbx[3]*0.5,-bbx[4]*1.5,0) )
        cmds.xform( t=(pos[0],pos[1],pos[2]), r=True )      
    
    # - find all the nurbCurves in the text, ad=allDescendents
    textShapes = cmds.listRelatives( textNode[0], ad=True, type='nurbsCurve', fullPath=True)
    # - delete text generator node to delete construct history
    cmds.delete( textNode[1] )
    # - reset the text to freeze its transform, apply the accumulated transforms
    cmds.makeIdentity( textNode[0], apply=True )
    # - parent all nurbCurve shape node under the jly_Ctrl
    cmds.parent( textShapes, jly_Ctrl, shape=True, relative=True )
    # - delete the now empty text shape empty groups
    cmds.delete( textNode[0] )
    
    # - make a T control for the label, create a line between the label and the actual pivot
    if doT:
        tmp = cmds.curve( name=nodeName+'_crap', degree=1, p=[(0,0,0),(pos[0],pos[1],pos[2])])
        jly_ShapeNodes = cmds.listRelatives( tmp, children=True, shapes=True, fullPath=True )
        cmds.parent(jly_ShapeNodes, jly_Ctrl, shape=True, relative=True )
        cmds.delete(tmp)    
    # - leave the top node selected
    cmds.select(jly_Ctrl, replace=True )
    # - return the name of the node created in the output window
    return jly_Ctrl


# - Create Make Label UI
def LabelUI():
    # - check if window already exists, if it does exists, delete it
    if (cmds.window("LabelCtrl_Window", exists=True)):
        cmds.deleteUI("LabelCtrl_Window")
    
    # - create a window with fields for entering text
    labelWindow = cmds.window('LabelCtrl_Window')
    # - create column layout
    cmds.columnLayout( adjustableColumn=True )
    
    # -- create 2 row column layout for node name
    nodeNameLayout = cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 10), columnWidth=[(1, 80), (2, 240)] )
    # - write text with annotation, ann = annotation
    cmds.text( label='Node Name', ann='Name of the Label Control' )
    # - input the name of Label Ctrl
    nodeName_Label = cmds.textField( text='Label_Ctrl' )
    # - go back up one level out of the row columns, back to single column
    cmds.setParent('..')
    
    # -- make a 4 row column layout for the position
    poslayout = cmds.rowColumnLayout( numberOfColumns=4, columnAttach=(1, 'right', 10), columnWidth=[(1, 80), (2, 80), (3, 80), (4, 80)] )
    # - add text 'position' with annotation
    cmds.text( label='Position', ann='Offset of the Label Shape\n from its own center pivot\n (used for T style contros)' )
    # - make 3 cells for X Y Z value input
    posX_Label = cmds.floatField( value=0 )
    posY_Label = cmds.floatField( value=0 )
    posZ_Label = cmds.floatField( value=0 )
    cmds.setParent('..')
    
    # -- make a 2 row column layout for radius, do T, and circle
    foo = cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 10), columnWidth=[(1, 80), (2, 240)] )
    # - create text for radius
    cmds.text( label='Radius', ann='Size of the Label Shape' )
    # - create float field for radius with a default = 10
    radius_Label = cmds.floatField( value=10 )
    # - create text for 'Do T?'
    cmds.text( label='Do T', ann='Add a line from the Control origin to the base of the Label Shape\n to make a T style Control' )
    # - create integer field fot input 1 or 0
    doT_Label = cmds.intField()
    # - create text for the visible label text
    cmds.text( label='Label', ann='Specify the text you want in your Label' )
    # - create text field for label name input
    label_Label = cmds.textField( text='your label here' )
    # - create text for 'Do Circle?'
    cmds.text( label='Do Circle', ann='Add a cirle at the Control origin to act as the Start Circle' )
    # - create integer field fot input 1 or 0
    doCircle_Label = cmds.intField( value=1 )
    cmds.setParent('..')
    
    # - make the command to actually create the label contrl
    def makeCmd(ignore):
        # -- query the 6 input and find out what the user put in each of them
        nodeNameString = cmds.textField( nodeName_Label, query=True, text=True)
        # - query pos X, pos Y, pos Z and combine them into one line in the posValue
        posValue = (cmds.floatField( posX_Label, query=True, value=True),cmds.floatField( posY_Label, query=True, value=True),cmds.floatField( posZ_Label, query=True, value=True))
        radiusValue = cmds.floatField( radius_Label, query=True, value=True)
        doTValue = cmds.intField( doT_Label, query=True, value=True)
        labelString = cmds.textField( label_Label, query=True, text=True)
        doCircleValue = cmds.intField( doCircle_Label, query=True, value=True)
        # - run the make label command with all the 6 values queried
        jly_MakeLabel(nodeName=nodeNameString,pos=posValue,radius=radiusValue,doT=doTValue,label=labelString,doCircle=doCircleValue)
    
    # - add a button to run the entire command
    cmds.button ( label='Make Label Control', command=makeCmd, ann='Make the Label Control\n using the options spcified above' )
    # - make the window visible on screen
    cmds.showWindow(labelWindow)


