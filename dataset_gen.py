import bpy
import math
import os
import random
import mathutils


# Set up scene
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.image_settings.file_format = 'PNG'

# Set render resolution
scene.render.resolution_x = 400
scene.render.resolution_y = 600

# Set up camera
camera = bpy.data.objects['Camera']
camera.location = (0, 0, 3)
camera.rotation_euler = (math.radians(0), 0, 0)

# Set up lighting
light_data = bpy.data.lights.new(name="light", type='AREA')
light_obj = bpy.data.objects.new(name="light_object", object_data=light_data)
light_obj.location = (0, 0, 10)
light_obj.rotation_euler = (math.radians(0), 0, 0)  # Adjust the rotation for better lighting angle
scene.collection.objects.link(light_obj)

# Adjust light settings
light_data.energy = 5  # Increase the energy for brighter lighting

# Set up ground
bpy.ops.mesh.primitive_plane_add(size=10, enter_editmode=False, location=(0, 0, 0))
ground = bpy.context.object

# Set up ground material for better visibility
ground_material = bpy.data.materials.new(name="GroundMaterial")
ground.data.materials.append(ground_material)

ground_material.use_nodes = True
nodes = ground_material.node_tree.nodes
nodes.clear()

# Add emission node to make the ground emit light
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs[0].default_value = (1, 1, 1, 1)  # White emission color
emission_node.inputs[1].default_value = 2  # Adjust the strength of emission

# Add "Material Output" node if not present
if 'Material Output' not in nodes:
    material_output_node = nodes.new(type='ShaderNodeOutputMaterial')
else:
    material_output_node = nodes['Material Output']

ground_material.node_tree.links.new(material_output_node.inputs['Surface'], emission_node.outputs['Emission'])

# Adjust other material settings
ground_material.diffuse_color = (0.8, 0.8, 0.8, 1.0)  # Light gray

# Update the viewport to reflect the material changes
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.tag_redraw()
# Set up ground
bpy.ops.mesh.primitive_plane_add(size=10, enter_editmode=False, location=(0, 0, 0))
ground = bpy.context.object


# Set up crate
bpy.ops.mesh.primitive_cube_add(size=2.2, enter_editmode=False, location=(0, 0, -0.22))
crate = bpy.context.object
crate.scale = (0.4, 0.6, 0.22)

# Set up physics
bpy.ops.rigidbody.object_add()
crate.rigid_body.type = 'PASSIVE'

# Load desired object
bpy.ops.import_mesh.ply(filepath="C:/Users/dikgoz321/Desktop/CAD file/obj_01.ply")
obj = bpy.context.selected_objects[0]

# Set up physics for the object
bpy.ops.rigidbody.object_add()
obj.rigid_body.type = 'ACTIVE'
obj.rigid_body.enabled = True


# Scale the object to desired dimensions
desired_dimensions = (0.1, 0.1, 0.01)
current_dimensions = obj.dimensions
scale_factors = [desired_dim / current_dim for desired_dim, current_dim in zip(desired_dimensions, current_dimensions)]
obj.scale = scale_factors

# Assign different materials to ground, crate, and object
ground_material = bpy.data.materials.new(name="GroundMaterial")
ground_material.diffuse_color = (0.8, 0.8, 0.8, 1.0)  # Light gray
ground.data.materials.append(ground_material)

crate_material = bpy.data.materials.new(name="CrateMaterial")
crate_material.diffuse_color = (0.2, 0.2, 0.8, 1.0)  # Blue
crate.data.materials.append(crate_material)

obj_material = bpy.data.materials.new(name="ObjectMaterial")
obj_material.diffuse_color = (0.8, 0.2, 0.2, 1.0)  # Red
obj.data.materials.append(obj_material)

# Number of objects to render
num_objects = 10

# Output folder path
output_folder = "C:/Users/dikgoz321/Desktop/output"  # Replace with the desired output folder path

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Output file path for annotations
output_file = os.path.join(output_folder, "annotations.txt")


# Enable physics simulation for the object
obj.rigid_body.type = 'ACTIVE'
obj.rigid_body.enabled = True
obj.rigid_body.collision_shape = 'MESH'

# Add rigid body constraint between the object and the crate
constraint = obj.constraints.new(type='CHILD_OF')
constraint.target = crate
constraint.influence = 1.0

# Disable gravity for the object
obj.rigid_body.type = 'PASSIVE'

# Open the output file for writing annotations
with open(output_file, 'w') as f:
    # Render loop
    for i in range(num_objects):
        # Randomize object position within the crate
        obj.location.x = crate.location.x + random.uniform(-crate.dimensions.x / 2, crate.dimensions.x / 2)
        obj.location.y = crate.location.y + random.uniform(-crate.dimensions.y / 2, crate.dimensions.y / 2)
        obj.location.z = crate.location.z + obj.dimensions.z / 2

        # Randomize object rotation
        obj.rotation_euler = (random.uniform(0, 2 * math.pi),
                              random.uniform(0, 2 * math.pi),
                              random.uniform(0, 2 * math.pi))

        # Set the current frame for physics simulation
        scene.frame_set(i + 1)

        # Render image
        output_path = os.path.join(output_folder, f"output_{i + 1}.png")
        scene.render.filepath = output_path

        # Enable physics simulation
        obj.rigid_body.enabled = True

        # Simulate the physics until the object comes to rest
        while obj.rigid_body.kinematic is False:
            bpy.context.scene.frame_set(scene.frame_current + 1)
            bpy.context.scene.frame_set(scene.frame_current - 1)

        # Disable physics simulation
        obj.rigid_body.enabled = False

        # Render the final image after the object has landed
        bpy.ops.render.render(write_still=True)

        # Write annotation to file
        cam_R_m2c = [round(r, 8) for r in camera.rotation_euler]
        cam_t_m2c = [round(c, 8) for c in camera.location]
        obj_boundingbox = [round(v, 0) for v in obj.dimensions]
        obj_id = obj.name
        annotation = f"{i + 1}: \n- cam_R_m2c: {cam_R_m2c}\n  cam_t_m2c: {cam_t_m2c}\n  obj_boundingbox: {obj_boundingbox}\n  obj_id: {obj_id}\n"
        f.write(annotation)

# Cleanup
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.ops.object.delete()
bpy.ops.object.select_all(action='DESELECT')
crate.select_set(True)
bpy.ops.object.delete()