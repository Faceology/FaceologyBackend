from PIL import Image
import face_recognition
from io import BytesIO
import urllib.request as urllib
from base64 import decodestring


def find_best_match(event_users, image):
    # decode the image
    image = decodestring(bytes(image, encoding='utf-8'))
    scored_users = list(map(lambda user: compute_similarity(user, image), event_users))
    best_match = max(scored_users, key = lambda user: user['score'])
    print(best_match['score'])
    return best_match

# player_other will have an additional field called 'score' post method-call
def compute_similarity(stored_user, photo_target):
    url_stored = stored_user['userInfo']['photo']
    stored_file = BytesIO(urllib.urlopen(url_stored).read())

    known_picture = face_recognition.load_image_file(stored_file)
    known_face_encoding = face_recognition.face_encodings(known_picture)[0]

    photo_target = BytesIO(photo_target)

    unknown_picture = face_recognition.load_image_file(photo_target)
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

    distance = face_recognition.face_distance([known_face_encoding], unknown_face_encoding)[0]
    stored_user['score'] = 1-distance
    return stored_user


