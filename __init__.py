bl_info = {
    "name" : "PointCloud Importer",
    "author" : "Ashrindy; Turk645 and Knuxfan24 - file format research",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 2),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator

from . import importPointCloud

class PointCloudPanel(bpy.types.Panel):
    bl_label = ".pcmodel Importer"
    bl_category = "PointCloud (.pcmodel) importer"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bpy.types.Scene.HedgeNeedle = StringProperty(name="HedgeNeedle", subtype='FILE_PATH', description="Sometimes models have LODs, for which HedgeNeedle is needed", default="")

    def draw(self, context):
        row = self.layout.row()
        row.operator("import.pcmodel", text="Import .pcmodel")

        row = self.layout.row()
        row.prop(context.scene, "HedgeNeedle", text="HedgeNeedle file path")
        

class ImportPointCloud(Operator, ImportHelper):
    bl_idname = "import.pcmodel"
    bl_label = "Import PCModel"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    filename_ext = ".pcmodel"
    filter_glob: StringProperty(default="*.pcmodel", options={"HIDDEN"})
    filepath: StringProperty(subtype='FILE_PATH')
    ImportUvs: BoolProperty(name="Import UVs", description="If not needed, it is recommended to turn this off, because it does slow the import process.", default=True)
    ImportShadowModels: BoolProperty(name="Import Shadow Models", description="If not needed, it is recommended to turn this off, because it does slow the import process.", default=True)

    def execute(self, context):
        print(bpy.context.scene.HedgeNeedle)
        if bpy.context.scene.HedgeNeedle == "":
            def hedgeneedleError(self, context):
                self.layout.label(text="You need to set the HedgeNeedle directory otherwise it won't work 90% of the time!")
            bpy.context.window_manager.popup_menu(hedgeneedleError, title = "Error")
            return {'FINISHED'}
        else:
            importPointCloud.importPointCloud(self)
        return {"FINISHED"}

def menu_func_import(self, context):
    self.layout.operator(ImportPointCloud.bl_idname, text="PointCloud (.pcmodel)")

def register():
    bpy.utils.register_class(PointCloudPanel)
    bpy.utils.register_class(ImportPointCloud)

def unregister():
    ...

if __name__ == "__main__":
    register()
