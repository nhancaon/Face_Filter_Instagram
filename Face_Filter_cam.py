from PIL import Image, ImageDraw
import face_recognition
import math
import numpy
import cv2
import os

def Bat_Filter(image, result):
    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    bat = Image.open('./Filter_image/bat.png')
    left_eye = numpy.array(face_landmarks_list[0]['left_eye'][0])
    right_eye = numpy.array(face_landmarks_list[0]['right_eye'][0])
    angle = math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
    bat_angle = -math.atan(angle) * 180 / math.pi
    bat_angle_rad = math.radians(bat_angle)
    Angle_matrix = numpy.array([[math.cos(bat_angle_rad), -math.sin(bat_angle_rad)], [
                               math.sin(bat_angle_rad), math.cos(bat_angle_rad)]])
    Vector1 = numpy.array([41 - bat.size[0]//2, bat.size[1]//2 - 307])
    Vector2 = numpy.array([178 - bat.size[0]//2, bat.size[1]//2 - 307])
    res1 = numpy.dot(Angle_matrix, Vector1)
    res2 = numpy.dot(Angle_matrix, Vector2)

    pre_bat_size = bat.size
    bat = bat.rotate(bat_angle, expand=True)
    aft_bat_size = bat.size
    bat_delta = (face_landmarks_list[0]['right_eye'][0][0] -
                 face_landmarks_list[0]['left_eye'][0][0])/(res2[0] - res1[0])
    bat = bat.resize(
        (int(bat.size[0] * bat_delta), int(bat.size[1] * bat_delta)))
    center_eye = [face_landmarks_list[0]['left_eye'][0][0] + (face_landmarks_list[0]['left_eye'][3][0] - face_landmarks_list[0]['left_eye'][0][0])/2,
                  face_landmarks_list[0]['left_eye'][0][1] + (face_landmarks_list[0]['left_eye'][3][1] - face_landmarks_list[0]['left_eye'][0][1])]

    pil_image = Image.fromarray(image)
    Vector3 = numpy.array([75 * bat_delta - bat.size[0]//2 / aft_bat_size[0]*pre_bat_size[0],
                          bat.size[1]//2 / aft_bat_size[1]*pre_bat_size[1] - 320 * bat_delta])
    res3 = numpy.dot(Angle_matrix, Vector3)
    test = [bat.size[0]//2 + res3[0], bat.size[1]//2 - res3[1]]
    LocoBat = [int(center_eye[0] - (bat.size[0]//2 + res3[0])),
               int(center_eye[1] - (bat.size[1]//2 - res3[1]))]

    # DEBUGGING
    # print(Vector3)
    # print(res3)
    # print(test)
    # print(bat.size[0]//2, bat.size[1]//2)
    # d = ImageDraw.Draw(bat, 'RGBA')
    # d.point(center_eye, fill=(150, 0, 0))
    # d.ellipse((test[0] - 5, test[1] - 5, test[0] + 5,test[1] + 5), fill='#f00')
    pil_image.paste(bat, LocoBat, bat)
    result[0] = pil_image
    return pil_image


def SunGlass_filter(image, result):
    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)

    bat = Image.open('./Filter_image/glasses.png')
    left_eye = numpy.array(face_landmarks_list[0]['left_eye'][0])
    right_eye = numpy.array(face_landmarks_list[0]['right_eye'][0])
    angle = math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
    bat_angle = -math.atan(angle) * 180 / math.pi
    bat_angle_rad = math.radians(bat_angle)
    Angle_matrix = numpy.array([[math.cos(bat_angle_rad), -math.sin(bat_angle_rad)], [
                               math.sin(bat_angle_rad), math.cos(bat_angle_rad)]])
    Vector1 = numpy.array([21 - bat.size[0]//2, bat.size[1]//2 - 88])
    Vector2 = numpy.array([292 - bat.size[0]//2, bat.size[1]//2 - 88])
    res1 = numpy.dot(Angle_matrix, Vector1)
    res2 = numpy.dot(Angle_matrix, Vector2)

    pre_bat_size = bat.size
    bat = bat.rotate(bat_angle, expand=True)
    aft_bat_size = bat.size
    bat_delta = (face_landmarks_list[0]['right_eye'][0][0] -
                 face_landmarks_list[0]['left_eye'][0][0])/(res2[0] - res1[0])
    bat = bat.resize(
        (int(bat.size[0] * bat_delta), int(bat.size[1] * bat_delta)))
    center_eye = [face_landmarks_list[0]['left_eye'][0][0] + (face_landmarks_list[0]['left_eye'][3][0] - face_landmarks_list[0]['left_eye'][0][0])/2,
                  face_landmarks_list[0]['left_eye'][0][1] + (face_landmarks_list[0]['left_eye'][3][1] - face_landmarks_list[0]['left_eye'][0][1])]

    pil_image = Image.fromarray(image)

    Vector3 = numpy.array([121 * bat_delta - bat.size[0]//2 / aft_bat_size[0]*pre_bat_size[0],
                          bat.size[1]//2 / aft_bat_size[1]*pre_bat_size[1] - 106 * bat_delta])
    res3 = numpy.dot(Angle_matrix, Vector3)

    test = [bat.size[0]//2 + res3[0], bat.size[1]//2 - res3[1]]
    LocoBat = [int(center_eye[0] - (bat.size[0]//2 + res3[0])),
               int(center_eye[1] - (bat.size[1]//2 - res3[1]))]

    # DEBUGGING
    # print(Vector3)
    # print(res3)
    # print(test)
    # print(bat.size[0]//2, bat.size[1]//2)
    # d = ImageDraw.Draw(bat, 'RGBA')
    # d.point(center_eye, fill=(150, 0, 0))
    # d.ellipse((test[0] - 5, test[1] - 5, test[0] + 5,test[1] + 5), fill='#f00')
    pil_image.paste(bat, LocoBat, bat)
    result[0] = pil_image
    return


def Cry_filter(image, result):
    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    face_loco = face_recognition.face_locations(image)

    bat = Image.open('./Filter_image/cry.png')
    left_eye = numpy.array(face_landmarks_list[0]['left_eye'][0])
    right_eye = numpy.array(face_landmarks_list[0]['right_eye'][0])
    angle = math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
    bat_angle = -math.atan(angle) * 180 / math.pi
    bat_angle_rad = math.radians(bat_angle)
    Angle_matrix = numpy.array([[math.cos(bat_angle_rad), -math.sin(bat_angle_rad)], [
                               math.sin(bat_angle_rad), math.cos(bat_angle_rad)]])
    Vector1 = numpy.array([31 - bat.size[0]//2, bat.size[1]//2 - 151])
    Vector2 = numpy.array([706 - bat.size[0]//2, bat.size[1]//2 - 151])
    res1 = numpy.dot(Angle_matrix, Vector1)
    res2 = numpy.dot(Angle_matrix, Vector2)

    pre_bat_size = bat.size
    bat = bat.rotate(bat_angle, expand=True)
    aft_bat_size = bat.size
    bat_delta = (face_landmarks_list[0]['right_eye'][0][0] -
                 face_landmarks_list[0]['left_eye'][0][0])/(res2[0] - res1[0])
    bat = bat.resize(
        (int(bat.size[0] * bat_delta), int(bat.size[1] * bat_delta)))
    center_eye = [face_landmarks_list[0]['left_eye'][0][0] + (face_landmarks_list[0]['left_eye'][3][0] - face_landmarks_list[0]['left_eye'][0][0])/2,
                  face_landmarks_list[0]['left_eye'][0][1] + (face_landmarks_list[0]['left_eye'][3][1] - face_landmarks_list[0]['left_eye'][0][1])]

    pil_image = Image.fromarray(image)

    Vector3 = numpy.array([149 * bat_delta - bat.size[0]//2 / aft_bat_size[0]*pre_bat_size[0],
                          bat.size[1]//2 / aft_bat_size[1]*pre_bat_size[1] - 141 * bat_delta])
    res3 = numpy.dot(Angle_matrix, Vector3)

    test = [bat.size[0]//2 + res3[0], bat.size[1]//2 - res3[1]]
    LocoBat = [int(center_eye[0] - (bat.size[0]//2 + res3[0])),
               int(center_eye[1] - (bat.size[1]//2 - res3[1]))]

    # DEBUGGING
    # print(Vector3)
    # print(res3)
    # print(test)
    # print(bat.size[0]//2, bat.size[1]//2)
    # d = ImageDraw.Draw(bat, 'RGBA')
    # d.point(center_eye, fill=(150, 0, 0))
    # d.ellipse((test[0] - 5, test[1] - 5, test[0] + 5,test[1] + 5), fill='#f00')
    pil_image.paste(bat, LocoBat, bat)
    result[0] = pil_image
    return


def Tear_filter(image, result):
    # Load the jpg file into a numpy array
    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    face_loco = face_recognition.face_locations(image)

    bat = Image.open('./Filter_image/cry2.png')
    left_eye = numpy.array(face_landmarks_list[0]['left_eye'][0])
    right_eye = numpy.array(face_landmarks_list[0]['right_eye'][0])
    angle = math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
    bat_angle = -math.atan(angle) * 180 / math.pi
    bat_angle_rad = math.radians(bat_angle)
    Angle_matrix = numpy.array([[math.cos(bat_angle_rad), -math.sin(bat_angle_rad)], [
                               math.sin(bat_angle_rad), math.cos(bat_angle_rad)]])
    Vector1 = numpy.array([190 - bat.size[0]//2, bat.size[1]//2 - 212])
    Vector2 = numpy.array([722 - bat.size[0]//2, bat.size[1]//2 - 212])
    res1 = numpy.dot(Angle_matrix, Vector1)
    res2 = numpy.dot(Angle_matrix, Vector2)

    pre_bat_size = bat.size
    bat = bat.rotate(bat_angle, expand=True)
    aft_bat_size = bat.size
    bat_delta = (face_landmarks_list[0]['right_eye'][0][0] -
                 face_landmarks_list[0]['left_eye'][0][0])/(res2[0] - res1[0])
    print('angle: ', bat_angle)
    bat = bat.resize(
        (int(bat.size[0] * bat_delta), int(bat.size[1] * bat_delta)))
    center_eye = [face_landmarks_list[0]['left_eye'][0][0] + (face_landmarks_list[0]['left_eye'][3][0] - face_landmarks_list[0]['left_eye'][0][0])/2,
                  face_landmarks_list[0]['left_eye'][0][1] + (face_landmarks_list[0]['left_eye'][3][1] - face_landmarks_list[0]['left_eye'][0][1])]

    pil_image = Image.fromarray(image)

    Vector3 = numpy.array([230 * bat_delta - bat.size[0]//2 / aft_bat_size[0]*pre_bat_size[0],
                          bat.size[1]//2 / aft_bat_size[1]*pre_bat_size[1] - 282 * bat_delta])
    res3 = numpy.dot(Angle_matrix, Vector3)

    test = [bat.size[0]//2 + res3[0], bat.size[1]//2 - res3[1]]
    LocoBat = [int(center_eye[0] - (bat.size[0]//2 + res3[0])),
               int(center_eye[1] - (bat.size[1]//2 - res3[1]))]

    # DEBUGGING
    # print(Vector3)
    # print(res3)
    # print(test)
    # print(bat.size[0]//2, bat.size[1]//2)
    # d = ImageDraw.Draw(bat, 'RGBA')
    # d.point(center_eye, fill=(150, 0, 0))
    # d.ellipse((test[0] - 5, test[1] - 5, test[0] + 5,test[1] + 5), fill='#f00')
    pil_image.paste(bat, LocoBat, bat)
    result[0] = pil_image
    return


def Sharingan_filter(image, result):
    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    face_loco = face_recognition.face_locations(image)

    bat = Image.open('./Filter_image/sharingan.png')
    left_eye = numpy.array(face_landmarks_list[0]['left_eye'][0])
    right_eye = numpy.array(face_landmarks_list[0]['right_eye'][0])
    angle = math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
    bat_angle = -math.atan(angle) * 180 / math.pi
    bat_angle_rad = math.radians(bat_angle)
    Angle_matrix = numpy.array([[math.cos(bat_angle_rad), -math.sin(bat_angle_rad)], [
                               math.sin(bat_angle_rad), math.cos(bat_angle_rad)]])
    Vector1 = numpy.array([86 - bat.size[0]//2, bat.size[1]//2 - 70])
    Vector2 = numpy.array([360 - bat.size[0]//2, bat.size[1]//2 - 70])
    res1 = numpy.dot(Angle_matrix, Vector1)
    res2 = numpy.dot(Angle_matrix, Vector2)

    pre_bat_size = bat.size
    bat = bat.rotate(bat_angle, expand=True)
    aft_bat_size = bat.size
    bat_delta = (face_landmarks_list[0]['right_eye'][0][0] -
                 face_landmarks_list[0]['left_eye'][0][0])/(res2[0] - res1[0])
    print('angle: ', bat_angle)
    bat = bat.resize(
        (int(bat.size[0] * bat_delta), int(bat.size[1] * bat_delta)))
    center_eye = [face_landmarks_list[0]['left_eye'][0][0] + (face_landmarks_list[0]['left_eye'][3][0] - face_landmarks_list[0]['left_eye'][0][0])/2,
                  face_landmarks_list[0]['left_eye'][0][1] + (face_landmarks_list[0]['left_eye'][3][1] - face_landmarks_list[0]['left_eye'][0][1])]

    pil_image = Image.fromarray(image)

    Vector3 = numpy.array([135 * bat_delta - bat.size[0]//2 / aft_bat_size[0]*pre_bat_size[0],
                          bat.size[1]//2 / aft_bat_size[1]*pre_bat_size[1] - 72 * bat_delta])
    res3 = numpy.dot(Angle_matrix, Vector3)

    test = [bat.size[0]//2 + res3[0], bat.size[1]//2 - res3[1]]
    LocoBat = [int(center_eye[0] - (bat.size[0]//2 + res3[0])),
               int(center_eye[1] - (bat.size[1]//2 - res3[1]))]

    # DEBUGGING
    # print(Vector3)
    # print(res3)
    # print(test)
    # print(bat.size[0]//2, bat.size[1]//2)
    # d = ImageDraw.Draw(bat, 'RGBA')
    # d.point(center_eye, fill=(150, 0, 0))
    # d.ellipse((test[0] - 5, test[1] - 5, test[0] + 5,test[1] + 5), fill='#f00')
    pil_image.paste(bat, LocoBat, bat)
    result[0] = pil_image
    return


def SkiMask_filter(image, result):
    # Load the jpg file into a numpy array

    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    face_loco = face_recognition.face_locations(image)

    bat = Image.open('./Filter_image/skimask2.png')
    left_eye = numpy.array(face_landmarks_list[0]['left_eye'][0])
    right_eye = numpy.array(face_landmarks_list[0]['right_eye'][0])
    angle = math.atan2(right_eye[1] - left_eye[1],
                       right_eye[0] - left_eye[0])
    bat_angle = -math.atan(angle) * 180 / math.pi
    bat_angle_rad = math.radians(bat_angle)
    Angle_matrix = numpy.array([[math.cos(bat_angle_rad), -math.sin(bat_angle_rad)], [
        math.sin(bat_angle_rad), math.cos(bat_angle_rad)]])
    Vector1 = numpy.array([40 - bat.size[0]//2, bat.size[1]//2 - 190])
    Vector2 = numpy.array([161 - bat.size[0]//2, bat.size[1]//2 - 190])
    res1 = numpy.dot(Angle_matrix, Vector1)
    res2 = numpy.dot(Angle_matrix, Vector2)

    pre_bat_size = bat.size
    bat = bat.rotate(bat_angle, expand=True)
    aft_bat_size = bat.size
    bat_delta = (face_landmarks_list[0]['right_eye'][0][0] -
                 face_landmarks_list[0]['left_eye'][0][0])/(res2[0] - res1[0])
    print('angle: ', bat_angle)
    bat = bat.resize(
        (int(bat.size[0] * bat_delta), int(bat.size[1] * bat_delta)))
    center_eye = [face_landmarks_list[0]['left_eye'][0][0] + (face_landmarks_list[0]['left_eye'][3][0] - face_landmarks_list[0]['left_eye'][0][0])/2,
                  face_landmarks_list[0]['left_eye'][0][1] + (face_landmarks_list[0]['left_eye'][3][1] - face_landmarks_list[0]['left_eye'][0][1])]

    pil_image = Image.fromarray(image)

    Vector3 = numpy.array([74 * bat_delta - bat.size[0]//2 / aft_bat_size[0]*pre_bat_size[0],
                           bat.size[1]//2 / aft_bat_size[1]*pre_bat_size[1] - 201 * bat_delta])
    res3 = numpy.dot(Angle_matrix, Vector3)

    test = [bat.size[0]//2 + res3[0], bat.size[1]//2 - res3[1]]
    LocoBat = [int(center_eye[0] - (bat.size[0]//2 + res3[0])),
               int(center_eye[1] - (bat.size[1]//2 - res3[1]))]

    # DEBUGGING
    # print(Vector3)
    # print(res3)
    # print(test)
    # print(bat.size[0]//2, bat.size[1]//2)
    # d = ImageDraw.Draw(bat, 'RGBA')
    # d.point(center_eye, fill=(150, 0, 0))
    # d.ellipse((test[0] - 5, test[1] - 5, test[0] + 5,test[1] + 5), fill='#f00')
    pil_image.paste(bat, LocoBat, bat)
    result[0] = pil_image
    return


def Clown(image, result):
    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    face_loco = face_recognition.face_locations(image)

    clown = Image.open('./Filter_image/clown.png')
    clown_delta = (face_landmarks_list[0]['nose_tip'][4][0] - face_landmarks_list[0]['nose_tip'][0][0]) / clown.size[0]
    clown = clown.resize((int(clown.size[0] * clown_delta), int(clown.size[1] * clown_delta)))


    pil_image = Image.fromarray(image)
    LocoClown = list(face_landmarks_list[0]['nose_bridge'][3])
    LocoClown[0] -= int(clown.size[0]/2)
    LocoClown[1] -= int(clown.size[1]/2)

    for face_landmarks in face_landmarks_list:
        d = ImageDraw.Draw(pil_image, 'RGBA')

        # Apply some eyeliner
        # LEFT
        left_eye = face_landmarks['left_eye'][:4]
        left_eye.append(( (left_eye[1][0] + left_eye[2][0])//2, (left_eye[1][1] + left_eye[2][1])//2 - clown.size[1]//2 ))
        d.polygon(left_eye , fill=(0,128,128, 200), width=6)
        left_eye = face_landmarks['left_eye'][3:] + [face_landmarks['left_eye'][0]]
        left_eye.append(( (left_eye[1][0] + left_eye[2][0])//2, (left_eye[1][1] + left_eye[2][1])//2 + clown.size[1]//2 ))
        d.polygon(left_eye , fill=(0,128,128, 200), width=6)

        # RIGHT
        right_eye = face_landmarks['right_eye'][:4]
        right_eye.append(( (right_eye[1][0] + right_eye[2][0])//2, (right_eye[1][1] + right_eye[2][1])//2 - clown.size[1]//2 ))
        d.polygon(right_eye, fill=(0,128,128, 200), width=6)
        right_eye = face_landmarks['right_eye'][3:] + [face_landmarks['right_eye'][0]]
        right_eye.append(( (right_eye[1][0] + right_eye[2][0])//2, (right_eye[1][1] + right_eye[2][1])//2 + clown.size[1]//2 ))
        d.polygon(right_eye, fill=(0,128,128, 200), width=6)

        # Make the eyebrows into a nightmare
        d.polygon(face_landmarks['left_eyebrow'], fill=(210, 4, 45, 250))
        d.polygon(face_landmarks['right_eyebrow'], fill=(210, 4, 45, 250))
        d.line(face_landmarks['left_eyebrow'], fill=(210, 4, 45, 200), width=8)
        d.line(face_landmarks['right_eyebrow'], fill=(210, 4, 45, 200), width=8)

        # Gloss the lips
        toplip =face_landmarks['top_lip']
        # toplip[0] = (toplip[0][0] - clown.size[0]//2, toplip[0][1])
        # toplip[6] = (toplip[6][0] + clown.size[0]//2, toplip[6][1])
        d.polygon(toplip, fill=(210, 4, 45, 200))
        bottom_lip =face_landmarks['bottom_lip']
        # bottom_lip[0] = (bottom_lip[0][0] + clown.size[0]//2, bottom_lip[0][1])
        # bottom_lip[6] = (bottom_lip[6][0] - clown.size[0]//2, bottom_lip[6][1])
        d.polygon(bottom_lip, fill=(210, 4, 45, 200))
        # d.line(face_landmarks['top_lip'], fill=(210, 4, 45, 200), width=8)
        # d.line(face_landmarks['bottom_lip'], fill=(210, 4, 45, 200), width=8)

        # Sparkle the eyes
        d.polygon(face_landmarks['left_eye'], fill=(44,120,101, 30))
        d.polygon(face_landmarks['right_eye'], fill=(44,120,101, 30))

    pil_image.paste(clown, LocoClown, mask=clown)
    # pil_image = cv2.cvtColor(pil_image, cv2.COLOR_BGR2RGB) 
    result[0] = pil_image
    return