from random import randrange
from GanntChart import *
import math
import copy
def rand_color(num_color):
    # color_list=[]
    # '''init color'''
    # init=[[0,255,142],[146,0,204],[255,174,0]]
    #
    # for i ,j in enumerate(init):
    #     color_list.append(copy.deepcopy(j))
    #
    # num_layer=int(math.ceil(num_color/3))
    # for l in range(num_layer,0,-1):
    #     if len(color_list) == num_color:
    #         break
    #     for k, j in enumerate(init):
    #         d_r = (255 - j[0])/l
    #         d_g = (255 - j[1])/l
    #         d_b = (255 - j[2])/l
    #         j[0] += d_r
    #         j[1] += d_g
    #         j[2] += d_b
    #         color_list.append(copy.deepcopy(j))
    #         if len(color_list)==num_color:
    #             break
    # print(color_list)
    # '''trans to hex'''
    # '''trans to hex'''
    # out_list = []
    # for i, j in enumerate(color_list):
    #     color_code = "#"
    #     for k, l in enumerate(j):
    #         if l < 16:
    #             color_code += "0"
    #         if l == 0:
    #             color_code += "0"
    #         # a=str(hex(int(l)).lstrip("0x").rstrip("L"))
    #         color_code += str(hex(int(l)).lstrip("0x").rstrip("L"))
    #     out_list.append(color_code)
    # out="#"+str(hex(r).lstrip("0x").rstrip("L"))+str(hex(g).lstrip("0x").rstrip("L"))+str(hex(b).lstrip("0x").rstrip("L"))
    # print(hex(r).lstrip("0x").rstrip("L"),g,b)
    # print(out_list)
    out_list=["14B278","F0CA4D","E37B40","ED3752","66A8CC","0C6899","98FFEC","FFDDD8","CC666C","05A124"]
    return out_list
def draw_gan():
    path="data_2_10_t"
    gan = GanntChart()
    gan.init(2, 30, 30)

    l=[[3,1,0,1],[0,1,1,8],[1,2,0,3],[2,2,3,9],[4,1,9,3],[7,1,12,3],[9,2,12,4],[4,1,15,6],
       [8,2,16,6],[6,1,21,9],[5,2,22,8]
       ]
    for k, j in enumerate(l):
        gan.AddJob("J" + str(j[0])+"("+str(j[3])+")", j[1], j[2], j[3])
    gan.SavetoFile("Gannt Chart/" + path)

if __name__=="__main__":
    # draw_gan()
    num_color=10
    rand_color(num_color)