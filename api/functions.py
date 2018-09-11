import face_recognition

def find(image , path):
    faces = face_recognition.load_image_file(path)
    known_image = face_recognition.face_encodings(faces)
    size = len(face_recognition.face_encodings(image))
    
    if (size > 0):
        unknown_image = face_recognition.face_encodings(image)[0]
        distance =face_recognition.face_distance(known_image, unknown_image)[0]
        if(distance >= 0.435 and distance < 0.499):
            global PROBABLY_FACE
            PROBABLY_FACE = path
        if (distance < 0.435):
            dict = {
                'flag' : True,
                'distance' : distance
            }
            return dict
        else:
            dict = {
                'flag' : False,
                'distance' : distance
            }
            return dict
        return (face_recognition.compare_faces(known_image, unknown_image)[0])
    else:
        global NO_FACES
        NO_FACES = 1
        print("array size is equal to 0")
        dict = {
            'flag' : False,
            'distance' : 0
        }
        return dict
        