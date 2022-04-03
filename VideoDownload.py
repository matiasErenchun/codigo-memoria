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
    except:
        print("error al tratar de descargar el video")


def transfor_video_to_image():
    path_videos = "D:\\videosRecolectados"
    patdestino = "D:\\framesdevideorecolectado\\"
    path = os.path.join(path_videos)
    for video in os.listdir(path):
        try:
            pathvideo = os.path.join(path, video)
            videocaptura = cv2.VideoCapture(pathvideo)
            print("nombre video:" + video)
            count =0
            while(videocaptura.isOpened()):
                os.path.join(patdestino)
                ret, frame = videocaptura.read()
                if(ret== True and count%25 == 0):
                    cv2.imwrite(patdestino + 'img-%05d.jpg' % count, frame)
                    if(cv2.waitKey(1) == ord('s')):
                        break
                elif(not ret):
                    break
                count+=1
        except:
            print("error al abrir el video")
    print("eso es to, eso es to, eso es todo amigos")





menu = '''
si desea descargar un video ingrese un numero entero positivo si desea salir ingrese 0:
'''
print(menu)
valor = int(input("ingrese la opcion: "))
while (valor > 0):
    url = str(input("ingrese la url del video"))
    descargarVideo(url)
    print(menu)
    valor = int(input("ingrese la opcion: "))
print("bye bye bro")
transfor_video_to_image()