bl_info = {
    "name" : "OVR Lipsync",
    "author" : "N1nDr0id",
    "description" : "An addon to automate lipsync using Meta's Oculus Lipsync.",
    "version" : (1, 0),
    "blender" : (4, 0, 2),
    "location" : "3D View > Sidebar > OVR Lipsync",
    "doc_url" : "https://github.com/N1nDr0id/ovr-lipsync-blender",
    "warning" : "This addon only works with mono .wav files.",
    "category" : "3D View"
}

import bpy
from bpy.props import PointerProperty, StringProperty, IntProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper
import os
import subprocess

class FrameData:
    def __init__(self):
        self.names = []
        """List of viseme names for this instance of FrameData."""

        self.frames = []
        """List of frames for this instance of FrameData. Each frame is a list containining floats that represent viseme values for said frame.
        
        Refer to this object's names list (this_object.names) for which viseme corresponds to which index."""

    # Initializes names and frames lists with appropriate values from output file
    def get_viseme_values(self, text_file_path):
        """Initializes names and frames lists with appropriate values from output file. Only to be used within from_wav_file.

        Args:
            text_file_path (str): Path to text file

        Returns:
            tuple(list(str), list(list(float))): A tuple containing 1. the list of viseme names and 2. a list of float lists representing viseme values for each frame
        """
        lines = None
        with open(text_file_path) as f:
            lines = f.readlines()

        # Everything before line 5 is simply header data for readability
        frame_values = []
        for line in lines[5:]:
            if line:
                frame_values.append([float(item.strip()) for item in line.split(";")])
        names = [item.strip() for item in lines[2][8:].split(";")]
        return (names, frame_values)

    def from_wav_file(self, wav_file_path, desired_frame_rate, output_file_path = "visemes_output.txt", keep_output_file = False):
        """Processes .wav file into viseme values for distinct frames. Must be called before FrameData can be used.

        Args:
            wav_file_path (str): Path to input .wav file
            desired_frame_rate (int): Target frame rate for visemes
            keep_output_file (bool, optional): Determines whether or not viseme output file should be kept. Defaults to False.
        """
        visemes_file_name = output_file_path
        wav_file_name = wav_file_path
        frame_rate = float(desired_frame_rate)
        print("Processing audio file...")
        subprocess.check_call([os.path.dirname(__file__) + "\\ProcessWAV.exe", str(frame_rate), wav_file_name, visemes_file_name])
        print("Done processing.")
        self.names, self.frames = self.get_viseme_values(visemes_file_name)
        if (not keep_output_file):
            os.remove(visemes_file_name)
        return self

    def get_frame_values(self, frame_index):
        """Gets the viseme values at a given frame index.

        Args:
            frame_index (int): Index of desired frame

        Raises:
            IndexError: Throws an error if frame_index is outside of valid range

        Returns:
            list(float): List of viseme values
        """
        if ((frame_index < 0) or (frame_index >= len(self.frames))):
            raise IndexError(f"Outside of valid frame range. Valid range is 0 to {len(self.frames) - 1}")
        return self.frames[frame_index]

    def print_frame(self, frame_index):
        """Pretty print for a given frame. Prints out the viseme names and values for a given frame.

        Args:
            frame_index (int): Index of desired frame

        Raises:
            IndexError: Throws an error if frame_index is outside of valid range
        """
        if ((frame_index < 0) or (frame_index >= len(self.frames))):
            raise IndexError(f"Outside of valid frame range. Valid range is 0 to {len(self.frames) - 1}")
        for i in range(len(self.names)):
            print(f"{self.names[i]}: {self.frames[frame_index][i]}")

# To workaround the "known bug with using a callback" mentioned
# in the EnumProperty docs, the function needs to be called on
# the EnumProperty's items.
ENUM_STRING_CACHE = {}
def intern_enum_items_strings(items):
    def intern_string(s):
        if isinstance(s, str):
            ENUM_STRING_CACHE.setdefault(s, s)
            s = ENUM_STRING_CACHE[s]
        return s

    return [
        tuple([intern_string(s) for s in item])
        for item in items
    ]

