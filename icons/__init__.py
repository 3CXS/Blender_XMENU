import os
import bpy

icons_collection = None
icons_directory = os.path.dirname(__file__)

def get_icon_id(identifier):
    return get_icon(identifier).icon_id

def get_icon(identifier):
    if identifier in icons_collection:
        return icons_collection[identifier]
    return icons_collection.load(identifier, os.path.join(icons_directory, identifier + ".png"), "IMAGE")

def get_icon_raw(identifier):
    if identifier in icons_collection:
        return icons_collection[identifier]
    return icons_collection.load(identifier, os.path.join(icons_directory, identifier + ".png"), "IMAGE")

def load_icons():
    global icons_collection
    icons_collection = bpy.utils.previews.new()

def unload_icons():
    bpy.utils.previews.remove(icons_collection)
