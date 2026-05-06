import bpy
import math
import os

def transform_entity(name, loc=(0,0,0), rot_deg=(0,0,0), relative=False):
    rot_rad = [math.radians(deg) for deg in rot_deg]
    mode = "relatively" if relative else "absolutely"

    if name in bpy.data.objects:
        obj = bpy.data.objects[name]
        if relative:
            obj.location.x += loc[0]
            obj.location.y += loc[1]
            obj.location.z += loc[2]
            for i in range(3):
                obj.rotation_euler[i] += rot_rad[i]
        else:
            obj.location = loc
            obj.rotation_euler = rot_rad
        print(f"SUCCESS: Transformed object '{name}' {mode}")

    elif name in bpy.data.collections:
        collection = bpy.data.collections[name]
        
        root_objects = [obj for obj in collection.objects if obj.parent not in collection.objects.values()]
        
        if not root_objects:
            print(f"WARNING: Collection '{name}' is empty or has no root objects.")
            return

        for obj in root_objects:
            if relative:
                obj.location.x += loc[0]
                obj.location.y += loc[1]
                obj.location.z += loc[2]
                for i in range(3):
                    obj.rotation_euler[i] += rot_rad[i]
            else:
                obj.location = loc
                obj.rotation_euler = rot_rad
        print(f"SUCCESS: Transformed collection '{name}' {mode}")

    else:
        print(f"ERROR: Entity '{name}' not found in objects or collections.")

def add_custom_light(name="NewLight", l_type='POINT', loc=(0,0,0), rot_deg=(0,0,0), energy=1000):
    bpy.ops.object.light_add(type=l_type, location=loc)
    light_obj = bpy.context.active_object
    light_obj.name = name
    light_obj.data.energy = energy
    light_obj.rotation_euler = [math.radians(d) for d in rot_deg]
    print(f"Added light: {name} ({l_type})")
    return light_obj

def add_camera(name="NewCamera", loc=(0,0,0), rot_deg=(0,0,0)):
    bpy.ops.object.camera_add(location=loc)
    cam_obj = bpy.context.active_object
    cam_obj.name = name
    cam_obj.rotation_euler = [math.radians(d) for d in rot_deg]
    
    print(f"Added camera: {name}")
    return cam_obj

def import_object(filepath, obj_name, loc=(0,0,0), rot_deg=(0,0,0)):
    if not os.path.exists(filepath):
        print(f"ERROR: File does not exist: {filepath}")
        return

    inner_path = os.path.join(filepath, "Object")
    
    try:
        bpy.ops.wm.append(
            directory=inner_path + os.sep,
            filename=obj_name
        )
        
        obj = bpy.context.active_object
        
        if obj and (obj.name.startswith(obj_name)):
            obj.location = loc
            obj.rotation_euler = [math.radians(d) for d in rot_deg]
            print(f"SUCCESS: Imported object '{obj_name}' and set to {loc}")
        else:
            print(f"WARNING: Import might have succeeded, but object '{obj_name}' was not recognized.")
            
    except Exception as e:
        print(f"Object import error: {e}")

def import_collection(filepath, coll_name, main_obj_name=None, loc=(0,0,0), rot_deg=(0,0,0)):
    if not os.path.exists(filepath):
        print(f"ERROR: File does not exist: {filepath}")
        return

    inner_path = os.path.join(filepath, "Collection")
    
    try:
        bpy.ops.wm.append(
            directory=inner_path + os.sep,
            filename=coll_name
        )
        
        if coll_name in bpy.data.collections:
            new_coll = bpy.data.collections[coll_name]
            
            if main_obj_name:
                main_obj = new_coll.objects.get(main_obj_name) 
                
                if main_obj:
                    main_obj.location = loc
                    main_obj.rotation_euler = [math.radians(d) for d in rot_deg]
                    print(f"SUCCESS: Imported collection '{coll_name}' and transformed '{main_obj_name}'")
                else:
                    print(f"WARNING: Collection '{coll_name}' imported, but main object '{main_obj_name}' not found inside.")
            else:
                print(f"SUCCESS: Imported collection '{coll_name}'")
        
    except Exception as e:
        print(f"Collection import error: {e}")

