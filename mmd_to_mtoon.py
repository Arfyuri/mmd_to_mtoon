bl_info = {
    "name": "MMD to MToon Connector",
    "author": "Arfyuri",
    "version": (1, 31),
    "blender": (3, 6, 0),
    "location": "3D Viewport > Sidebar > Arfyuri Tools",
    "description": "Converts MMD materials to MToon with proper texture connections",
    "category": "Material",
}

# pyrefly: ignore [missing-import]
import bpy

# Mapping from MMDShaderDev inputs to MToon_unversioned inputs
# Adjust these according to the input names in your MMDShaderDev node
MMD_INPUT_TO_MTOON = {
    "Base Tex": [  # Main texture input in MMDShaderDev
        ("MainTexture", "Color"),
        ("ShadeColor", "Color"),
        ("MainTextureAlpha", "Alpha")
    ],
    "Toon Tex": [  # Toon texture input
        ("ShadeTexture", "Color"),
        ("ReceiveShadow_Texture_alpha", "Alpha")
    ],
    "Sphere Tex": [  # Sphere texture input
        ("SphereAddTexture", "Color")
    ]
}

# Default values for MToon parameters
MTOON_DEFAULT_VALUES = {
    "ShadeShift": 1.0,
    "ShadeToony": 1.0
}

class MMDToMToonOperator(bpy.types.Operator):
    bl_idname = "object.mmd_to_mtoon_fixed"
    bl_label = "MMD to MToon (Fixed)"

    def execute(self, context):
        # Check the existence of the MToon_unversioned node group
        mtoon_group = bpy.data.node_groups.get("MToon_unversioned")
        if not mtoon_group:
            self.report({"ERROR"}, "MToon_unversioned node group not found! Install the VRM add-on.")
            return {'CANCELLED'}

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            for mat_slot in obj.material_slots:
                material = mat_slot.material
                if not material or not material.use_nodes:
                    print(f"⚠️ {material.name if material else '(empty slot)'}: No nodes in material.")
                    continue

                nodes = material.node_tree.nodes
                links = material.node_tree.links

                # Find MMDShaderDev node
                mmd_node = next((n for n in nodes if n.type == 'GROUP' and n.node_tree and "MMDShaderDev" in n.node_tree.name), None)
                if not mmd_node:
                    print(f"❌ {material.name}: MMDShaderDev node not found!")
                    continue

                # Create MToon node
                mtoon_node = nodes.new('ShaderNodeGroup')
                mtoon_node.node_tree = mtoon_group
                mtoon_node.location = mmd_node.location

                # Connect texture nodes from MMD inputs to MToon inputs
                for mmd_input_name, mtoon_connections in MMD_INPUT_TO_MTOON.items():
                    if mmd_input_name in mmd_node.inputs and mmd_node.inputs[mmd_input_name].is_linked:
                        texture_node = mmd_node.inputs[mmd_input_name].links[0].from_node
                        if texture_node.type == 'TEX_IMAGE':
                            for mtoon_input, output_type in mtoon_connections:
                                if output_type in texture_node.outputs and mtoon_input in mtoon_node.inputs:
                                    links.new(texture_node.outputs[output_type], mtoon_node.inputs[mtoon_input])
                                    print(f"✅ {material.name}: {texture_node.name} ({output_type}) -> {mtoon_input} connected")
                                else:
                                    print(f"❌ {material.name}: {texture_node.name} -> {mtoon_input} could not be connected (missing output or input)")
                        else:
                            print(f"⚠️ {material.name}: Node connected to input '{mmd_input_name}' is not an image texture!")
                    else:
                        print(f"⚠️ {material.name}: MMD input '{mmd_input_name}' not found or not connected!")

                # Assign default values to MToon parameters
                for param, value in MTOON_DEFAULT_VALUES.items():
                    if param in mtoon_node.inputs:
                        mtoon_node.inputs[param].default_value = value
                        print(f"⚙️ {material.name}: {param} -> set to {value}")

                # Connect MToon node to material output
                output_node = next((n for n in nodes if n.type == 'OUTPUT_MATERIAL'), None)
                if output_node and mtoon_node.outputs:
                    links.new(mtoon_node.outputs[0], output_node.inputs['Surface'])
                    print(f"🔌 {material.name}: MToon connected to material output")

                # Remove MMDShaderDev node
                nodes.remove(mmd_node)
                print(f"♻️ {material.name}: MMDShaderDev node removed")

                print(f"✅ {material.name}: Conversion complete!")

        return {'FINISHED'}

class MMDToMToonPanel(bpy.types.Panel):
    bl_label = "MMD to MToon"
    bl_idname = "VIEW3D_PT_mmd_to_mtoon_fixed"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Arfyuri Tools'

    def draw(self, context):
        self.layout.operator("object.mmd_to_mtoon_fixed", text="Convert to MToon")

class MMDToMToon_PT_credits(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Arfyuri Tools'
    bl_label = "Credits"
    bl_parent_id = "VIEW3D_PT_mmd_to_mtoon_fixed"
    bl_options = {'HIDE_HEADER'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.separator()
        col = layout.column()
        col.scale_y = 0.7
        col.label(text="Built by Arfyuri")

        row = layout.row()
        row.scale_y = 1.3
        row.operator(MMDToMToon_OT_open_support.bl_idname, text="Support Me", icon='FUND')

class MMDToMToon_OT_open_support(bpy.types.Operator):
    """Open the support page in your web browser"""
    bl_idname = "mmd_to_mtoon.open_support"
    bl_label = "Support Me"
    
    def execute(self, context):
        bpy.ops.wm.url_open(url="https://arfyuri.carrd.co")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MMDToMToonOperator)
    bpy.utils.register_class(MMDToMToonPanel)
    bpy.utils.register_class(MMDToMToon_OT_open_support)
    bpy.utils.register_class(MMDToMToon_PT_credits)

def unregister():
    # Child panel must be unregistered before its parent
    bpy.utils.unregister_class(MMDToMToon_PT_credits)
    bpy.utils.unregister_class(MMDToMToon_OT_open_support)
    bpy.utils.unregister_class(MMDToMToonPanel)
    bpy.utils.unregister_class(MMDToMToonOperator)

if __name__ == "__main__":
    register()