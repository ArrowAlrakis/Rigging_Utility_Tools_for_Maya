# ================================
# Script Name: RebuildJointChain_v01.py
# Author: Arrow Lyu
# Date: 2024/08/19
# Description:
#   - Creates a preview polyCube with user-defined size and subdivisions.
#   - Applies a height map (alpha texture) as a displacement on the cube.
#   - Allows easy deletion of the preview geometry.
# Usage:
#   - Make sure you have your texture files under "sourceimages/Alpha_Pack/".
#   - Select the object, input the file name and then cilck apply.
# ================================

import maya.cmds as cmds
import maya.mel as mel
import random

# create main window
def ui():
    # make sure there is no window exist before create a new one
    if cmds.window('Customized Surface', ex=True):
        cmds.deleteUI('Customized Surface')
    win = cmds.window('Customized Surface')
    # ui layout   
    cmds.columnLayout(adjustableColumn=True)
    cmds.frameLayout(label='1. Create Your PolyCube for Testing')

    # content
    # size
    cmds.text('Scale X', h=20)
    cmds.textField('scale_x_input', h=30)
    cmds.text('Scale Z', h=20)
    cmds.textField('scale_z_input', h=30)
    cmds.text('Scale Y', h=20)
    cmds.textField('scale_y_input', h=30)
    
    # subdivision
    cmds.text('Subdivision Width', h=20)
    cmds.textField('sub_width_input', h=30)
    cmds.text('Subdivision Height', h=20)
    cmds.textField('sub_height_input', h=30)
    cmds.text('Subdivision Depth', h=20)
    cmds.textField('sub_depth_input', h=30)
    cmds.button('Create Test Cube', c='create_shape()', h=40, bgc=[0.6,0.5,0.9])
    
    
    cmds.separator(height=10)

    # texture deformer
    cmds.frameLayout( label='2. File Name of Your Alapha Texture' )
    cmds.text('(example: moon.jpg)')
    cmds.textField('my_file_name_input', text=True, vis=True, h=30, sbm='File Name: Input file name of a texture')
    cmds.button('Apply Alpha', c='texture_deform()', h=40, bgc=[0.2,0.5,0.7])
    

    cmds.separator(height=10)

    # clear test
    cmds.frameLayout( label='3. Delete Test PolyCube' )
    cmds.button('Delete', c='clear()', h=40, bgc=[0.1,0.7,0.5])
    
    # create window "win"
    cmds.showWindow(win)




def create_shape():
    # create mesh
    my_name = 'land'
    cube = cmds.polyCube(sd=50, sh=4, sw=50, n=my_name)   
    # set size
    scale_x = int(cmds.textField('scale_x_input', q=True, text=True))
    scale_z = int(cmds.textField('scale_z_input', q=True, text=True))
    scale_y = int(cmds.textField('scale_y_input', q=True, text=True))
    cmds.setAttr('%s.scaleX' %my_name, scale_x)
    cmds.setAttr('%s.scaleZ' %my_name, scale_z)
    cmds.setAttr('%s.scaleY' %my_name, scale_y)   
    # set sub division
    sub_width = int(cmds.textField('sub_width_input', q=True, text=True))
    sub_height = int(cmds.textField('sub_height_input', q=True, text=True))
    sub_depth = int(cmds.textField('sub_depth_input', q=True, text=True))
    get_history = cmds.listHistory(cube)
    my_history = get_history[-1]
    my_subwidth = my_history + '.subdivisionsWidth'
    my_subheigth = my_history + '.subdivisionsHeight'
    my_subdepth = my_history + '.subdivisionsDepth'
    cmds.setAttr(my_subwidth, sub_width)
    cmds.setAttr(my_subheigth, sub_height)
    cmds.setAttr(my_subdepth, sub_depth)
    

def clear():
    # delete test object
    cmds.delete('land')
           
def texture_deform():
    # user input
    my_file_name = cmds.textField('my_file_name_input', q=True, text=True)
    # create texture deformer
    my_deformer = cmds.textureDeformer(envelope=1, strength=1, offset=0, vectorStrength=(1, 1, 1), vectorOffset=(0, 0, 0), vectorSpace="Object" ,direction="Handle", pointSpace="UV", exclusive="")
    # create new shader node
    my_shader = 'ha_shader'
    shader=cmds.shadingNode('lambert',asShader=True, n=my_shader)
    # create file node
    fileNode = cmds.shadingNode('file', asTexture=True, isColorManaged=True)
    # create shading node
    fileNode2d = cmds.shadingNode('place2dTexture', asUtility=True)
    # apply texture
    my_file_adress = ('sourceimages/alpha_pack/' + my_file_name)
    shading_group = cmds.sets(renderable=True,noSurfaceShader=True,empty=True)
    cmds.setAttr( '%s.fileTextureName'%fileNode, my_file_adress, type = 'string')
    # link file node to texture deformer
    cmds.connectAttr(fileNode + '.outColor', 'textureDeformer1' + '.texture', f=True)

ui()