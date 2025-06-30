# ================================
# Script Name: SeedPlanter_v02.py
# Author: Arrow Lyu
# Date: 2025/05/24
# Description:
#   - Allows user to plant selected objects (seeds) onto a ground mesh.
#   - Seeds are randomly scattered across surface points.
#   - Rearrangement can be applied after planting to randomize again.
# Usage:
#   - Select ground object first. Then select seed object.
#   - Use UI to generate result.
# ================================


import maya.cmds as cmds
import random

class CreateBuildingsUI:
    def __init__(self):
        # create empty node for grouping and delete constrain later
        self.ground = None
        self.seed_objects = []
        self.instances = []
        self.seed_group = "seed_group"
        
        cmds.createNode('transform', n='const_group')
        
        # if seed_group exist, delete it
        if cmds.objExists(self.seed_group):
            cmds.delete(self.seed_group)
        cmds.group(em=True, name=self.seed_group)
        
        # if window exist, delete it
        if cmds.window('BuildingToolUI', exists=True):
            cmds.deleteUI('BuildingToolUI')
        
        # create ui window
        self.win = cmds.window('BuildingToolUI', title='Building Scatter Tool', sizeable=False)
        cmds.columnLayout(adj=True, rs=5, columnAlign='center')

        cmds.separator(h=8)
        cmds.text(label='1. Select your ground object (surface)')
        cmds.button(label='Set Selected as Ground', c=self.set_ground)

        self.ground_label = cmds.text(label='Ground: None', align='left')

        cmds.separator(h=8)
        cmds.text(label='2. Select object(s) to plant')
        cmds.button(label='Set Selected as Seeds', c=self.set_seeds)
        self.seed_label = cmds.text(label='Seeds: None', align='left')

        cmds.separator(h=8)
        self.num_field = cmds.intFieldGrp(label='Instances:', value1=20)

        cmds.button(label='Create Instances', bgc=(0.4, 0.8, 0.6), h=30, c=self.create_instances)
        
        self.x_scale_slider = cmds.floatSliderGrp(label='X Scale', field=True, min=0.1, max=5.0, value=1.0)
        self.y_scale_slider = cmds.floatSliderGrp(label='Y Scale', field=True, min=0.1, max=5.0, value=1.0)
        self.z_scale_slider = cmds.floatSliderGrp(label='Z Scale', field=True, min=0.1, max=5.0, value=1.0)
        cmds.button(label='Apply Scaling', c=self.scale)

        self.rot_fields = cmds.floatFieldGrp(label='Rotate XYZ', numberOfFields=3, value1=0, value2=0, value3=0)
        cmds.button(label='Apply Rotation', c=self.rotate)

        cmds.button(label='Random Collapse', bgc=(1, 0.6, 0.3), c=self.collapse)

        cmds.separator(h=8)
        cmds.button(label='Clear Instances', bgc=(1, 0.3, 0.3), c=self.clear)

        cmds.showWindow(self.win)
    
    ### define surface
    def set_ground(self, *_):
        sel = cmds.ls(sl=True)
        if sel:
            self.ground = sel[0]
            cmds.text(self.ground_label, e=True, label=f'Ground: {self.ground}')
        else:
            cmds.warning("Please select a ground object.")
    ### define seed
    def set_seeds(self, *_):
        sel = cmds.ls(sl=True)
        if sel:
            self.seed_objects = sel
            cmds.text(self.seed_label, e=True, label=f'Seeds: {", ".join(self.seed_objects)}')
        else:
            cmds.warning("Please select at least one seed object.")
    ### random plant seeds onto the surface
    def create_instances(self, *_):
        count = cmds.intFieldGrp(self.num_field, q=True, value1=True)
        if not self.ground:
            cmds.warning("No ground object set.")
            return

        # Clear previous
        self.clear()

        # Get size of ground
        bound = cmds.exactWorldBoundingBox(self.ground)
        min_x, min_y, min_z, max_x, max_y, max_z = bound
        range_x = max_x - min_x
        range_z = max_z - min_z
        range_y = max_y - min_y
        
        for i in range(count):
            if self.seed_objects:
                src = random.choice(self.seed_objects)
                inst = cmds.instance(src, name=f'inst_{i}')[0]
            else:
                inst = cmds.polyCube(name=f'building_{i}', w=1, h=2, d=1)[0]

            x = random.uniform(min_x, max_x)
            z = random.uniform(min_z, max_z)
            cmds.move(x, 0, z, inst)
            cmds.parent(inst, self.seed_group)
            self.instances.append(inst)

            if self.ground:
                const = cmds.geometryConstraint(self.ground, inst, w=1)
                cmds.delete(const)  # only snap once
    ### scale all seeds
    def scale(self, *_):
        x_scale_value = cmds.floatSliderGrp(self.x_scale_slider, q=True, value=True)
        y_scale_value = cmds.floatSliderGrp(self.y_scale_slider, q=True, value=True)
        z_scale_value = cmds.floatSliderGrp(self.z_scale_slider, q=True, value=True)
        for inst in self.instances:
            cmds.scale(x_scale_value, y_scale_value, z_scale_value, inst)
    ### random rotate
    def rotate(self, *_):
        x, y, z = cmds.floatFieldGrp(self.rot_fields, q=True, value=True)
        for inst in self.instances:
            cmds.rotate(x, y, z, inst)
    ### random collapse
    def collapse(self, *_):
        for inst in self.instances:
            rx = random.uniform(-180, 180)
            ry = random.uniform(-180, 180)
            rz = random.uniform(-180, 180)
            cmds.rotate(rx, ry, rz, inst)
            
    ### delete constrains, use after all are done
    def clear(self, *_):
        for inst in self.instances:
            if cmds.objExists(inst):
                cmds.delete(inst)
        self.instances = []

CreateBuildingsUI()