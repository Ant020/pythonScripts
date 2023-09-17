import os
import psutil
import subprocess

# Fonction pour rechercher le chemin d'accès de Blender
f = open("myfile.txt", "x") 
f.close()
def find_blender_path() -> str:
    # Find the path to Blender.exe 
    blender_exe: str = "blender.exe"
    roots_directories: list[str] = [partition.mountpoint for partition in psutil.disk_partitions()]
    
    for directory in roots_directories:
        for root, _, files in os.walk(directory):
            if blender_exe in files:
                return os.path.join(root, blender_exe)        
    
    return None

blenderPath = find_blender_path()
selfPath = os.path.dirname(os.path.realpath(__file__))
scenePath = os.path.join(selfPath, "scene.py")
subprocess.run([blenderPath, "-b", "-P", scenePath])
print('Done!')