import face_recognition
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import PIL

def face_analyzer(FILE_NAME):
    lif=face_recognition.load_image_file(FILE_NAME)
    face_locations = face_recognition.face_locations(lif,model="hog")
    face_embeddings=[]
    distances_text=""
    for top, right, bottom, left in face_locations:
        face_image=lif[top:bottom, left:right]
        face_embeddings.append(face_recognition.face_encodings(face_image))
    if len(face_locations)>=2:
        for i in range(len(face_embeddings)-1):
            if face_embeddings[i]==[]:
                continue
            for j in range(i+1,len(face_embeddings)):
                if face_embeddings[j]==[]:
                    continue
                face_sim=1-face_recognition.face_distance([face_embeddings[i][0]],face_embeddings[j][0])[0]      
                distances_text+=f"Face {i+1} simmilarity to face {j+1}: {100*face_sim:.1f}% <br>"

    fig,ax = plt.subplots(1)
    ax.imshow(lif)
    for pic_nr, (top, right, bottom, left) in enumerate(face_locations):
        rect = patches.Rectangle((left,bottom),(right-left),(top-bottom),linewidth=1,edgecolor='r',facecolor='none')
        ax.add_patch(rect)
        ax.annotate(pic_nr+1,(left+20, bottom-20), size=18, color="r")
    plt.axis('off')
    new_name=FILE_NAME.split("/")
    new_name[-2]="annotated"
    new_name="/".join(new_name)
    plt.savefig(new_name, dpi=900)
    return distances_text