def shapekey_name_by_index(context, index_str):
    index = int(index_str[2:])
    if (context and
        context.scene and
        context.scene.my_collection_meshes and
        context.scene.my_collection_meshes.shape_keys):
            return context.scene.my_collection_meshes.shape_keys.key_blocks[index]
            
def is_any_shapekey_default(context):
    if (context.scene.my_collection_meshes.my_shapekey_aa == "KB0" or context.scene.my_collection_meshes.my_shapekey_aa == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_ch == "KB0" or context.scene.my_collection_meshes.my_shapekey_ch == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_dd == "KB0" or context.scene.my_collection_meshes.my_shapekey_dd == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_e == "KB0" or context.scene.my_collection_meshes.my_shapekey_e == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_ff == "KB0" or context.scene.my_collection_meshes.my_shapekey_ff == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_ih == "KB0" or context.scene.my_collection_meshes.my_shapekey_ih == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_kk == "KB0" or context.scene.my_collection_meshes.my_shapekey_kk == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_nn == "KB0" or context.scene.my_collection_meshes.my_shapekey_nn == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_oh == "KB0" or context.scene.my_collection_meshes.my_shapekey_oh == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_ou == "KB0" or context.scene.my_collection_meshes.my_shapekey_ou == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_pp == "KB0" or context.scene.my_collection_meshes.my_shapekey_pp == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_rr == "KB0" or context.scene.my_collection_meshes.my_shapekey_rr == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_ss == "KB0" or context.scene.my_collection_meshes.my_shapekey_ss == ""):
        return True
    elif (context.scene.my_collection_meshes.my_shapekey_th == "KB0" or context.scene.my_collection_meshes.my_shapekey_th == ""):
        return True
    return False

# This callback will return a list of enum items in the usual
# [(identifier, name, description), ...] format.
def my_shapekey_enum_items_callback(self, context):
    items = []

    if self and self.shape_keys:
        items = [
            (f'KB{i}', kb.name, '')
            for i, kb in enumerate(self.shape_keys.key_blocks)
        ]

    return intern_enum_items_strings(items)


class OT_TestOpenFilebrowserWav(bpy.types.Operator, ImportHelper): 
    bl_idname = "filepicker.open_filebrowser"
    bl_label = "Pick .wav File"
    bl_description = "Opens a file picker to pick a .wav file for lipsync"
    
    filter_glob: StringProperty( 
        default='*.wav', 
        options={'HIDDEN'} 
    )
    
    def execute(self, context):
        """Do something with the selected file(s)."""
        filename, extension = os.path.splitext(self.filepath)
        print('Selected file:', self.filepath)
        print('File name:', filename)
        print('File extension:', extension)
        if not (extension.lower() == ".blend"):
            context.scene.audio_file_path = self.filepath
        return {'FINISHED'}


def filter_callback(self, object):
    return object.name in bpy.data.meshes.keys()

