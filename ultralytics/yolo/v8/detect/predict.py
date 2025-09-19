# Ultralytics YOLO 🚀, GPL-3.0 license

import hydra
import torch
import argparse
import time
from pathlib import Path
import math
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
from ultralytics.yolo.engine.predictor import BasePredictor
from ultralytics.yolo.utils import DEFAULT_CONFIG, ROOT, ops
from ultralytics.yolo.utils.checks import check_imgsz
from ultralytics.yolo.utils.plotting import Annotator, colors, save_one_box

import cv2
# from ultralytics.yolo.v8.detect.deep_sort_pytorch.utils.parser import get_config
# from ultralytics.yolo.v8.detect.deep_sort_pytorch.deep_sort import DeepSort
from collections import deque
import numpy as np
import sys
import os

# Importar configurações de contagem
config_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'config')
if config_path not in sys.path:
    sys.path.append(config_path)

try:
    from counting_config import *
    print("Configurações de contagem carregadas com sucesso!")
except ImportError:
    print("Arquivo de configuração não encontrado. Usando configurações padrão.")
    # Configurações padrão
    COUNTING_LINE = [(100, 500), (1050, 500)]
    ROI_AREA = [(50, 100), (1200, 600)]
    ENABLE_ROI = True
    CROSSING_THRESHOLD = 10
    COUNTING_DIRECTION = 'both'
    VEHICLE_CLASSES = [2, 3, 5, 7, 8]
    LINE_COLOR = (0, 255, 0)
    ROI_COLOR = (255, 255, 0)
    LINE_THICKNESS = 3
    SHOW_COUNTERS = True
    COUNTER_POSITION = (20, 50)
    PIXELS_PER_METER = 8
    SPEED_TIME_WINDOW = 15
    MIN_CONFIDENCE = 0.5
    MIN_OBJECT_SIZE = (30, 30)
    TRACKING_BUFFER = 30

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)
data_deque = {}

deepsort = None

object_counter = {}
object_counter1 = {}

# Usar configuração carregada do arquivo
line = COUNTING_LINE

speed_line_queue = {}

def estimatespeed(location1, location2):
    d_pixel = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    # Usar pixels por metro da configuração
    ppm = PIXELS_PER_METER
    d_meters = d_pixel/ppm
    time_constant = SPEED_TIME_WINDOW * 3.6
    
    speed = d_meters * time_constant
    return int(speed)

def apply_roi(frame, roi_area):
    """Aplicar ROI (Region of Interest) ao frame"""
    if not ENABLE_ROI:
        return frame
    
    # Criar máscara
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.rectangle(mask, roi_area[0], roi_area[1], 255, -1)
    
    # Aplicar máscara
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return result

