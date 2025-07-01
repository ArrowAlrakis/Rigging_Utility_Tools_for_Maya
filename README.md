# Rigging Utility Tools for Maya
[Shelf Preview](./Preview.png)

A curated shelf of 13 productivity-enhancing Maya Python tools.
Created by Arrow Lyu, this set includes tools for rigging, modeling, scene interaction, and utility support.


# Main Shelf Script
📄 [shelf_Pyt_Tools_v01.mel](./shelf_Pyt_Tools_v01.mel) – Main shelf


# Python Scripts

📄 [Python_Tools_Utilities_v01.py](./Scripts/Python_Tools_Utilities_v01.py) – Contains the functions for the first 8 buttons on the shelf, including modules: 
1. Object Snap.
2. Show/Hide Local Axis.
3. Add current project path to Maya python path.
4. Combine many object shapes into one.
5. Lock/Unlock Attributes UI.
6. Create Ball control UI.
7. Create Pole control UI.
8. Create Label UI.

📄 [RebuildJointChain_v01.py](./Scripts/RebuildJointChain_v01.py) – Rebuild the existing joint chain with the desired joint count using motion paths.

📄 [DoControl_v01.py](./Scripts/DoControl_v01.py) – Generates custom control curves and assigns them to the selected joint chain.

📄 [SeedPlanter_v02.py](./Scripts/SeedPlanter_v02.py) – Scatters selected objects randomly on a selected surface, including scale, rotation, and clear feature.

📄 [HeightPreview_v01.py](./Scripts/HeightPreview_v01.py) – Creates a preview box to fast visualize height maps in the viewport.

📄 [ThreeDesign_v01.py](./Scripts/ThreeDesign_v01.py) – Generates 3 types of 3D patterns with layered primitive geometry.

# Overview

This shelf contains 13 buttons covering: Control creation and assignment; Randomized object scattering (Seed Planter); Joint rebuilding from hierarchy; Fast Height texture visual feedback; Quick concept generation; Utility functions for selection, naming, grouping, snapping, pivot control, attribute control, etc.

Most tools are accessible through simple Maya UI popups or one-click shelf actions. Scripts are written in Python using maya.cmds and tested in Maya 2020–2025.


# Demo Video

▶ [Watch full utility tool demo](<>)

---

# How to Use
Option 1
1. Open Maya
2. Drag and drop or execute `shelf_Pyt_Tools_v01.mel` in the Script Editor
3. This will install the custom shelf Pyt_Tools with 13 buttons, all connected to the Python scripts.
4. Click any button to run its associated tool.


Option 2
1. Open Maya
2. Load any `.py` script from this repo into the Script Editor (Python tab)
3. Execute it to run the tool or open its UI
4. Some scripts (`Python_Tools_Utilities_v01.py`) contain multiple utility functions. You may need to run specific function calls manually, for example:

    import Python_Tools_Utilities_v01 as utils
   
    utils.rename_objects()



# About the Author
This tool was developed by Arrow Lyu, a game art designer with experience in rigging and scripting, aiming to bridge art and technical workflows. It reflects an interest in character TD work and tech art pipelines for games and animation.

# Contact / Portfolio
Email: jcrane@gmail.com
GitHub: [[Arrow's profile]](https://github.com/ArrowAlrakis)