class insert_keyframes(bpy.types.Operator):
    bl_idname = "test_keyframe.func1"
    bl_label = "Apply Keyframes"
    bl_description = "Applies viseme keyframes for the given audio. Requires all visemes to be properly selected and a valid .wav file to be chosen"
    def execute(self, context):
        if not (context.scene.audio_file_path.endswith(".wav")):
            self.report({"WARNING"}, "Selected audio file is not a .wav file!")
            return {"CANCELLED"}
        if (is_any_shapekey_default(context)):
            self.report({"WARNING"}, "Not all viseme shapekeys are properly mapped! Ensure viseme shapekeys are mapped to something other than the Basis (default) shapekey.")
            return {"CANCELLED"}
        if (context.scene.my_collection_meshes and context.scene.audio_file_path and not is_any_shapekey_default(context)):
            context.scene.audio_folder_path = os.path.dirname(context.scene.audio_file_path)
            scene_fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
            viseme_fps = 100
            output_file_path = context.scene.audio_folder_path + "\\visemes_output.txt"
            frame_data = FrameData().from_wav_file(context.scene.audio_file_path, viseme_fps, output_file_path = output_file_path, keep_output_file=False)
            # For now, assume viseme names follow this pattern: "vrc.v_(name)"
            # Add ability to change this later
            audio_length = len(frame_data.frames) / viseme_fps
            audio_length_frames = audio_length * scene_fps
            #viseme_fps / scene_fps
            for i in range(int(audio_length_frames)):
                frame_index = int(i * (viseme_fps / scene_fps))
                frame = frame_data.get_frame_values(frame_index)
                for name_index in range(len(frame_data.names)):
                    shape = None
                    if not (frame_data.names[name_index].lower() == "sil"):
                        shape_value = frame[name_index]
                    if (frame_data.names[name_index].lower() == "aa"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_aa)
                    elif (frame_data.names[name_index].lower() == "ch"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ch)
                    elif (frame_data.names[name_index].lower() == "dd"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_dd)
                    elif (frame_data.names[name_index].lower() == "e"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_e)
                    elif (frame_data.names[name_index].lower() == "ff"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ff)
                    elif (frame_data.names[name_index].lower() == "ih"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ih)
                    elif (frame_data.names[name_index].lower() == "kk"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_kk)
                    elif (frame_data.names[name_index].lower() == "nn"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_nn)
                    elif (frame_data.names[name_index].lower() == "oh"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_oh)
                    elif (frame_data.names[name_index].lower() == "ou"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ou)
                    elif (frame_data.names[name_index].lower() == "pp"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_pp)
                    elif (frame_data.names[name_index].lower() == "rr"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_rr)
                    elif (frame_data.names[name_index].lower() == "ss"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ss)
                    elif (frame_data.names[name_index].lower() == "th"):
                        shape = shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_th)
                        #name = "vrc.v_" + frame_data.names[name_index].lower()
                        #context.scene.my_collection_meshes.shape_keys.key_blocks[name].value = shape_value
                        #context.scene.my_collection_meshes.shape_keys.key_blocks[name].keyframe_insert(data_path='value', frame=i + context.scene.start_frame)
                    if (shape != None):
                        shape.value = shape_value
                        shape.keyframe_insert(data_path='value', frame=i + context.scene.start_frame)
        return {'FINISHED'}

class clear_lip_shapekeys(bpy.types.Operator):
    bl_idname = "test_keyframe.func3"
    bl_label = "Clear Viseme Shapekeys"
    bl_description = "Clears shapekey values for currently selected viseme shapekeys"
    def execute(self, context):
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_aa).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ch).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_dd).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_e).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ff).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ih).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_kk).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_nn).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_oh).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ou).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_pp).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_rr).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_ss).value = 0.0
        shapekey_name_by_index(context, context.scene.my_collection_meshes.my_shapekey_th).value = 0.0
        return {'FINISHED'}
    
class clear_shapekeys(bpy.types.Operator):
    bl_idname = "test_keyframe.func2"
    bl_label = "Clear All Shapekeys"
    bl_description = "Clears shapekey values for all shapekeys on selected mesh. Use with caution"
    def execute(self, context):
        for shapekey in context.scene.my_collection_meshes.shape_keys.key_blocks:
            shapekey.value = 0.0
        return {'FINISHED'}

class TestPanel_PT_mainpanel(bpy.types.Panel):
    bl_label = "Lipsync"
    bl_idname = "TESTPANEL_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OVR Lipsync"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        row = layout.row()
        row.prop(scene, "my_collection_meshes")
        row = layout.row()
        row.prop(scene, "start_frame")
        if (context and
            context.scene and
            context.scene.my_collection_meshes and
            context.scene.my_collection_meshes.shape_keys):
            row = layout.row()
            row.prop(scene, "audio_file_path")
            row = layout.row()
            row.operator(OT_TestOpenFilebrowserWav.bl_idname)
            row = layout.row()
            row.operator(insert_keyframes.bl_idname)
            if (context.scene.audio_file_path and not is_any_shapekey_default(context)):
                row.active = True
            else:
                row.active = False
            row = layout.row()
            row.operator(clear_lip_shapekeys.bl_idname)
            row = layout.row()
            row.operator(clear_shapekeys.bl_idname)

