import bpy
import bpy_extras.io_utils

def diff_vals_update(self, context):
    normalized = self.diff_vals[0] / 65504
    bpy.data.materials["FFXIV_Base.001"].node_tree.nodes["GlossRamp"].color_ramp.elements[0].color = (normalized, normalized, normalized, 1)

bpy.types.Material.diff_vals = bpy.props.FloatVectorProperty(update=diff_vals_update, max=65504, min=-65504, step=2000)
bpy.types.Material.is_colorset = bpy.props.BoolProperty()

bpy.data.materials["FFXIV_Base.001"].diff_vals[0] = 0.0
bpy.data.materials["FFXIV_Base.001"].is_colorset = False

class Colorset:
    def __init__(self):
        self.Diffuse = bpy.data.materials["FFXIV_Base.001"].node_tree.nodes["DiffRamp"].color_ramp.elements[0]
        self.Gloss = 0.1
        bpy.data.materials["FFXIV_Base.001"].node_tree.nodes["GlossRamp"].color_ramp.elements[0].color = (self.Gloss, self.Gloss, self.Gloss, 1)
        
cube = Colorset()

class ImportOperator(bpy.types.Operator):
    """Load a colorset dds to the current material"""
    bl_idname = "export.colorset"
    bl_label = "Import Colorset"
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        colorset = open(self.filepath, 'rb')
        print(self.filepath)
        print("opened colorset: ")
        print(colorset.read())
        colorset.close()
        return {'FINISHED'}
        
    def invoke(self, context, event):
        bpy.context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ColorsetPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Colorset"
    bl_idname = "MATERIAL_PT_colorset"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.prop(bpy.data.materials["FFXIV_Base.001"], 'is_colorset')
        if(bpy.data.materials["FFXIV_Base.001"].is_colorset is True):
            row = layout.row()
            row.prop(cube.Diffuse, "color")
            row.enabled = False
            row = layout.row()
            row.prop(bpy.data.materials["FFXIV_Base.001"], 'diff_vals', index=1)
        
def register():
    bpy.utils.register_class(ColorsetPanel)
    bpy.utils.register_class(ImportOperator)

def unregister():
    bpy.utils.unregister_class(ColorsetPanel)
    bpy.utils.unregister_class(ImportOperator)

if __name__ == "__main__":
    register()