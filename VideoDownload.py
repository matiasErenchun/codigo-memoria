import pytube
import os
import cv2


def descargarVideo(url):
    out_put_path = "D:\\videosRecolectados"
    url_video = url
    youtube = pytube.YouTube(url_video)
    print(youtube.title)
    try:
        youtube.streams.filter(progressive=True, file_extension="mp4") \
            .order_by('resolution') \
            .desc().first() \
            .download(
            output_path=out_put_path)
        print("se descargo: %s", youtube.title)
        namefiel=youtube.title+".mp4"
        return 1,namefiel
    except:
        print("error al tratar de descargar el video")
        return -1

def transfor_video_to_image():
    path_videos = "D:\\videosRecolectados"
    patdestino = "D:\\framesdevideorecolectado\\"
    path = os.path.join(path_videos)
    for video in os.listdir(path):
        try:
            pathvideo = os.path.join(path, video)
            videocaptura = cv2.VideoCapture(pathvideo)
            print("nombre video:" + video)
            mipath = os.path.join(patdestino, video + "\\")
            print(mipath)
            if not os.path.exists(mipath):
                print("no existe")
                os.mkdir(mipath)
                midestino = os.path.join(mipath)
                count =0
                while(videocaptura.isOpened()):
                    os.path.join(patdestino)
                    ret, frame = videocaptura.read()
                    if(ret== True and count%25 == 0):#revisar como quedan los nombres
                        cv2.imwrite(midestino + video + 'img-%05d.jpg' % count, frame)
                        if(cv2.waitKey(1) == ord('s')):
                            break
                    elif(not ret):
                        break
                    count+=1
            else:
                print("la carpeta de"+video+" ya existe")
        except:
            print("error al abrir el video")
    print("eso es to, eso es to, eso es todo amigos")

'''def transfor_video_to_image(video):
    path_videos = "D:\\videosRecolectados"
    patdestino = "D:\\framesdevideorecolectado\\"
    path = os.path.join(path_videos)
    try:
        pathvideo = os.path.join(path, video)
        videocaptura = cv2.VideoCapture(pathvideo)
        print("nombre video:" + video)
        mipath = os.path.join(patdestino, video+"\\")
        print(mipath)
        if not os.path.exists(mipath):
            print("no existe")
            os.mkdir(mipath)
        midestino = os.path.join(mipath)
        print("destino:"+midestino)
        count = 0
        videoCondition=videocaptura.isOpened()
        print("videoCondition:"+videoCondition)
        while videoCondition:
            os.path.join(mipath)
            ret, frame = videocaptura.read()
            if (ret == True and count%50 == 0):
                print("cortando" + midestino)
                status = cv2.imwrite(midestino + 'img-%05d.jpg' % count, frame)
                print("Image written to file-system : ", status)
                if cv2.waitKey(1) == ord('s'):
                    break
            elif not ret:
                print("terminado")
                break
            count += 1
    except:
        print("error al abrir el video")
    print("se termino de cortar el video:"+video)
'''

def menu():
    print("ingrese una de las siguentes opciones:")
    print("0 para descargar un vedeo y tranformarlo a fotogramas.")
    print("1 para tranformar un video, de la carpeta videos capturados, a fotogramas.")
    print("cualquier otro valor terminara el programa.")
    valor = int(input("ingrese la opcion: "))
    if valor == 0:
        url = str(input("ingrese la url del video"))
        respuesta, namefile = descargarVideo(url)
        if respuesta > 0:
            print(namefile)
            transfor_video_to_image()
    elif valor == 1:
        print("transformando")
        transfor_video_to_image()
    return valor


valor = menu()
while 0 <= valor <= 1:
    valor = menu()
print("bye bye ")
