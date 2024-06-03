import os, bpy, bmesh
from os.path import dirname

ADDON_DIR = dirname(dirname(dirname(os.path.realpath(__file__)))) + "\\BlenderPCModelImporter"
print(ADDON_DIR)
ADDON_NAME = os.path.basename(ADDON_DIR)
FILEPATH = ""


class UserException(Exception):

    message: str

    def __init__(self, message: str, *args: object):
        self.message = message
        super().__init__(message, *args)

def get_path():
    return ADDON_DIR

try:
    import pythonnet
except ModuleNotFoundError as exc:
    raise UserException(("Could not install python.net, please try running blender with"
            " admin rights")) from exc

path = os.path.join(get_path(), "libs")
dll_names = [
    "PointCloudBlender.dll"
]

pythonnet.load("coreclr")

import clr
for dll_name in dll_names:
    dll_path = os.path.join(path, dll_name)
    clr.AddReference(dll_path)

from PointCloudBlender import PointCloudReader
from PointCloudBlender import ModelReader

def importPointCloud(importer):
    pc = PointCloudReader.LoadPointCloud(importer.filepath)
    collection = bpy.data.collections.new(os.path.basename(importer.filepath))
    bpy.context.scene.collection.children.link(collection)
    for i in pc:
        if os.path.exists(dirname(importer.filepath) + "\\" + i.ModelName + ".terrain-model"):
            model = ModelReader.Model(dirname(importer.filepath) + "\\" + i.ModelName + ".terrain-model", bpy.context.scene.HedgeNeedle)
            for Mesh in model.meshes:
                mesh1 = bpy.data.meshes.new(i.ModelName + " Mesh")
                mesh1.use_auto_smooth = True
                ob = bpy.data.objects.new(i.InstanceName, mesh1)
                ob.location = (-i.Position.X, i.Position.Z, i.Position.Y)
                ob.rotation_euler = (i.Rotation.X, i.Rotation.Z, i.Rotation.Y)
                collection.objects.link(ob)
                bpy.context.view_layer.objects.active = ob
                ob.select_set(True)
                mesh = bpy.context.object.data
                bm = bmesh.new()
                for v in Mesh.verts:
                    bm.verts.new((-v.X, v.Z, v.Y))
                list = [v for v in bm.verts]
                for f in Mesh.faces:
                    try:
                        bm.faces.new((list[f.x], list[f.y], list[f.z]))
                    except:
                        continue
                bm.to_mesh(mesh)
                bm.free()