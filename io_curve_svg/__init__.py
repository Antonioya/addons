# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "Scalable Vector Graphics (SVG) 1.1 format",
    "author": "JM Soler, Sergey Sharybin, Antonio Vazquez",
    "blender": (2, 80, 0),
    "location": "File > Import > Scalable Vector Graphics (.svg)",
    "description": "Import SVG as curves",
    "warning": "",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/import_export/curve_svg.html",
    "support": 'OFFICIAL',
    "category": "Import-Export",
}


# To support reload properly, try to access a package var,
# if it's there, reload everything
if "bpy" in locals():
    import importlib
    if "import_svg" in locals():
        importlib.reload(import_svg)


import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       FloatProperty,
                       EnumProperty)
from bpy_extras.io_utils import ImportHelper


class ImportSVG(bpy.types.Operator, ImportHelper):
    """Load a SVG file"""
    bl_idname = "import_curve.svg"
    bl_label = "Import SVG"
    bl_options = {'UNDO'}

    filename_ext = ".svg"
    filter_glob: StringProperty(default="*.svg", options={'HIDDEN'})

    target: EnumProperty(items=(('GPENCIL', "Grease Pencil Strokes", "Import as Grease Pencil Strokes"),
                                     ('CURVE', "Curves", "Import as Curves")),
                                     name="Target",
                                     description="Target type")

    use_collections: BoolProperty(
        name="Layers as Collections",
        description="Seaparate SVG layers as collections",
        default=True,
    )

    use_rotation: BoolProperty(
        name="Default Orientation",
        description="Rotate strokes to default grease pencil orientation",
        default=True,
    )

    scale: FloatProperty(
        name='Scale Object', min=0.5, max=50, default=3.0,
        precision=2,
        description='Scale original file',
    )

    sample: FloatProperty(
        name='Sample', min=0.0, max=50, default=0.0001,
        precision=3,
        description='Sample Stroke distance, zero to disable',
    )

    scale_thickness: FloatProperty(
        name='Scale Thickness', min=0.001, max=100, default=0.30,
        precision=2,
        description='Scale thickness of points',
    )

    def execute(self, context):
        from . import import_svg

        return import_svg.load(self, context, filepath=self.filepath)

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "target")

        if self.target == 'GPENCIL':
            row = layout.row(align=True)
            row.prop(self, "use_collections")
            row = layout.row(align=True)
            row.prop(self, "use_rotation")

            row = layout.row(align=True)
            row.prop(self, "scale")
            row = layout.row(align=True)
            row.prop(self, "scale_thickness")
            row = layout.row(align=True)
            row.prop(self, "sample")


def menu_func_import(self, context):
    self.layout.operator(ImportSVG.bl_idname,
        text="Scalable Vector Graphics (.svg)")


def register():
    bpy.utils.register_class(ImportSVG)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportSVG)

    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

# NOTES
# - blender version is hardcoded

if __name__ == "__main__":
    register()
