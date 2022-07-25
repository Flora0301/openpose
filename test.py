#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:17:47 2020

@author: joe
"""


from src import torch_openpose,util

import cv2

video_path = './video/20220628140.mkv'
cap = cv2.VideoCapture(video_path)

RBigToe_list = []

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        break

    tp = torch_openpose.torch_openpose('body_25')  # 载入模型
    poses, heels, heel, position = tp(img)  # poses, heels 全部人的关键点，heel，position 目标人物关键点
    # print("position: " + str(position))

    # 脚趾关键点坐标
    RBigToe = position[0][22]
    print("RBigToe: " + str(RBigToe))
    RBigToe_list.append(RBigToe)

    # img = util.draw_bodypose(img, poses, 'body_25')
    cv2.imshow('v', img)

    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()

# 提取起始帧
# print("list: " + str(RBigToe_list))

num = len(RBigToe_list)
dist = 0
dist_list = []
frame_up = 0
frame_down = 0
next = 0

x1 = 0
y1 = 0
for i in range(num):
    x = RBigToe_list[i][0]
    y = RBigToe_list[i][1]
    dist = pow(pow(x-x1, 2) + pow(y-y1, 2), 0.5)
    dist_list.append(dist)
    x1 = x
    y1 = y
    print(str(i) + " dist: " + str(dist))

print("dis_list: " + str(dist_list))
for i in range(1, num):
    if dist_list[i] > 10:
        frame_up = i
        print("起始帧： " + str(frame_up))
        break

for j in range(frame_up, num):
    if dist_list[j] < 10:
        frame_down = j + 1
        print("结束帧： " + str(frame_down))
        break
# for i in range(num):
#     if i % 2 == 0:
#         prior = RBigToe_list[i][1]
#         dist = next - prior
#         next = prior
#         if frame_up != 0 :
#             if dist > 10:
#                 frame_up = i
#
# # 提取结束帧
# for j in range(frame_up, num, 2):
#



# position: [[[297.0, 174.0, 1.0210559368133545], [267.0, 206.0, 0.9706293344497681], [241.0, 209.0, 0.9450704455375671],
#             [237.0, 276.0, 0.953989565372467], [251.0, 333.0, 0.9816102981567383], [293.0, 203.0, 0.9242585301399231],
#             [313.0, 259.0, 0.445705771446228], [0.0, 0.0, 0.0], [299.0, 325.0, 0.9471896886825562],
#             [280.0, 327.0, 0.9307724833488464], [286.0, 408.0, 0.8837556838989258], [294.0, 484.0, 0.9267120361328125],
#             [320.0, 323.0, 0.8936924934387207], [320.0, 405.0, 0.9090144634246826], [311.0, 477.0, 0.8894822001457214],
#             [290.0, 168.0, 0.9767276048660278], [299.0, 167.0, 0.6939061284065247], [263.0, 168.0, 1.000135898590088],
#             [0.0, 0.0, 0.0], [340.0, 493.0, 0.7072316408157349], [343.0, 486.0, 0.7370491623878479],
#             [306.0, 485.0, 0.5802323222160339], [325.0, 498.0, 0.8199432492256165], [307.0, 503.0, 0.7995603084564209],
#             [290.0, 492.0, 0.7928311228752136]]]


