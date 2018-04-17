from PIL import Image
import face_recognition
from io import BytesIO
import urllib.request as urllib
from base64 import decodestring
from resizeimage import resizeimage


def find_best_match(event_users, image):
    # decode the image
    image = decodestring(bytes(image, encoding='utf-8'))
    if compute_similarities(event_users, image):
        best_match = max(event_users, key = lambda user: user['score'])
        print(best_match['score'])
        return best_match
    else:
        "No face found!"
        return None

# player_other will have an additional field called 'score' post method-call
def compute_similarities(event_users, photo_target):
    photo_target = BytesIO(photo_target)
    resize = 0.25
    with Image.open(photo_target) as image:
        width, height = image.size
        imageB = resizeimage.resize_contain(image, [int(resize * width), int(resize * height)])
        imageB.save("imageB.png")
    unknown_picture = face_recognition.load_image_file("imageB.png")

    if len(face_recognition.face_encodings(unknown_picture)) > 0:
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
        for stored_user in event_users:
            url_stored = stored_user['userInfo']['photo']
            stored_file = BytesIO(urllib.urlopen(url_stored).read())
            with Image.open(stored_file) as image:
                width, height = image.size
                imageA = resizeimage.resize_contain(image, [int(resize * width), int(resize * height)])
                imageA.save("imageA.png")

            known_picture = face_recognition.load_image_file("imageA.png")
            known_face_encoding = face_recognition.face_encodings(known_picture)[0]

            distance = face_recognition.face_distance([known_face_encoding], unknown_face_encoding)[0]
            stored_user['score'] = 1-distance
        return True
    else:
        return False



