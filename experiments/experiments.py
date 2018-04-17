import face_recognition
import numpy as np
import os
import sys
from PIL import Image
from io import BytesIO
import urllib2
from base64 import decodestring
from resizeimage import resizeimage
import time

def transform_faces(img_path):
    for img_file in os.listdir(img_path):
        im = Image.open(img_path + img_file)
        # darker image
        im_dark = im.point(lambda p: p * 0.75)
        # lighter image
        im_light = im.point(lambda p: p * 1.25)

        im_dark.save(img_path + "dark" + img_file)
        im_light.save(img_path + "light" + img_file)

def process_sm(img_path):
    num_faces = []

    for img_file in os.listdir(img_path):
        try:
            image = face_recognition.load_image_file(img_path + img_file)
            num_faces.append(len(face_recognition.face_encodings(image)))
        except:
            continue

    orig_length = len(num_faces)
    num_faces = list(filter(lambda x: x !=0, num_faces))
    percent_passed = len(num_faces) / (1.0 * orig_length)
    print("Avg faces per picture " + str(np.mean(num_faces)))
    print("Percentage of passed detections " + str(percent_passed))

# image inputs should already be rotated
def process_orientation(img_path):
    num_left = []
    num_right = []
    num_front = []

    for img_file in os.listdir(img_path):
        print img_file[-5]
        try:
            image = face_recognition.load_image_file(img_path + img_file)
            if img_file[-5] == 'R':
                num_right.append(len(face_recognition.face_encodings(image)))
            elif img_file[-5] == 'L':
                num_left.append(len(face_recognition.face_encodings(image)))
            else:
                num_front.append(len(face_recognition.face_encodings(image)))
        except Exception as e:
            print e
            continue

    orig_length_right = len(num_right)
    orig_length_left = len(num_left)
    orig_length_front = len(num_front)

    num_right_faces = list(filter(lambda x: x !=0, num_right))
    num_left_faces = list(filter(lambda x: x !=0, num_left))
    num_front_faces = list(filter(lambda x: x !=0, num_front))

    percent_passed_right = len(num_right_faces) / (1.0 * orig_length_right)
    percent_passed_left = len(num_left_faces) / (1.0 * orig_length_left)
    percent_passed_front = len(num_front_faces) / (1.0 * orig_length_front)

    print("Avg faces per picture Right" + str(np.mean(num_right_faces)))
    print("Avg faces per picture Left" + str(np.mean(num_left_faces)))
    print("Avg faces per picture Front" + str(np.mean(num_front_faces)))
    print("Percentage of passed detections left" + str(percent_passed_left))
    print("Percentage of passed detections right" + str(percent_passed_right))
    print("Percentage of passed detections front" + str(percent_passed_front))


# image inputs are artificially transformed
def process_lighting(img_path):
    dark = []
    light = []
    regular = []
    distancesDark = []
    distancesLight = []
    for img_file in os.listdir(img_path):
        print img_file
        if img_file[0] == 'd':
            dark_img = face_recognition.load_image_file(img_path + img_file)
            dark.append(face_recognition.face_encodings(dark_img)[0])
        elif img_file[0] == 'l':
            light_img = face_recognition.load_image_file(img_path + img_file)
            light.append(face_recognition.face_encodings(light_img)[0])
        else:
            regular_img = face_recognition.load_image_file(img_path + img_file)
            regular.append(face_recognition.face_encodings(regular_img)[0])

    for i in range(len(regular)):
        light_dist = face_recognition.face_distance([regular[i]], light[i])[0]
        dark_dist = face_recognition.face_distance([regular[i]], dark[i])[0]
        distancesLight.append(1 - light_dist)
        distancesDark.append(1 - dark_dist)
    print distancesLight, distancesDark
    return distancesLight, distancesDark

    pass

def find_distance(url, photoB):
    start = time.time()
    stored_file = BytesIO(urllib2.urlopen(url).read())
    known_picture = face_recognition.load_image_file(stored_file)
    known_face_encoding = face_recognition.face_encodings(known_picture)[0]

    unknown_picture = face_recognition.load_image_file(photoB)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    distance = face_recognition.face_distance([known_face_encoding], unknown_face_encoding)[0]
    print time.time() - start
    return 1-distance

def test_size(url, photoB):
    distances = []
    times = []
    resizes = list(range(100, 10, -5))
    for resize in range(100, 10, -5):
        resize *= 0.01
        print resize
        start = time.time()
        stored_file = BytesIO(urllib2.urlopen(url).read())
        with Image.open(stored_file) as image:
            width, height = image.size
            imageA = resizeimage.resize_contain(image, [int(resize * width), int(resize * height)])
            imageA.save("imageA.png")

        with Image.open(photoB) as image:
            width, height = image.size
            imageB = resizeimage.resize_contain(image, [int(resize * width), int(resize * height)])
            imageB.save("imageB.png")

        try:
            known_picture = face_recognition.load_image_file("imageA.png")
            known_face_encoding = face_recognition.face_encodings(known_picture)[0]

            unknown_picture = face_recognition.load_image_file("imageB.png")
            unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

            score = face_recognition.face_distance([known_face_encoding], unknown_face_encoding)[0]
            print 1-score
            print (time.time() - start)
            distances.append(1-score)
            times.append(time.time() - start)
        except:
            break
    print distances
    print times
    print resizes
    return (distances, times, resizes)

def main():
    # social media source comparison
    #process_sm('linkedin_imgs/')
    #process_sm('fb_imgs/')

    # tianyi orientation comparison
    #print(find_distance('tianyi/tianyi_f.jpg', 'tianyi/tianyi_l.jpg'))
    #print(find_distance('tianyi/tianyi_f.jpg', 'tianyi/tianyi_r.jpg'))

    # test sizes
    print(test_size('https://media.licdn.com/dms/image/C4E04AQFRRmVw-PTV2g/profile-originalphoto-shrink_450_600/0?e=1528833600&v=beta&t=ox4R_Mh81Cal_nrxlsQwWPi9ZCCyng_rFInrUEzEkII', 'tianyi/tianyi_f.jpg'))
    #print find_distance('https://media.licdn.com/dms/image/C4E04AQFRRmVw-PTV2g/profile-originalphoto-shrink_450_600/0?e=1528833600&v=beta&t=ox4R_Mh81Cal_nrxlsQwWPi9ZCCyng_rFInrUEzEkII', 'tianyi/tianyi_f.jpg')

    # NIST orientation comparison
    #process_orientation('mug_imgs/')

    # test lighting
    # transform_faces('linkedin_imgs/')
    #process_lighting('linkedin_imgs/')
    pass

main()


