# ================================
# Script Name: RebuildJointChain_v01.py
# Author: Arrow Lyu
# Date: 2025/03/20
# Description:
#   - Rebuilds a joint chain based on selected joint hierarchy.
#   - New joints are positioned according to original positions.
# Usage:
#   - Select root joint and run.
# ================================


# create main window
def ui():
    # make sure there is no window exist before create a new one
    if cmds.window('Joint Tool', ex=True):
        cmds.deleteUI('Joint Tool')
    win=cmds.window('Joint Tool')
    # center the layout
    cmds.columnLayout(adj=True)
    
    # content for recreate joints
    cmds.text('How to use:')
    cmds.separator(height=10)
    cmds.text('1. Select parent joint to recreates joints')
    cmds.text('2. Input the number of joints you want')
    cmds.text('3. Generate your new joint chain')
    cmds.separator(height=10)
    # give 2 textfield for user input
    cmds.text('How many new joints do you want?')
    cmds.textField('joint_number1', h=30)
    cmds.button('Create Joints', h=40, c='create_new_joint()',  bgc=[0.05,0.7,0.9])
    # create window "win"
    cmds.showWindow(win)
    
###################################################################################################       
'''
1. recreate joints
'''
# function to create new joints and hide old ones
def create_new_joint():
    # assign variables
    joint_number=int(cmds.textField('joint_number1', q=True, text=True))
    
    # select old joints, and put them in a list
    original_joint=cmds.ls(sl=True,l=True)[0]
    # make a new list with old joints and  reverse
    original_joint_list=cmds.listRelatives(original_joint, ad=True,f=True)
    original_joint_list.reverse()
    original_joint_list.insert(0,original_joint)
    # get position information in list
    post_list=[cmds.xform(i, q=True, ws=True, t=True) for i in original_joint_list]
    
    # create curve along old joints
    path=cmds.curve(n='post_curve', d=1, p=(post_list))
    # rebuild curve to set parameter range to 0-1
    cmds.rebuildCurve(n='path',d=1,kr=0,kcp=True)
        
    # hide old joints
    cmds.hide(original_joint_list)
    
    # create new joints, and put them on motionpath one by one
    motionpath_list=[]
    joint_group=[]   
    for i in range(joint_number):
        cmds.select(cl=True)
        create_joint=cmds.joint()
        create_motion_path=cmds.pathAnimation(create_joint, c=path)
        cmds.setAttr('%s.uValue'%create_motion_path, 1.0/(joint_number-1)*i)
        motionpath_list.append(create_motion_path)
        joint_group.append(create_joint)
        cmds.select(cl=True)
        
   
    # duplicate each joints, put new joints in group and delete old joints
    new_joint_group=[]
    for i in joint_group:
        cmds.select(i)
        # list connection with each joints and delete
        selected = cmds.ls(sl=True)[0]
        disconnected = cmds.listConnections('%s.tx'%selected, plugs=True)[0]
        cmds.disconnectAttr(disconnected, '%s.tx'%selected)
        disconnected = cmds.listConnections('%s.ty'%selected, plugs=True)[0]
        cmds.disconnectAttr(disconnected, '%s.ty'%selected)
        disconnected = cmds.listConnections('%s.tz'%selected, plugs=True)[0]
        cmds.disconnectAttr(disconnected, '%s.tz'%selected)
        
        joint_dupicate = cmds.duplicate()
        new_joint_group.append(joint_dupicate)
        cmds.select(cl=True)
        cmds.delete(i)
        
    # reverse new joint list for parent joints    
    new_joint_group.reverse()
    
    # delete the old curve
    cmds.delete('post_curve')
    
    # parent joints
    for i in range(int(len(new_joint_group)-1)):
        cmds.parent(new_joint_group[i],new_joint_group[i+1])
        
    # edit x axis for each joint   
    first_joint=new_joint_group[-1]
    cmds.select(first_joint)  
    select_joint = cmds.ls(sl=True)    
    selected_joint_list = cmds.listRelatives(ad=True, f=True)
    selected_joint_list.reverse()
    selected_joint_list.insert(0, select_joint[0])
    cmds.select(selected_joint_list)
    
    select_joint_second_grp = cmds.ls(sl=True)
    for i in new_joint_group:
        cmds.joint(e=True, zso=True, oj='xyz', sao='yup')
        
# call functions
ui()