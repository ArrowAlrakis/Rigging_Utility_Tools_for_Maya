# Rigging Utility Tools for Maya

A collection of lightweight Python-based rigging utilities created to assist rigging workflows in Autodesk Maya.

Created by Arrow Lyu.

---

# Overview

This toolset was designed as a set of personal helpers to speed up rigging-related tasks in Maya. It includes custom UI tools, snapping, axis control, and rig part labeling helpers.

Although originally used as internal support during other Auto Rig development, the tools can be used independently.

---

# Scripts

- `PYT_JLY_codeUtilities_v004.py`: Contains the actual utility functions and UI modules
- `PYT_JLY_importUtilities_v001.py`: Entry script to import and launch tool UIs (calls functions from the utility script)

---

# Included Tools

- **LabelUI** – Assign custom name labels to selected objects.
- **PoleUI** – Generate pole vector helpers for IK chains.
- **BallUI** – Simple ball joint creation (experimental).
- **AxisUI** – Modify rotation axes quickly.
- **PPathUI / Many1UI / LockUI** – Various helpers for object parenting, locking transforms, and organizing hierarchy.
- **lyu_ObjSnap** – Snap objects quickly via script.

> Note: Some tools are experimental or made for personal use and may not be fully generalized.

---

# Demo Video

▶ [Watch full utility tool demo](<>)

---

# How to Use

1. Open Maya and load the two `.py` files into your script path or source them manually.
2. Run `PYT_JLY_importUtilities_v001.py` in Maya Script Editor.
3. The main UI (`LabelUI`) will launch.
4. Uncomment other functions in the import script to use their corresponding UIs.

---

# About the Author
This tool was developed by Arrow Lyu, a game art designer with experience in rigging and scripting, aiming to bridge art and technical workflows. It reflects an interest in character TD work and tech art pipelines for games and animation.

# Contact / Portfolio
Email: jcrane@gmail.com
GitHub: [[Arrow's profile]](https://github.com/ArrowAlrakis)
