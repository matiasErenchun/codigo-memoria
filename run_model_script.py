import os
import cv2
import random
import asyncio
import requests
import threading
import websockets
import numpy as np
from queue import Queue
import concurrent.futures
from datetime import datetime

import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util


def preload_files_and_model(project, model):
    files_To_Run = ""
    paths_To_Run = ""
    labels = ""
    if model == 'effi-d2-6k':
        files_To_Run = {
            'PIPELINE_CONFIG': os.path.join(project + '/models/efficientdet-d2-6k/fine_tuned_model', 'pipeline.config'),
            'LABELMAP': os.path.join(project + '/models/efficientdet-d2-6k/label_map.pbtxt'),
        }
        paths_To_Run = {
            'CHECKPOINT_PATH': os.path.join(project + '/models/efficientdet-d2-6k/training'),
        }
        labels = [{'id': 1, 'name': 'ave_posada'}, {'id': 2, 'name': 'ave_tierra'}, {'id': 3, 'name': 'ave_volando'}]
        return files_To_Run, paths_To_Run, labels
    if model == 'retinaNet':
        files_To_Run = {
            'PIPELINE_CONFIG': os.path.join(project + '/models/ssd-retinanet/fine_tuned_model', 'pipeline.config'),
            'LABELMAP': os.path.join(project + '/models/ssd-retinanet/label_map.pbtxt'),
        }
        paths_To_Run = {
            'CHECKPOINT_PATH': os.path.join(project + '/models/ssd-retinanet/training'),
        }
        labels = [{'id': 1, 'name': 'ave_posada'}, {'id': 2, 'name': 'ave_volando'}]
        return files_To_Run, paths_To_Run, labels
    if model == 'effi-d2-10k':
        files_To_Run = {
            'PIPELINE_CONFIG': os.path.join(project + '/models/efficientdet-d2-10k/fine_tuned_model',
                                            'pipeline.config'),
            'LABELMAP': os.path.join(project + '/models/efficientdet-d2-10k/label_map.pbtxt'),
        }
        paths_To_Run = {
            'CHECKPOINT_PATH': os.path.join(project + '/models/efficientdet-d2-10k/training'),
        }
        labels = [{'id': 1, 'name': 'ave_posada'}, {'id': 2, 'name': 'ave_volando'}]
        return files_To_Run, paths_To_Run, labels
    if model == 'effi-d1-20k':
        files_To_Run = {
            'PIPELINE_CONFIG': os.path.join(project + '/models/efficientdet-d1-20k/fine_tuned_model',
                                            'pipeline.config'),
            'LABELMAP': os.path.join(project + '/models/efficientdet-d1-20k/label_map.pbtxt'),
        }
        paths_To_Run = {
            'CHECKPOINT_PATH': os.path.join(project + '/models/efficientdet-d1-20k/training'),
        }
        labels = [{'id': 1, 'name': 'ave_posada'}, {'id': 2, 'name': 'ave_volando'}]
        return files_To_Run, paths_To_Run, labels
    if model == 'effi-d3-10k':
        files_To_Run = {
            'PIPELINE_CONFIG': os.path.join(project + '/models/efficientdet-d3-20k/fine_tuned_model',
                                            'pipeline.config'),
            'LABELMAP': os.path.join(project + '/models/efficientdet-d3-20k/label_map.pbtxt'),
        }
        paths_To_Run = {
            'CHECKPOINT_PATH': os.path.join(project + '/models/efficientdet-d3-20k/training'),
        }
        labels = [{'id': 1, 'name': 'ave_posada'}, {'id': 2, 'name': 'ave_volando'}]
        return files_To_Run, paths_To_Run, labels
    if model == 'faster-rcnn':
        files_To_Run = {
            'PIPELINE_CONFIG': os.path.join(project + '/models/faster-rcnn/fine_tuned_model', 'pipeline.config'),
            'LABELMAP': os.path.join(project + '/models/faster-rcnn/label_map.pbtxt'),
        }
        paths_To_Run = {
            'CHECKPOINT_PATH': os.path.join(project + '/models/faster-rcnn/training'),
        }
        labels = [{'id': 1, 'name': 'ave_posada'}, {'id': 2, 'name': 'ave_volando'}]
        return files_To_Run, paths_To_Run, labels
    return files_To_Run, paths_To_Run, labels


project = 'BirdDetector'
actual_model = 'faster-rcnn'
current_ckpt = 'ckpt-10'

files_To_Run, paths_To_Run, labels = preload_files_and_model(project, actual_model)
# labels = [{'name':'pajaro', 'id':1}]

# Ruta donde se creará el archivo
# labelmap_path = files_To_Run['LABELMAP']
# print(labelmap_path)
# Si la ruta no existe, se crea

carpeta_proyecto = os.path.dirname(os.path.abspath(__file__))

archivo = files_To_Run['LABELMAP']
category_index = label_map_util.create_category_index_from_labelmap(
    files_To_Run['LABELMAP'])