def edit_camera(name="Camera", focal_length=50.0, use_dof=False, focus_dist=10.0, fstop=2.8, focus_obj_name=None):
    if name not in bpy.data.objects:
        print(f"ERROR: Camera '{name}' not found.")
        return
        
    cam_obj = bpy.data.objects[name]
    
    if cam_obj.type != 'CAMERA':
        print(f"ERROR: Object '{name}' is not a camera.")
        return
        
    cam_data = cam_obj.data  
    cam_data.lens = focal_length
    cam_data.dof.use_dof = use_dof
    
    if use_dof:
        cam_data.dof.aperture_fstop = fstop
        
        if focus_obj_name and focus_obj_name in bpy.data.objects:
            cam_data.dof.focus_object = bpy.data.objects[focus_obj_name]
            print(f"Camera DoF focused on object: {focus_obj_name}")
        else:
            cam_data.dof.focus_distance = focus_dist
            cam_data.dof.focus_object = None
            print(f"Camera DoF focus distance set to: {focus_dist}m")
            
    print(f"SUCCESS: Edited camera '{name}' (Focal Length: {focal_length}mm, DoF: {use_dof})")

def edit_light(name, energy=None, color: tuple = None):
    if name not in bpy.data.objects:
        print(f"ERROR: Light '{name}' not found.")
        return
        
    light_obj = bpy.data.objects[name]
    
    if light_obj.type != 'LIGHT':
        print(f"ERROR: Object '{name}' is not a light.")
        return
        
    light_data = light_obj.data
    
    if energy is not None:
        light_data.energy = energy
        
    if color is not None:
        if isinstance(color, tuple) and len(color) >= 3:
            light_data.color = color[:3]
        else:
            print(f"WARNING: Invalid color format for '{name}'. Expected a tuple.")
            return
            
    print(f"SUCCESS: Edited light '{name}' (Energy: {energy}, Color: {color})")

def start_render(output_path, filename, start_frame, end_frame, is_animation=True):
    scene = bpy.context.scene
    scene.render.filepath = os.path.join(output_path, filename)
    
    if is_animation:
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
        scene.frame_start = start_frame
        scene.frame_end = end_frame
        print(f"Starting animation render (MP4): {filename}...")
    else:
        scene.render.image_settings.file_format = 'PNG'
        print(f"Starting still render (PNG): {filename}...")

    bpy.ops.render.render(animation=is_animation, write_still=True)
    print(f"SUCCESS: Render saved to {output_path}")

asset_path = r"C:\Users\huber\Desktop\Blender\Assets\donut.blend"

#import_collection(asset_path, "DonutAsset", "Donut", loc=(0, 0, 0), rot_deg=(0, 0, 0))
#add_custom_light('POINT', loc=(0,0,0), energy=1000, name="MojeSwiatlo")

#transform_entity("DonutAsset", loc=(5, 5, 0), rot_deg=(0, 0, 45), relative=False)
#transform_entity("Cube", loc=(10, 10, 0), relative=False)
#transform_entity("Camera", loc=(0, -10, 5), rot_deg=(90, 0, 0), relative=False)
#transform_entity("MojeSwiatlo", loc=(0, 0, 10), relative=False)
add_camera("cam1", (0,0,0), (0,0,0),)
add_custom_light("l1",'SUN',(10, 10, 0), (0,0,0), 1000)
edit_light("l1", 1000, (1.0,0.0,0.0))
start_render(r"C:\Users\huber\Desktop\Blender", "asd", 1, 2, False)

#edit_camera("Camera", focal_length=85.0, use_dof=True, fstop=2.8, focus_obj_name="Donut")