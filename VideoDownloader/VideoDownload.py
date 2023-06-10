from pytube import YouTube
import os
import cv2
import traceback
import yt_dlp as youtube_dl


def descargarVideo():
    nombrevideo = str(input("ingrese nombredel video: "))
    nombrevideo = nombrevideo.replace(" ", "_")
    url = str(input("ingrese la url del video: "))
    url_destino = 'D:\\videosRecolectados\\' + nombrevideo + '.mp4'
    ydl_opts = {
        'outtmpl': url_destino
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def transfor_video_to_image():
    path_videos = "E:\\resposGit\\codigo-memoria\\VideoDownloader\\videos_recolectado"
    patdestino = "E:\\resposGit\\codigo-memoria\\VideoDownloader\\frames_recolectados\\"
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
                count = 0
                while (videocaptura.isOpened()):
                    os.path.join(patdestino)
                    ret, frame = videocaptura.read()
                    if (ret == True and count % 25 == 0):  # revisar como quedan los nombres
                        cv2.imwrite(midestino + video + 'img-%05d.jpg' % count, frame)
                        if (cv2.waitKey(1) == ord('s')):
                            break
                    elif (not ret):
                        break
                    count += 1
            else:
                print("la carpeta de" + video + " ya existe")
        except:
            print("error al abrir el video")
    print("eso es to, eso es to, eso es todo amigos")


def menu():
    print("ingrese una de las siguentes opciones:")
    print("0 para descargar un video")
    print("1 para tranformar un video, de la carpeta videos capturados, a fotogramas.")
    print("cualquier otro valor terminara el programa.")
    valor = int(input("ingrese la opcion: "))
    if valor == 0:
        descargarVideo()
    elif valor == 1:
        print("transformando")
        transfor_video_to_image()
    return valor


valor = menu()
while 0 <= valor <= 1:
    valor = menu()
print("bye bye ")
