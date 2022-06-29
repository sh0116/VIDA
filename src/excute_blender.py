import os
def excute(cubedata,tagdata,title):
    tagstring = ""
    for tagd in tagdata:
        temp = ''
        for tagdd in tagd: temp += str(tagdd)+"::" 
        tagstring += temp+";;"

    cubedatastring = ""
    for cubed in cubedata: cubedatastring += str(cubed)+";;" 

    print(len(cubedatastring))
    with open("cube_String.txt", "w") as f:
        f.write(cubedatastring)

    #res = os.system(".\\Blender_dir\\blender.exe --background --python .\\FloorPlan\\blender_script.py "+tagstring.replace(" ","")+" "+cubedatastring.replace(" ","")+" "+str(title).replace(" ",""))
    res = os.system("C:\\VIDA\\Blender_dir\\blender.exe --background --python C:\\VIDA\\FloorPlan\\blender_script.py "+tagstring.replace(" ","")+" "+str(title).replace(" ",""))

    if res: print("successful : make model")
    else: print("failed : make model")

    return res
