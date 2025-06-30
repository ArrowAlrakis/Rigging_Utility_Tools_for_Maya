# ================================
# Script Name: DoControl_v01.py
# Author: Arrow Lyu
# Date: 2025/06/26
# Description:
#   - Automatically creates controls for a joint chain.
#   - Skips the last (end) joint from control creation.
#   - Controls are constrained to joints and organized hierarchically.
# Usage:
#   - Select the root joint and run.
# ================================


import maya.cmds as cmds

# Create the main function of the controller chain: create controls for selected joint chain
def create_controls_from_joint_chain(radius=3.0, axis='Y', name_prefix='ctrl'):
    
    if not cmds.ls(sl=True, type='joint'):
        cmds.warning("Please select the root joint.")
        return

    # Define axis direction for circle
    axis_dict = {'X': (1, 0, 0), 'Y': (0, 1, 0), 'Z': (0, 0, 1)}
    if axis not in axis_dict:
        cmds.warning("Invalid axis. Use 'X', 'Y', or 'Z'.")
        return
    orient = axis_dict[axis]

    # Get full joint chain
    root_joint = cmds.ls(sl=True, l=True)[0]
    all_joints = cmds.listRelatives(root_joint, ad=True, type='joint', f=True) or []
    all_joints.append(root_joint)
    all_joints.reverse()

    if len(all_joints) < 2:
        cmds.warning("Joint chain too short to skip end joint.")
        return

    joints_to_rig = all_joints[:-1]  # skip end joint
    ctrl_list = []

    for joint in joints_to_rig:
        pos = cmds.xform(joint, q=True, ws=True, t=True)
        short_name = joint.split('|')[-1]
        ctrl_name = f"{name_prefix}_{short_name}_CTRL"
        grp_name = f"{ctrl_name}_GRP"

        ctrl = cmds.circle(n=ctrl_name, nr=orient, r=radius)[0]
        grp = cmds.group(ctrl, n=grp_name)
        cmds.xform(grp, ws=True, t=pos)
        cmds.makeIdentity(ctrl, apply=True, t=1, r=1, s=1, n=0)
        cmds.parentConstraint(ctrl, joint, mo=True)

        ctrl_list.append((ctrl, grp))

    for i in range(len(ctrl_list) - 1):
        cmds.parent(ctrl_list[i + 1][1], ctrl_list[i][0])

    cmds.select(clear=True)
    print("✅ FK controls created. End joint skipped.")


# Get value from UI and execute function when button is clicked
def on_create_button(*args):
    try:
        radius = float(cmds.textField('radiusField', q=True, text=True))
        axis = cmds.textField('axisField', q=True, text=True).upper()
        name_prefix = cmds.textField('prefixField', q=True, text=True)

        if axis not in ['X', 'Y', 'Z']:
            cmds.warning("Axis must be X, Y or Z.")
            return
        if not name_prefix:
            name_prefix = "ctrl"

        create_controls_from_joint_chain(radius=radius, axis=axis, name_prefix=name_prefix)

    except ValueError:
        cmds.warning("Invalid radius. Please enter a number.")

# create ui window
def ui():
    if cmds.window('ControlToolWin', exists=True):
        cmds.deleteUI('ControlToolWin')

    win = cmds.window('ControlToolWin', title='FK Control Tool', widthHeight=(300, 250))
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label='How to use:')
    cmds.separator(h=5, style='in')
    cmds.text(label='1. Select the root joint')
    cmds.text(label='2. Adjust the settings below')
    cmds.text(label='3. Click to generate FK controls')
    cmds.separator(h=10, style='in')

    cmds.text(label='Control Radius:')
    cmds.textField('radiusField', h=30, text='3.0')

    cmds.text(label='Control Axis (X/Y/Z):')
    cmds.textField('axisField', h=30, text='Y')

    cmds.text(label='Name Prefix:')
    cmds.textField('prefixField', h=30, text='ctrl')

    cmds.separator(h=10)
    cmds.button(label='Create FK Control Chain', h=40, bgc=[0.1, 0.7, 0.9], c=on_create_button)

    cmds.showWindow(win)

# run UI
ui()