# Verificar si el archivo existe en el directorio actual
if not os.path.isfile(archivo):
    # Si no existe, crear el archivo
    with open(archivo, 'a') as f:
        for label in labels:
            f.write('item { \n')
            f.write('\tname:\'{}\'\n'.format(label['name']))
            f.write('\tid:{}\n'.format(label['id']))
            f.write('}\n')
    print(f'Se creó el archivo {archivo}')
else:
    print(f'El archivo {archivo} ya existe en el directorio actual')

print(f"label map path:files_To_Run['LABELMAP']")
# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files_To_Run['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths_To_Run['CHECKPOINT_PATH'], current_ckpt)).expect_partial()


@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


def process_imagen(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image_np = cv2.resize(img_np, (1920, 1080))
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections['detection_boxes'],
        detections['detection_classes'] + label_id_offset,
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=5,
        min_score_thresh=.2,
        agnostic_mode=False)
    return detections, image_np_with_detections


def precharge_model(barrier):
    """
        esta funcion esta encargada de precargar el modelo de deteccion antes de iuniciar el servidor,
         asi el mdoelo comieza aprocesar imagenes apenas se hace una coneccion .

        Args:
            parametro (wait): se recibe el barrier correrspondiente para una vez el model esta cargado permitir
            que inicialise y carge el resto del sistema.
        """
    img = cv2.imread('posada.jpg')
    if img is None:
        print("erro de carga d eimagen")
    else:
        _, img_encoded = cv2.imencode('.jpg', img)
        image_charge = np.array(img_encoded).tobytes()
        detections, image_np_with_detections = process_imagen(image_charge)
        print(detections['detection_classes'])
        print("charge model ready")
    barrier.wait()


def image_processor(barrier, image_queue, detections_queue):
    barrier.wait()
    while True:
        try:
            # Envía mensajes al servidor
            data = image_queue.get(timeout=5)
            image_data = data['image']
            time_str = data['time']
            randomm = data['random']
            print("time: " + str(time_str))
            detections, image_np_with_detections = process_imagen(image_data)
            nombre_imagen = str(randomm) + '-' + str(time_str) + '.jpg'
            ruta_destino = os.path.join(carpeta_proyecto, "capturas", nombre_imagen)
            data = {'detection_classes': detections['detection_classes'],
                    'detection_scores': detections['detection_scores'], 'ruta_destino': ruta_destino,
                    'image': image_np_with_detections}
            detections_queue.put(data)
        except Exception:
            print(" ESperando imagenes para procesar")


def detections_processor(detections_queue, detections_barrier, score, target):
    detections_barrier.wait()
    while True:
        try:
            # Envía mensajes al servidor
            data = detections_queue.get(timeout=5)
            detection_classes = data['detection_classes']
            detection_scores = data['detection_scores']
            ruta = data['ruta_destino']
            img_np = data['image']
            i = 0
            keep_looking = True
            print(detection_scores)
            print(detection_classes)
            while detection_scores[i] >= score:
                if detection_classes[i] == target:
                    keep_looking = False
                    print(f"detection class: {detection_classes[i]}, score: {detection_scores[i]}")
                    cv2.imwrite(ruta, img_np)
                i += 1
        except Exception as e:
            print("detection Exception")
            print(f"Se produjo una excepción: {e}")


async def websocket_handler(websocket, path, barrier, images_queue):
    # Se ejecuta cuando se establece una conexión websocket
    print("Conexión establecida.")
    barrier.wait()
    try:
        while True:
            # Recibir datos del cliente
            data = await websocket.recv()

            received_data = eval(data)

            print(f"dandom value:{received_data['random']}")
            images_queue.put(received_data)
            # Enviar una respuesta al cliente
            response = "Respuesta del servidor"
            # await websocket.send(response)
            print(f"Respuesta enviada: {response}")

    except websockets.exceptions.ConnectionClosedOK:
        # La conexión websocket se ha cerrado de forma normal
        print("Conexión cerrada.")

    except websockets.exceptions.ConnectionClosedError as e:
        # La conexión websocket se ha cerrado con un error
        print(f"Error al cerrar la conexión: {e}")
    except Exception as e:
        print(f"Error {e}")


images_queue = Queue()
barrier = threading.Barrier(1)

max_workers = 1
detections_queue = Queue()
detections_barrier = threading.Barrier(max_workers + 1)
score = float(0.2)
target = 0
thread = threading.Thread(target=image_processor, args=(barrier, images_queue, detections_queue))
thread.start()

precharge_model(barrier)
# Crear el servidor websocket
start_server = websockets.serve(
    lambda websocket, path: websocket_handler(websocket, path, barrier, images_queue),
    "172.22.38.152",
    8765,
    max_size=2 ** 25
)

processor_threads = []
for _ in range(max_workers):
    processor_thread = threading.Thread(target=detections_processor,
                                        args=(detections_queue, detections_barrier, score, target))
    processor_thread.start()
    processor_threads.append(processor_thread)

detections_barrier.wait()
# Iniciar el bucle de eventos de asyncio
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

thread.join()
for processor_thread in processor_threads:
    processor_thread.join()