class TESTPANEL_PT_visemespanel(bpy.types.Panel):
    bl_parent_id = "TESTPANEL_PT_main"
    bl_label = "Viseme Mapping"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OVR Lipsync"
    
    def draw(self, context):
        layout = self.layout
        if (context and
            context.scene and
            context.scene.my_collection_meshes and
            context.scene.my_collection_meshes.shape_keys):
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_aa")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_ch")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_dd")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_e")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_ff")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_ih")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_kk")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_nn")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_oh")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_ou")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_pp")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_rr")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_ss")
            row = layout.row()
            row.prop(context.scene.my_collection_meshes, "my_shapekey_th")
        


classes = [OT_TestOpenFilebrowserWav, insert_keyframes, clear_lip_shapekeys, clear_shapekeys, TestPanel_PT_mainpanel, TESTPANEL_PT_visemespanel]

def register():
    bpy.types.Scene.my_collection_meshes = PointerProperty(
        name="Mesh",
        type=bpy.types.Mesh,
        poll=filter_callback)
    bpy.types.Scene.start_frame = IntProperty(name="Start Frame", description="Beginning frame for audio to be applied", default=0, min=0, subtype='UNSIGNED')
    bpy.types.Scene.audio_file_path = StringProperty(name="Audio File Path", description="Path to .wav file", default="")
    bpy.types.Scene.audio_folder_path = StringProperty(name="Temp Folder Path", description="Path to folder containing .wav file. This is where the visemes_output.txt file will be temporarily stored before being deleted", default="")
    
    bpy.types.Mesh.my_shapekey_aa = bpy.props.EnumProperty(
        name="AA",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_ch = bpy.props.EnumProperty(
        name="CH",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_dd = bpy.props.EnumProperty(
        name="DD",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_e = bpy.props.EnumProperty(
        name="E",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_ff = bpy.props.EnumProperty(
        name="FF",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_ih = bpy.props.EnumProperty(
        name="IH",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_kk = bpy.props.EnumProperty(
        name="KK",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_nn = bpy.props.EnumProperty(
        name="NN",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_oh = bpy.props.EnumProperty(
        name="OH",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_ou = bpy.props.EnumProperty(
        name="OU",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_pp = bpy.props.EnumProperty(
        name="PP",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_rr = bpy.props.EnumProperty(
        name="RR",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_ss = bpy.props.EnumProperty(
        name="SS",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    bpy.types.Mesh.my_shapekey_th = bpy.props.EnumProperty(
        name="TH",
        description="Select a shapekey",
        items=my_shapekey_enum_items_callback,
    )
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Collection.my_collection_meshes
    del bpy.types.Scene.start_frame
    del bpy.types.Scene.audio_file_path
    del bpy.types.Scene.audio_folder_path
    del bpy.types.Mesh.my_shapekey_aa
    del bpy.types.Mesh.my_shapekey_ch
    del bpy.types.Mesh.my_shapekey_dd
    del bpy.types.Mesh.my_shapekey_e
    del bpy.types.Mesh.my_shapekey_ff
    del bpy.types.Mesh.my_shapekey_ih
    del bpy.types.Mesh.my_shapekey_kk
    del bpy.types.Mesh.my_shapekey_nn
    del bpy.types.Mesh.my_shapekey_oh
    del bpy.types.Mesh.my_shapekey_ou
    del bpy.types.Mesh.my_shapekey_pp
    del bpy.types.Mesh.my_shapekey_rr
    del bpy.types.Mesh.my_shapekey_ss
    del bpy.types.Mesh.my_shapekey_th
    

if (__name__ == "__main__"):
    register()