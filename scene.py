import time
import os
from math import pi
try:
    import bpy
except ModuleNotFoundError:
    print("Not in Blender. Exiting...")
    exit()
    
selfPath = os.path.dirname(os.path.abspath(__file__))
parentPath = os.path.dirname(selfPath)
    
#clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
    
#create a plane
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0.25))
bpy.ops.object.shade_smooth()
plane = bpy.context.active_object

#subdivide the plane
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=50)

#apply another subdivision but with modifier and set the options
subdivisionModifier = plane.modifiers.new(name="subdivision", type='SUBSURF')
subdivisionModifier.subdivision_type = 'SIMPLE'
subdivisionModifier.levels = 3
subdivisionModifier.render_levels = 6

#apply the displacement modifier and set the options
displacementModifier = plane.modifiers.new(name="displacement", type='DISPLACE')
heightImagePath = os.path.join(parentPath, r"maps\heightMapStGer.png")
displacementModifier.strength = 0.3

#create a texture and apply it to the displacement modifier
displacementModifier.texture = bpy.data.textures.new(name="height Texture", type='IMAGE')
displacementModifier.texture.image = bpy.data.images.load(heightImagePath)

#create and apply a material to the plane
material = bpy.data.materials.new(name="mapMaterial")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]
texImage = material.node_tree.nodes.new("ShaderNodeTexImage")
mapImagePath = os.path.join(parentPath, r"maps\mapStGer.png")
texImage.image = bpy.data.images.load(mapImagePath)
material.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
plane.data.materials.append(material)

# add a light to the scene
sun_data = bpy.data.lights.new(name="soleil", type='SUN')
sun_data.color = (0.981, 1, 0.694) # #FFFFFF
sun_data.energy = 3
sun_data.specular_factor = 0.5
sun_data.angle = 0.5
sun = bpy.data.objects.new(name="soleil", object_data=sun_data)
bpy.context.collection.objects.link(sun)
sun.location = (0, 0, 1)
anglesInDegrees = (72, -30, -20)
angles = tuple([angle * pi / 180 for angle in anglesInDegrees])
sun.rotation_euler = angles

# add a camera to the scene
camera_data = bpy.data.cameras.new(name="camera")
camera_data.lens = 35
camera = bpy.data.objects.new(name="camera", object_data=camera_data)
bpy.context.collection.objects.link(camera)
camera.location = (1.7, -1.1, 1.1)
anglesInDegrees = (59, 0, 55)
angles = tuple([angle * pi / 180 for angle in anglesInDegrees])
camera.rotation_euler = angles

#save the scene
bpy.ops.object.mode_set(mode='OBJECT')
savePath = os.path.join(selfPath, fr"scene{time.time()}.blend")
bpy.ops.wm.save_as_mainfile(filepath=savePath)