def draw_roi(frame, roi_area, color=(255, 255, 0)):
    """Desenhar ROI no frame"""
    if ENABLE_ROI:
        cv2.rectangle(frame, roi_area[0], roi_area[1], color, 2)
        cv2.putText(frame, "ROI", (roi_area[0][0], roi_area[0][1] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    return frame

def is_in_roi(bbox, roi_area):
    """Verificar se o objeto está dentro da ROI"""
    if not ENABLE_ROI:
        return True
    
    # Centro do objeto
    center_x = int((bbox[0] + bbox[2]) / 2)
    center_y = int((bbox[1] + bbox[3]) / 2)
    
    # Verificar se está dentro da ROI
    return (roi_area[0][0] <= center_x <= roi_area[1][0] and 
            roi_area[0][1] <= center_y <= roi_area[1][1])
    

def init_tracker():
    # Função desabilitada temporariamente para evitar problemas com DeepSORT
    # global deepsort
    # cfg_deep = get_config()
    # cfg_deep.merge_from_file("ultralytics/yolo/v8/detect/deep_sort_pytorch/configs/deep_sort.yaml")
    # deepsort = DeepSort(cfg_deep.DEEPSORT.REID_CKPT,
    #                     max_dist=cfg_deep.DEEPSORT.MAX_DIST, min_confidence=cfg_deep.DEEPSORT.MIN_CONFIDENCE,
    #                     nms_max_overlap=cfg_deep.DEEPSORT.NMS_MAX_OVERLAP,
    #                     max_iou_distance=cfg_deep.DEEPSORT.MAX_IOU_DISTANCE,
    #                     max_age=cfg_deep.DEEPSORT.MAX_AGE, n_init=cfg_deep.DEEPSORT.N_INIT,
    #                     nn_budget=cfg_deep.DEEPSORT.NN_BUDGET,
    #                     use_cuda=True)
    pass


##########################################################################################
def xyxy_to_xywh(*xyxy):
    """" Calculates the relative bounding box from absolute pixel values. """
    bbox_left = min([xyxy[0].item(), xyxy[2].item()])
    bbox_top = min([xyxy[1].item(), xyxy[3].item()])
    bbox_w = abs(xyxy[0].item() - xyxy[2].item())
    bbox_h = abs(xyxy[1].item() - xyxy[3].item())
    x_c = (bbox_left + bbox_w / 2)
    y_c = (bbox_top + bbox_h / 2)
    w = bbox_w
    h = bbox_h
    return x_c, y_c, w, h


def xyxy_to_tlwh(bbox_xyxy):
    tlwh_bboxs = []
    for i, box in enumerate(bbox_xyxy):
        x1, y1, x2, y2 = [int(i) for i in box]
        top = x1
        left = y1
        w = int(x2 - x1)
        h = int(y2 - y1)
        tlwh_obj = [top, left, w, h]
        tlwh_bboxs.append(tlwh_obj)
    return tlwh_bboxs


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    if label == 0:  # person
        color = (85, 45, 255)
    elif label == 2:  # Car
        color = (222, 82, 175)
    elif label == 3:  # Motobike
        color = (0, 204, 255)
    elif label == 5:  # Bus
        color = (0, 149, 255)
    else:
        color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2
    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

    cv2.rectangle(img, (x1 + r, y1), (x2 - r, y2), color, -1, cv2.LINE_AA)
    cv2.rectangle(img, (x1, y1 + r), (x2, y2 - r - d), color, -1, cv2.LINE_AA)

    cv2.circle(img, (x1 + r, y1 + r), 2, color, 12)
    cv2.circle(img, (x2 - r, y1 + r), 2, color, 12)
    cv2.circle(img, (x1 + r, y2 - r), 2, color, 12)
    cv2.circle(img, (x2 - r, y2 - r), 2, color, 12)

    return img


def UI_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]

        img = draw_border(img, (c1[0], c1[1] - t_size[1] - 3), (c1[0] + t_size[0], c1[1] + 3), color, 1, 8, 2)

        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def get_direction(point1, point2):
    direction_str = ""

    # calculate y axis direction
    if point1[1] > point2[1]:
        direction_str += "South"
    elif point1[1] < point2[1]:
        direction_str += "North"
    else:
        direction_str += ""

    # calculate x axis direction
    if point1[0] > point2[0]:
        direction_str += "East"
    elif point1[0] < point2[0]:
        direction_str += "West"
    else:
        direction_str += ""

    return direction_str


def draw_boxes(img, bbox, names, object_id, identities=None, offset=(0, 0)):
    cv2.line(img, line[0], line[1], (46, 162, 112), 3)

    height, width, _ = img.shape
    # remove tracked point from buffer if object is lost
    for key in list(data_deque):
        if key not in identities:
            data_deque.pop(key)

    for i, box in enumerate(bbox):
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]

        # code to find center of bottom edge
        center = (int((x2 + x1) / 2), int((y2 + y2) / 2))

        # get ID of object
        id = int(identities[i]) if identities is not None else 0

        # create new buffer for new object
        if id not in data_deque:
            data_deque[id] = deque(maxlen=64)
        color = compute_color_for_labels(object_id[i])
        obj_name = names[object_id[i]]
        label = '{}{:d}'.format("", id) + ":" + '%s' % (obj_name)

        # add center to buffer
        data_deque[id].appendleft(center)
        if len(data_deque[id]) >= 2:
            direction = get_direction(data_deque[id][0], data_deque[id][1])
            object_speed = estimatespeed(data_deque[id][1], data_deque[id][0])
            speed_line_queue[id].append(object_speed)
            if intersect(data_deque[id][0], data_deque[id][1], line[0], line[1]):
                cv2.line(img, line[0], line[1], (255, 255, 255), 3)
                if "South" in direction:
                    if obj_name not in object_counter:
                        object_counter[obj_name] = 1
                    else:
                        object_counter[obj_name] += 1
                if "North" in direction:
                    if obj_name not in object_counter1:
                        object_counter1[obj_name] = 1
                    else:
                        object_counter1[obj_name] += 1
        try:
            label = label + "" + str(sum(speed_line_queue[id])//len(speed_line_queue[id])) + "km/h"
        except:
            pass
        UI_box(box, img, label=label, color=color, line_thickness=2)
        # draw trail
        for i in range(1, len(data_deque[id])):
            # check if on buffer value is none
            if data_deque[id][i - 1] is None or data_deque[id][i] is None:
                continue
            # generate dynamic thickness of trails
            thickness = int(np.sqrt(64 / float(i + i)) * 1.5)
            # draw trails
            cv2.line(img, data_deque[id][i - 1], data_deque[id][i], color, thickness)

        # 4. Display Count in top right corner
        for idx, (key, value) in enumerate(object_counter1.items()):
            cnt_str = str(key) + ":" + str(value)
            cv2.line(img, (width - 500, 25), (width, 25), [85, 45, 255], 40)
            cv2.putText(img, f'Number of Vehicles Entering', (width - 500, 35), 0, 1, [225, 255, 255], thickness=2,
                        lineType=cv2.LINE_AA)
            cv2.line(img, (width - 150, 65 + (idx * 40)), (width, 65 + (idx * 40)), [85, 45, 255], 30)
            cv2.putText(img, cnt_str, (width - 150, 75 + (idx * 40)), 0, 1, [255, 255, 255], thickness=2,
                        lineType=cv2.LINE_AA)

        for idx, (key, value) in enumerate(object_counter.items()):
            cnt_str1 = str(key) + ":" + str(value)
            cv2.line(img, (20, 25), (500, 25), [85, 45, 255], 40)
            cv2.putText(img, f'Numbers of Vehicles Leaving', (11, 35), 0, 1, [225, 255, 255], thickness=2,
                        lineType=cv2.LINE_AA)
            cv2.line(img, (20, 65 + (idx * 40)), (127, 65 + (idx * 40)), [85, 45, 255], 30)
            cv2.putText(img, cnt_str1, (11, 75 + (idx * 40)), 0, 1, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)

    return img


class DetectionPredictor(BasePredictor):

    def get_annotator(self, img):
        return Annotator(img, line_width=self.args.line_thickness, example=str(self.model.names))

    def preprocess(self, img):
        img = torch.from_numpy(img).to(self.model.device)
        img = img.half() if self.model.fp16 else img.float()  # uint8 to fp16/32
        img /= 255  # 0 - 255 to 0.0 - 1.0
        return img

    def postprocess(self, preds, img, orig_img):
        preds = ops.non_max_suppression(preds,
                                        self.args.conf,
                                        self.args.iou,
                                        agnostic=self.args.agnostic_nms,
                                        max_det=self.args.max_det)

        for i, pred in enumerate(preds):
            shape = orig_img[i].shape if self.webcam else orig_img.shape
            pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], shape).round()

        return preds

    def write_results(self, idx, preds, batch):
        p, im, im0 = batch
        all_outputs = []
        log_string = ""
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        self.seen += 1
        im0 = im0.copy()
        
        # Aplicar ROI se habilitado
        if ENABLE_ROI:
            im0 = draw_roi(im0, ROI_AREA, ROI_COLOR)
        
        if self.webcam:  # batch_size >= 1
            log_string += f'{idx}: '
            frame = self.dataset.count
        else:
            frame = getattr(self.dataset, 'frame', 0)

        self.data_path = p
        save_path = str(self.save_dir / p.name)  # im.jpg
        self.txt_path = str(self.save_dir / 'labels' / p.stem) + ('' if self.dataset.mode == 'image' else f'_{frame}')
        log_string += '%gx%g ' % im.shape[2:]  # print string
        self.annotator = self.get_annotator(im0)

        det = preds[idx]
        all_outputs.append(det)
        
        # Desenhar linha de contagem
        cv2.line(im0, COUNTING_LINE[0], COUNTING_LINE[1], LINE_COLOR, LINE_THICKNESS)
        cv2.putText(im0, "LINHA DE CONTAGEM", 
                   (COUNTING_LINE[0][0], COUNTING_LINE[0][1] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, LINE_COLOR, 2)
        
        if len(det) == 0:
            if SHOW_COUNTERS:
                im0 = draw_counting_info(im0)
            return log_string
            
        # Filtrar apenas classes de veículos configuradas
        vehicle_detections = []
        for *xyxy, conf, cls in reversed(det):
            if int(cls) in VEHICLE_CLASSES and conf >= MIN_CONFIDENCE:
                # Verificar se está na ROI
                bbox = [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])]
                if is_in_roi(bbox, ROI_AREA):
                    # Verificar tamanho mínimo
                    width = bbox[2] - bbox[0]
                    height = bbox[3] - bbox[1]
                    if width >= MIN_OBJECT_SIZE[0] and height >= MIN_OBJECT_SIZE[1]:
                        vehicle_detections.append([*xyxy, conf, cls])
        
        for c in det[:, 5].unique():
            if int(c) in VEHICLE_CLASSES:
                n = (det[:, 5] == c).sum()  # detections per class
                log_string += f"{n} {self.model.names[int(c)]}{'s' * (n > 1)}, "
        
        # Processar detecções de veículos
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        xywh_bboxs = []
        confs = []
        oids = []
        outputs = []
        
        for *xyxy, conf, cls in vehicle_detections:
            x_c, y_c, bbox_w, bbox_h = xyxy_to_xywh(*xyxy)
            xywh_obj = [x_c, y_c, bbox_w, bbox_h]
            xywh_bboxs.append(xywh_obj)
            confs.append([conf.item()])
            oids.append(int(cls))
            
            # Desenhar detecção
            label = f'{self.model.names[int(cls)]} {conf:.2f}'
            self.annotator.box_label(xyxy, label, color=colors(int(cls), True))
        
        if len(xywh_bboxs) > 0:
            xywhs = torch.Tensor(xywh_bboxs)
            confss = torch.Tensor(confs)

            # Processamento simplificado sem DeepSORT
            # Para cada detecção, verificar se cruza a linha
            for i, (*xyxy, conf, cls) in enumerate(vehicle_detections):
                center_x = int((xyxy[0] + xyxy[2]) / 2)
                center_y = int((xyxy[1] + xyxy[3]) / 2)
                
                # Verificar cruzamento da linha (simplificado)
                self.check_line_crossing(center_x, center_y, int(cls))
        
        # Desenhar informações de contagem
        if SHOW_COUNTERS:
            im0 = draw_counting_info(im0)
        
        # Desenhar anotações
        im0 = self.annotator.result()
        
        return log_string
    
    def check_line_crossing(self, center_x, center_y, class_id):
        """Verificar se o objeto cruzou a linha de contagem"""
        # Implementação simplificada de cruzamento de linha
        line_y = COUNTING_LINE[0][1]  # Assumindo linha horizontal
        
        # Criar ID único baseado na posição
        object_id = f"{center_x}_{center_y}_{class_id}"
        
        # Verificar se está próximo da linha
        if abs(center_y - line_y) <= CROSSING_THRESHOLD:
            class_name = self.model.names[class_id]
            
            if class_name not in object_counter:
                object_counter[class_name] = 0
            
            # Incrementar contador (lógica simplificada)
            # Em uma implementação real, seria necessário tracking para evitar contagem dupla
            if object_id not in speed_line_queue:
                speed_line_queue[object_id] = True
                object_counter[class_name] += 1
                print(f"Veículo detectado: {class_name} - Total: {object_counter[class_name]}")

def draw_counting_info(img):
    """Desenhar informações de contagem na imagem"""
    if not SHOW_COUNTERS:
        return img
    
    # Fundo para os contadores
    cv2.rectangle(img, (10, 10), (300, 30 + len(object_counter) * 30), (0, 0, 0), -1)
    
    # Título
    cv2.putText(img, "CONTAGEM DE VEICULOS", (15, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Contadores por classe
    y_offset = 60
    for idx, (class_name, count) in enumerate(object_counter.items()):
        text = f"{class_name}: {count}"
        cv2.putText(img, text, (15, y_offset + idx * 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    return img


@hydra.main(version_base=None, config_path=str(DEFAULT_CONFIG.parent), config_name=DEFAULT_CONFIG.name)
def predict(cfg):
    init_tracker()
    cfg.model = cfg.model or "yolov8n.pt"
    cfg.imgsz = check_imgsz(cfg.imgsz, min_dim=2)  # check image size
    cfg.source = cfg.source if cfg.source is not None else ROOT / "assets"
    predictor = DetectionPredictor(cfg)
    predictor()


if __name__ == "__main__":
    predict()
