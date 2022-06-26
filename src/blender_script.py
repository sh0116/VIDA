import bpy


# a5 size 150 * 210
def create_A5():
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(105, 105, 0), scale=(105.0, 105.0, 3.0))
    
    print("success make cube")

def create_cube(x,y,dx,dy):
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(x, y, 1.5), scale=(dx, dy, 3.0))
    print("success make cube")

# standard dot size 
def create_uv(loc,cnt,x,y):
    loc = 210-(x+loc[0]+(cnt*5.5)),y+loc[1],loc[2]
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=loc, scale=(0.75, 0.75, 0.6))

def make_dot(SL):
    x,y,dot_list,_ = SL
    #dot_list = dot_list[2:-2].split("],[")
    list_dot_location = [(0,0,3),(0,2.3,3),(0,4.6,3),(-2.3,0,3),(-2.3,2.3,3),(-2.3,4.6,3)]
    cnt=0
    for dot in dot_list[2:-2].split("],["):
        dot = list(map(int,dot.split(",")))
        for loc_i in range(len(list_dot_location)):
            if dot[loc_i]:
                create_uv(list_dot_location[loc_i],cnt,int(x)//2,int(y)//2)
        cnt+=1
    

def make_maptitle(tag_list,title):
    list_dot_location = [(0,0,3),(0,2.3,3),(0,4.6,3),(-2.3,0,3),(-2.3,2.3,3),(-2.3,4.6,3)]
    cnt = 0
    y_point = 155
    x_point = 10
    for ti in title:
        for loc_i in range(len(list_dot_location)):
            if ti[loc_i]:
                create_uv(list_dot_location[loc_i],cnt,x_point,y_point)
        cnt+=1

    y_point += 5
    for ti in tag_list:
        x,y,dot_list,title_strings = ti
        if y_point>=200:
            y_point = 170
            x_point = 115
        else:
            y_point += 10
        cnt = 0
        for dot in dot_list[2:-2].split("],["):
            dot = list(map(int,dot.split(",")))
            for loc_i in range(len(list_dot_location)):
                if dot[loc_i]:
                    create_uv(list_dot_location[loc_i],cnt,x_point,y_point)
            cnt+=1
        cnt+=2
        for title_string in title_strings[2:-2].split("],["):
            title_string = list(map(int,title_string.split(",")))
            for loc_i in range(len(list_dot_location)):
                if title_string[loc_i]:
                    create_uv(list_dot_location[loc_i],cnt,x_point,y_point)
            cnt+=1
    
        
    
#  점자만드는 main스크립트    
def main():
    # execute script
    # blender --background --python C:\Users\seokh\OneDrive\Desktop\KBSC\blender_script.py
    # 4 == tag 5 == cube 6 == title
    import sys,os
    
    tag_string = sys.argv[4]
    #cube_string = sys.argv[5]
    title = sys.argv[5]
    tag_list = []

    for ts in tag_string.split(";;")[:-1]:
        temp_ts = []
        for tt in ts.split("::")[:-1]:
            temp_ts.append(tt)
        tag_list.append(temp_ts)

    f = open("cube_String.txt", 'r')
    cube_string = f.readline()
    f.close()

    cube_list = []
    for cs in cube_string.split(";;")[:-1]:
        cs = cs[1:-1]
        cube_list.append(cs.split(","))
    
    title_list = []
    for ti in title[2:-2].split("],["):
        title_list.append(list(map(int,ti.split(","))))

    #print(cube_list)
    #print("********************************")
    #print(tag_list)
    #cube_list = [['203', '228', '224', '232'], ['150', '159', '218', '240'], ['287', '326', '201', '210'], ['338', '346', '201', '211'], ['346', '355', '191', '211'], ['346', '355', '157', '186'], ['142', '149', '148', '158'], ['142', '149', '194', '204'], ['149', '158', '148', '213'], ['42', '91', '149', '158'], ['91', '101', '148', '203'], ['101', '113', '147', '158'], ['101', '116', '194', '204'], ['4', '13', '143', '158'], ['13', '23', '148', '158'], ['254', '264', '133', '240'], ['264', '266', '133', '143'], ['264', '276', '201', '211'], ['279', '313', '133', '142'], ['313', '322', '130', '142'], ['322', '346', '133', '142'], ['346', '356', '133', '151'], ['356', '368', '133', '142'], ['387', '400', '133', '142'], ['400', '409', '123', '142'], ['3', '13', '84', '138'], ['280', '286', '106', '117'], ['286', '296', '98', '116'], ['296', '312', '98', '107'], ['307', '312', '65', '74'], ['312', '323', '65', '117'], ['323', '400', '65', '74'], ['400', '409', '65', '118'], ['3', '14', '66', '78'], ['14', '87', '65', '74'], ['87', '91', '65', '91'], ['87', '96', '104', '131'], ['91', '96', '49', '91'], ['96', '101', '48', '74'], ['96', '136', '121', '131'], ['101', '136', '65', '74'], ['136', '147', '60', '91'], ['136', '147', '104', '131'], ['147', '173', '60', '69'], ['147', '180', '122', '131'], ['173', '180', '58', '90'], ['180', '182', '58', '131'], ['182', '189', '60', '69'], ['170', '173', '18', '28'], ['173', '183', '18', '44'], ['254', '264', '65', '116'], ['264', '266', '107', '116'], ['183', '283', '18', '27'], ['264', '283', '65', '74'], ['283', '293', '18', '74'], ['293', '300', '65', '74'], ['91', '101', '19', '43'],['101', '153', '18', '28']]
    #tag_list = [['8', '94', '[[0,0,1,1,1,1],[0,1,0,1,1,0]]', '[[1,1,0,1,1,0],[1,1,0,0,0,1],[0,1,0,0,1,0],[0,0,0,1,1,0],[1,1,0,0,0,1],[0,1,1,0,1,1]]'], ['345', '101', '[[0,0,1,1,1,1],[1,0,0,0,0,0]]', '[[0,0,0,0,1,1],[1,0,1,0,1,0],[0,1,0,0,0,1],[0,0,0,0,0,1],[1,0,1,0,1,0],[0,1,0,0,0,0]]'], ['166', '40', '[[0,0,1,1,1,1],[1,1,0,0,0,0]]', '[[0,0,0,1,1,0],[1,0,1,1,0,0],[1,1,0,1,1,0],[0,1,1,1,0,0],[0,1,1,0,1,0]]'], ['262', '41', '[[0,0,1,1,1,1],[1,0,0,1,0,0]]', '[[0,0,0,1,1,0],[1,0,1,1,1,0],[0,0,0,0,1,0],[1,1,0,0,0,1],[0,1,0,0,1,0],[0,1,0,1,0,0],[1,1,0,0,0,1]]'], ['188', '186', '[[0,0,1,1,1,1],[1,0,0,1,1,0]]', '[[0,0,0,1,0,0],[0,1,1,1,0,0],[0,0,0,0,0,1],[1,0,1,0,1,0],[0,1,0,0,0,0]]'], ['93', '167', '[[0,0,1,1,1,1],[1,0,0,0,1,0]]', '[[0,0,0,1,0,1],[1,1,0,0,0,1],[1,0,0,0,0,0],[1,1,0,1,1,0],[0,1,0,1,0,1],[0,1,0,0,1,0],[0,0,0,1,1,0],[1,1,0,0,0,1],[0,1,1,0,1,1]]'], ['117', '84', '[[0,0,1,1,1,1],[1,1,0,1,0,0]]', '[[0,1,0,1,1,0],[1,1,1,0,0,1],[0,0,0,1,0,1],[1,1,0,0,0,1],[0,1,1,0,1,1],[0,0,0,0,0,1],[1,0,1,0,1,0],[0,1,0,0,0,0]]']]
    #title_list = [[1, 1, 0, 1, 1, 0], [1, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 0], [1, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0], [1, 1, 0, 0, 0, 0]]

    print("successful : execute blender script!")
    create_A5()
    print("successful : make create_A5!")
    make_maptitle(tag_list, title_list)
    #print("title")
    #print(title_list)
    #print("cube")
    #print(cube_list)
    for s in cube_list:
        x,x1,y,y1 = map(int,s)
        create_cube(((((x1-x)/2)+x)*0.5),((((y1-y)/2)+y)*0.5)-0.5,((x1-x)/2)*0.5,(((y1-y)/2)*0.5)+0.5)
    print("successful : make cube!")
    #print(tag_list)
    for tag in tag_list:
        make_dot(tag)
    print("successful : make braille!")
    
    windows_user_name = os.path.expanduser('~')
    a = windows_user_name+"\\Downloads\\"+"result.stl"  
    print(a)
    bpy.ops.export_mesh.stl(filepath=a)

main()