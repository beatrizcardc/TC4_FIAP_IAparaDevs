# -*- coding: utf-8 -*-
"""TC4_v49.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EK22ucNZ6peJPpvYLBPeQ5ZmO7NJ6TWf

# 🌟 **Tech Challenge 4**

O **Tech Challenge** desta fase será a criação de uma aplicação que utilize **análise de vídeo**.  

O projeto deve incorporar as seguintes técnicas:  
🎯 **Reconhecimento facial**  
🎭 **Análise de expressões emocionais**  
🏃‍♂️ **Detecção de atividades em vídeos**  
📊 **Geração de resumo automático**

---

## 🚀 **A Proposta do Desafio**  

Você deverá criar uma aplicação a partir do vídeo disponível na plataforma do aluno, que execute as seguintes tarefas:  

### 1. **👤 Reconhecimento Facial**  
   - Identifique e marque os rostos presentes no vídeo.  

### 2. **😊 Análise de Expressões Emocionais**  
   - Analise as expressões emocionais dos rostos identificados.  

### 3. **🕺 Detecção de Atividades**  
   - Detecte e categorize as atividades sendo realizadas no vídeo.  

   **Atividades a serem detectadas:**  
   - ✋ **Mão esquerda levantada**  
   - ✋ **Mão direita levantada**  
   - 🙌 **Mãos levantadas**  
   - 💃 **Dançando**  
   - 🤝 **Aperto de mãos**  

### 4. **📄 Geração de Resumo**  
   - Crie um resumo automático das principais atividades e emoções detectadas no vídeo.  
   - Relatório gerado em formato `.txt` e exibido na tela com ícones e informações detalhadas.

---
"""

# 1. Instalar DeepFace e dependências essenciais
!pip install deepface opencv-python-headless retina-face

# 2. Atualizar pandas, tqdm, matplotlib para garantir compatibilidade
!pip install --upgrade pandas tqdm matplotlib

!pip install retina-face

!pip install mediapipe

!pip install deepface mediapipe moviepy tqdm opencv-python-headless

!pip install mtcnn

!pip install fer

!pip install tensorflow

#from google.colab import drive
#drive.mount('/content/drive')

!pip install tensorflow==2.9.1 keras==2.9.0
!pip install --upgrade deepface opencv-python-headless retina-face

"""Ajustando Reconhecimento Facial para precisão de evento únicos, sem pular Frames"""

!pip install --upgrade tensorflow deepface

!pip install tensorflow keras opencv-python-headless deepface

"""## 1. 👤 Reconhecimento Facial"""

import cv2
from deepface import DeepFace
from tqdm import tqdm
import os

# Configurando pasta de saída
output_dir = '/content/drive/MyDrive/Analise_Emocoes_TC4'
os.makedirs(output_dir, exist_ok=True)

# Função principal para reconhecimento facial no vídeo
def process_video_faces_only(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_video_path = os.path.join(output_dir, 'analisado35e_video_faces_only.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, original_fps, (original_width, original_height))

    unique_people_count = 0
    detected_people_history = set()  # Histórico de pessoas detectadas
    frame_threshold = 10  # Limite de frames para considerar uma nova detecção
    position_threshold = 10  # Limite de variação de posição para considerar o mesmo rosto

    with tqdm(total=total_frames, desc="Analisando vídeo") as pbar:
        frame_index = 0
        while cap.isOpened() and frame_index < total_frames:
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            print(f"Processando frame {frame_index}...")
            try:
                analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='retinaface')
                if isinstance(analysis, list):
                    analysis = analysis[0]  # Se for uma lista, pegar o primeiro rosto detectado
                faces = [analysis] if isinstance(analysis, dict) else analysis
            except Exception as e:
                # Salvar o frame problemático para inspeção
                problem_frame_path = os.path.join(output_dir, f'problem_frame_{frame_index}.jpg')
                cv2.imwrite(problem_frame_path, frame)
                print(f"Frame problemático salvo em: {problem_frame_path}")
                print(f"Erro ao analisar o frame {frame_index}: {e}")
                frame_index += 1
                continue

            if not faces:
                frame_index += 1
                continue

            current_frame_people = set()  # Pessoas detectadas neste frame
            for face in faces:
                if 'region' not in face:
                    continue
                box = face['region']
                x, y, w, h = box['x'], box['y'], box['w'], box['h']
                person_id = (x // position_threshold, y // position_threshold, w // position_threshold, h // position_threshold)  # Normalizando coordenadas para evitar múltiplas contagens do mesmo rosto
                current_frame_people.add(person_id)

                # Desenhar caixa delimitadora no rosto
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                label = f"Pessoa {len(detected_people_history) + 1}"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Atualizar histórico e contar pessoas únicas
            for person_id in current_frame_people:
                if person_id not in detected_people_history:
                    unique_people_count += 1
                    detected_people_history.add(person_id)

            out.write(frame)
            frame_index += 1
            pbar.update(1)

    cap.release()
    out.release()
    generate_faces_report(total_frames, unique_people_count)
    print(f"Vídeo processado e salvo em: {output_video_path}")

# Função para gerar relatório de reconhecimento facial
def generate_faces_report(total_frames, unique_people_count):
    report_path = os.path.join(output_dir, 'faces_recognition_report35e.txt')
    with open(report_path, 'w') as f:
        f.write("Resumo do Reconhecimento Facial\n\n")
        f.write(f"Total de frames analisados: {total_frames}\n")
        f.write(f"Total de pessoas únicas detectadas (eventos únicos): {unique_people_count}\n")
    print(f"Relatório gerado em: {report_path}")


# Caminho do vídeo de entrada
video_path = '/content/drive/MyDrive/Projeto_TechChallenge4/Unlocking Facial Recognition_ Diverse Activities Analysis.mp4'
process_video_faces_only(video_path)

"""## 2. 😊 Análise de Expressões Emocionais

## 3. 🕺 Detecção de Atividades
Detecte e categorize as atividades sendo realizadas no vídeo.

Atividades a serem detectadas:*

  - ✋ Mão esquerda levantada

  - ✋ Mão direita levantada

  - 🙌 Mãos levantadas

  - 💃 Dançando

  - 🤝 Aperto de mãos
  

## 4. 📄 Geração de Resumo

Restringindo DANÇA
shoulder_rotation:

A faixa foi ajustada de (0.5, 1.1) para (0.6, 1.0) para restringir o intervalo de rotação dos ombros.
Isso reduz falsos positivos, garantindo que a rotação detectada seja consistente com movimentos de dança.
shoulder_movement:

O limite foi aumentado de 0.25 para 0.3.
Isso significa que os ombros precisam se mover mais significativamente na vertical para serem considerados como parte da dança.
arm_movement:

O limite foi aumentado de 0.4 para 0.5.
Exige um movimento mais pronunciado dos braços em relação aos ombros para evitar a detecção de movimentos menores como dança.
"""

import cv2
import mediapipe as mp
from fer import FER
from tqdm import tqdm
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Inicializando MediaPipe Pose e FER
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=6, min_detection_confidence=0.5)  #aumentando nº de faces em cada frame para 6, estava 1
fer_detector = FER(mtcnn=True)


# Configurando saída
output_dir = '/content/drive/MyDrive/Analise_Emocoes_TC4'
os.makedirs(output_dir, exist_ok=True)

# Histórico para anomalias
emotion_history = []
anomaly_threshold = 5  # Limite de mudanças rápidas de emoções para considerar anomalia

def detect_activities(pose_results):
    """
    Detecta atividades corporais como mãos levantadas, dançando e aperto de mãos.
    """
    activities = []
    if pose_results.pose_landmarks:
        landmarks = pose_results.pose_landmarks.landmark
        left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        nose = landmarks[mp_pose.PoseLandmark.NOSE]  #adicionando para separar melhor mãos de rosto

        # Detectar mãos levantadas com ajustes para não detectar rosto como mão
        # Detectar mãos levantadas - critérios mais restritivos
        if (
            left_hand.y < left_shoulder.y and  # Mão acima do ombro
            abs(left_hand.x - left_shoulder.x) > 0.1 and  # Longe do ombro lateralmente
            abs(left_hand.x - nose.x) > 0.15  # Longe do centro do rosto
        ):
            activities.append("Mao esquerda levantada")

        if (
            right_hand.y < right_shoulder.y and  # Mão acima do ombro
            abs(right_hand.x - right_shoulder.x) > 0.1 and  # Longe do ombro lateralmente
            abs(right_hand.x - nose.x) > 0.15  # Longe do centro do rosto
        ):
            activities.append("Mao direita levantada")

        if (
            left_hand.y < left_shoulder.y and
            right_hand.y < right_shoulder.y and
            abs(left_hand.x - nose.x) > 0.15 and
            abs(right_hand.x - nose.x) > 0.15
        ):
            activities.append("Maos levantadas")

        # Detectar dança (movimento significativo do torso e ombros)
        shoulder_distance = abs(left_shoulder.x - right_shoulder.x)
        shoulder_movement = abs(left_shoulder.y - right_shoulder.y)
        arm_movement = max(abs(left_hand.x - left_shoulder.x), abs(right_hand.x - right_shoulder.x))
        shoulder_rotation = abs(left_shoulder.x - right_shoulder.x) / max(abs(left_shoulder.y - right_shoulder.y), 0.01)  # Evitar divisão por zero

        if (
            0.6 < shoulder_rotation < 1.0  # Critério mais restritivo para rotação razoável
            and (shoulder_movement > 0.3 or arm_movement > 0.5)  # Movimento significativo dos ombros ou braços
        ):
            activities.append("Dancando")

        # Detectar aperto de mãos (mãos próximas e alinhadas)
        if (
            abs(left_hand.x - right_hand.x) < 0.015  # Ajustado para maior precisão no eixo X 0.015 pega uma só atividade
            and abs(left_hand.y - right_hand.y) < 0.015  # Ajustado para maior precisão no eixo Y
            and abs(left_hand.z - right_hand.z) < 0.015  # Incluído profundidade para maior robustez
        ):
            activities.append("Aperto de maos")

    return activities

def analyze_emotion(frame):
    """
    Analisa emoções no frame usando FER e verifica por anomalias.
    """
    try:
        result = fer_detector.detect_emotions(frame)
        if result:
            emotions = result[0]['emotions']
            dominant_emotion = max(emotions, key=emotions.get)
            emotion_history.append(dominant_emotion)
            if len(emotion_history) > anomaly_threshold:
                emotion_history.pop(0)
                if len(set(emotion_history)) > 3:  # Muitas mudanças rápidas
                    return "Anomaly Detected"
            return dominant_emotion
        else:
            return "Not Detected"
    except Exception as e:
        print(f"Erro ao analisar emoções: {e}")
        return "Not Detected"

def add_text_with_background(frame, texts, font_size=1.0, font_thickness=2, bg_color=(200, 200, 200), text_color=(0, 0, 0), position=(10, 30), line_spacing=1.5):
    """
    Adiciona texto com fundo no frame usando OpenCV.
    """
    x, y = position
    for i, text in enumerate(texts):
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_size, font_thickness)
        text_width, text_height = text_size
        y_text = y + int(i * text_height * line_spacing)

        # Desenhar retângulo de fundo
        cv2.rectangle(frame, (x, y_text - text_height - 5), (x + text_width + 10, y_text + 5), bg_color, -1)
        # Adicionar texto
        cv2.putText(frame, text, (x + 5, y_text), cv2.FONT_HERSHEY_SIMPLEX, font_size, text_color, font_thickness, cv2.LINE_AA)
    return frame

def process_video_emotions_activities(video_path):
    """
    Processa vídeo, analisando emoções, atividades e detectando anomalias.
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_video_path = os.path.join(output_dir, 'final91_video_emotions_activities.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    events_summary = {
        'emotions': {},
        'activities': {},
        'unknown_emotions': 0,
        'anomalies': 0
    }

    last_emotion = None
    last_activities = set()

    with tqdm(total=total_frames, desc="Analisando vídeo") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            # Processando o frame para landmarks de pose
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_results = pose.process(frame_rgb)

            # Desenhando o esqueleto do Mediapipe no frame, se landmarks forem detectados
            if pose_results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

            # Analisar emoção
            emotion = analyze_emotion(frame)
            if emotion == "Anomaly Detected":
                events_summary['anomalies'] += 1
            elif emotion == "Not Detected":
                events_summary['unknown_emotions'] += 1
            elif emotion != last_emotion:
                events_summary['emotions'][emotion] = events_summary['emotions'].get(emotion, 0) + 1
                last_emotion = emotion

            # Detectar atividades
            activities = set(detect_activities(pose_results))
            if activities != last_activities:
                for activity in activities:
                    events_summary['activities'][activity] = events_summary['activities'].get(activity, 0) + 1
                last_activities = activities

            # Adicionar legendas
            texts = [f"Emotion: {emotion}", f"Activities: {', '.join(activities) if activities else 'None'}"]
            frame = add_text_with_background(frame, texts, font_size=1.0, font_thickness=2, bg_color=(200, 200, 200), text_color=(0, 0, 0), position=(10, 30), line_spacing=2.0)

            # Escrever o frame no vídeo de saída
            out.write(frame)
            pbar.update(1)

    cap.release()
    out.release()
    print(f"Vídeo processado e salvo em: {output_video_path}")

    generate_emotions_activities_report(total_frames, events_summary)


def generate_emotions_activities_report(total_frames, events_summary):
    """
    Gera relatório resumido de emoções, atividades e anomalias.
    """
    report_path = os.path.join(output_dir, 'emotions_activities_report91.txt')
    with open(report_path, 'w') as f:
        f.write("Resumo de Emoções, Atividades e Anomalias\n\n")
        f.write(f"Total de frames analisados: {total_frames}\n")
        f.write("Total de emoções detectadas (eventos únicos):\n")
        for emotion, count in events_summary['emotions'].items():
            f.write(f"  - {emotion}: {count}\n")
        f.write(f"Total de frames sem emoções detectadas: {events_summary['unknown_emotions']}\n")
        f.write(f"Total de anomalias detectadas: {events_summary['anomalies']}\n")
        f.write("Total de atividades detectadas (eventos únicos):\n")
        for activity, count in events_summary['activities'].items():
            f.write(f"  - {activity}: {count}\n")
    print(f"Relatório gerado em: {report_path}")

# Caminho do vídeo de entrada
video_path = '/content/drive/MyDrive/Analise_Emocoes_TC4/analisado35d_video_faces_only.mp4'
process_video_emotions_activities(video_path)

"""#Resumo de Emoções, Atividades e Anomalias

###📊 Total de frames analisados: 1109

😊 Total de emoções detectadas (eventos únicos):
  - 😐 Neutral: 33
  - 😢 Sad: 24
  - 😡 Angry: 17
  - 😨 Fear: 13
  - 😀 Happy: 23
  - 😲 Surprise: 14

❌ Total de frames sem emoções detectadas: 599

⚠️ Total de anomalias detectadas: 21

🏃‍♂️ Total de atividades detectadas (eventos únicos):
  - 💃 Dançando: 1
  - ✋ Mão esquerda levantada: 10
  - 🙌 Mãos levantadas: 5
  - 🤚 Mão direita levantada: 6
  - 🤝 Aperto de mãos: 1
#

## 🎥 Frames Totais
"""

import cv2
import mediapipe as mp
from fer import FER
from tqdm import tqdm
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Inicializando MediaPipe Pose e FER
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=6, min_detection_confidence=0.5)  #aumentando nº de faces em cada frame para 6, estava 1
fer_detector = FER(mtcnn=True)


# Configurando saída
output_dir = '/content/drive/MyDrive/Analise_Emocoes_TC4'
os.makedirs(output_dir, exist_ok=True)

# Histórico para anomalias
emotion_history = []
anomaly_threshold = 5  # Limite de mudanças rápidas de emoções para considerar anomalia

def detect_activities(pose_results):
    """
    Detecta atividades corporais como mãos levantadas, dançando e aperto de mãos.
    """
    activities = []
    if pose_results.pose_landmarks:
        landmarks = pose_results.pose_landmarks.landmark
        left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        nose = landmarks[mp_pose.PoseLandmark.NOSE]  #adicionando para separar melhor mãos de rosto

        # Detectar mãos levantadas com ajustes para não detectar rosto como mão
        # Detectar mãos levantadas - critérios mais restritivos
        if (
            left_hand.y < left_shoulder.y and  # Mão acima do ombro
            abs(left_hand.x - left_shoulder.x) > 0.1 and  # Longe do ombro lateralmente
            abs(left_hand.x - nose.x) > 0.15  # Longe do centro do rosto
        ):
            activities.append("Mao esquerda levantada")

        if (
            right_hand.y < right_shoulder.y and  # Mão acima do ombro
            abs(right_hand.x - right_shoulder.x) > 0.1 and  # Longe do ombro lateralmente
            abs(right_hand.x - nose.x) > 0.15  # Longe do centro do rosto
        ):
            activities.append("Mao direita levantada")

        if (
            left_hand.y < left_shoulder.y and
            right_hand.y < right_shoulder.y and
            abs(left_hand.x - nose.x) > 0.15 and
            abs(right_hand.x - nose.x) > 0.15
        ):
            activities.append("Maos levantadas")

        # Detectar dança mais restritivo (movimento significativo do torso e ombros)
        shoulder_distance = abs(left_shoulder.x - right_shoulder.x)
        shoulder_movement = abs(left_shoulder.y - right_shoulder.y)
        arm_movement = max(abs(left_hand.x - left_shoulder.x), abs(right_hand.x - right_shoulder.x))
        shoulder_rotation = abs(left_shoulder.x - right_shoulder.x) / max(abs(left_shoulder.y - right_shoulder.y), 0.01)  # Evitar divisão por zero

        if (
            0.6 < shoulder_rotation < 1.0  # Critério mais restritivo para rotação razoável
            and (shoulder_movement > 0.3 or arm_movement > 0.5)  # Movimento significativo dos ombros ou braços
        ):
            activities.append("Dancando")

        # Detectar aperto de mãos (mãos próximas e alinhadas)
        if (
            abs(left_hand.x - right_hand.x) < 0.015  # Ajustado para maior precisão no eixo X 0.015 pega uma só atividade
            and abs(left_hand.y - right_hand.y) < 0.015  # Ajustado para maior precisão no eixo Y
            and abs(left_hand.z - right_hand.z) < 0.015  # Incluído profundidade para maior robustez
        ):
            activities.append("Aperto de maos")

    return activities

def analyze_emotion(frame):
    """
    Analisa emoções no frame usando FER e verifica por anomalias.
    """
    try:
        result = fer_detector.detect_emotions(frame)
        if result:
            emotions = result[0]['emotions']
            dominant_emotion = max(emotions, key=emotions.get)
            emotion_history.append(dominant_emotion)
            if len(emotion_history) > anomaly_threshold:
                emotion_history.pop(0)
                if len(set(emotion_history)) > 3:  # Muitas mudanças rápidas
                    return "Anomaly Detected"
            return dominant_emotion
        else:
            return "Not Detected"
    except Exception as e:
        print(f"Erro ao analisar emoções: {e}")
        return "Not Detected"

def add_text_with_background(frame, texts, font_size=1.0, font_thickness=2, bg_color=(200, 200, 200), text_color=(0, 0, 0), position=(10, 30), line_spacing=1.5):
    """
    Adiciona texto com fundo no frame usando OpenCV.
    """
    x, y = position
    for i, text in enumerate(texts):
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_size, font_thickness)
        text_width, text_height = text_size
        y_text = y + int(i * text_height * line_spacing)

        # Desenhar retângulo de fundo
        cv2.rectangle(frame, (x, y_text - text_height - 5), (x + text_width + 10, y_text + 5), bg_color, -1)
        # Adicionar texto
        cv2.putText(frame, text, (x + 5, y_text), cv2.FONT_HERSHEY_SIMPLEX, font_size, text_color, font_thickness, cv2.LINE_AA)
    return frame

def process_video_emotions_activities(video_path):
    """
    Processa vídeo, analisando emoções, atividades e detectando anomalias.
    """
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_video_path = os.path.join(output_dir, 'final92_video_emotions_activities.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    events_summary = {
        'emotions': {},
        'activities': {},
        'unknown_emotions': 0,
        'anomalies': 0
    }

    last_emotion = None
    last_activities = set()

    with tqdm(total=total_frames, desc="Analisando vídeo") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            # Processando o frame para landmarks de pose
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_results = pose.process(frame_rgb)

            # Desenhando o esqueleto do Mediapipe no frame, se landmarks forem detectados
            if pose_results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

            # Analisar emoção
            emotion = analyze_emotion(frame)
            if emotion == "Anomaly Detected":
                events_summary['anomalies'] += 1
            elif emotion == "Not Detected":
                events_summary['unknown_emotions'] += 1
            elif emotion != last_emotion:
                events_summary['emotions'][emotion] = events_summary['emotions'].get(emotion, 0) + 1
                last_emotion = emotion

            # Detectar atividades
            activities = set(detect_activities(pose_results))
            if activities != last_activities:
                for activity in activities:
                    events_summary['activities'][activity] = events_summary['activities'].get(activity, 0) + 1
                last_activities = activities

            # Adicionar legendas
            texts = [f"Emotion: {emotion}", f"Activities: {', '.join(activities) if activities else 'None'}"]
            frame = add_text_with_background(frame, texts, font_size=1.0, font_thickness=2, bg_color=(200, 200, 200), text_color=(0, 0, 0), position=(10, 30), line_spacing=2.0)

            # Escrever o frame no vídeo de saída
            out.write(frame)
            pbar.update(1)

    cap.release()
    out.release()
    print(f"Vídeo processado e salvo em: {output_video_path}")

    generate_emotions_activities_report(total_frames, events_summary)


def generate_emotions_activities_report(total_frames, events_summary):
    """
    Gera relatório resumido de emoções, atividades e anomalias.
    """
    report_path = os.path.join(output_dir, 'emotions_activities_report92.txt')
    with open(report_path, 'w') as f:
        f.write("Resumo de Emoções, Atividades e Anomalias\n\n")
        f.write(f"Total de frames analisados: {total_frames}\n")
        f.write("Total de emoções detectadas (eventos únicos):\n")
        for emotion, count in events_summary['emotions'].items():
            f.write(f"  - {emotion}: {count}\n")
        f.write(f"Total de frames sem emoções detectadas: {events_summary['unknown_emotions']}\n")
        f.write(f"Total de anomalias detectadas: {events_summary['anomalies']}\n")
        f.write("Total de atividades detectadas (eventos únicos):\n")
        for activity, count in events_summary['activities'].items():
            f.write(f"  - {activity}: {count}\n")
    print(f"Relatório gerado em: {report_path}")

# Caminho do vídeo de entrada
video_path = '/content/drive/MyDrive/Analise_Emocoes_TC4/analisado35e_video_faces_only.mp4'
process_video_emotions_activities(video_path)

"""Resumo de Emoções, Atividades e Anomalias

Total de frames analisados: 3326
Total de emoções detectadas (eventos únicos):
  - 😐 neutral: 110
  - 😨 fear: 49
  - 😢 sad: 87
  - 😠 angry: 31
  - 😊 happy: 75
  - 😲 surprise: 33
  - 🤢 disgust: 1

Total de frames sem emoções detectadas: 1761

Total de anomalias detectadas: 50

Total de atividades detectadas (eventos únicos):
  - ✋ (Esq) Mao esquerda levantada: 22
  - ✋ (Dir) Mao direita levantada: 22
  - 🙌 Maos levantadas: 16
  - 💃 Dancando: 2
  - 🤝 Aperto de maos: 1

Ajustes no código:
1. Restringir emoções repetidas:
Adicionei um controle temporal para que uma emoção só seja detectada novamente após um intervalo mínimo de frames. Isso evita que a mesma emoção seja contabilizada várias vezes em sequência.

2. Restringir falsos positivos de dança:
Atualizei os critérios para incluir movimento consistente dos braços e ombros e um limite mínimo para evitar que movimentos pequenos ou isolados sejam considerados dança.
"""

!pip install mediapipe
!pip install fer
!pip install tqdm
!pip install numpy
!pip install pillow
!pip install opencv-python

!pip uninstall mediapipe -y
!pip install mediapipe==0.10.9

!pip install --upgrade mediapipe

!pip install --upgrade pandas-gbq google-auth-oauthlib tensorflow

"""## 🚫 Tirando Perfil da Detecção de Anomalia"""

!pip install protobuf

"""## 🛠️ Ajustando Anomalias, Separando as Imagens

📌 Principais Ajustes:

   - ⚠️ Anomalias como Eventos Únicos:

    -- Verificação de frames consecutivos para eliminar duplicações e manter apenas eventos realmente únicos e relevantes.
"""

import cv2
import mediapipe as mp
from fer import FER
from tqdm import tqdm
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Inicializando MediaPipe Pose e FaceDetection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
fer_detector = FER(mtcnn=True)

# Configurando saída
output_dir = '/content/drive/MyDrive/Analise_Emocoes_TC4'
os.makedirs(output_dir, exist_ok=True)

# Pasta para salvar frames de anomalias e atividades específicas
anomaly_dir = os.path.join(output_dir, 'anomaly_frames_v2')
os.makedirs(anomaly_dir, exist_ok=True)

# Função para adicionar texto com fundo no vídeo
def add_text_with_background(frame, texts, font_size=0.8, position=(10, 30), bg_color=(240, 240, 240), text_color=(0, 0, 0), font_thickness=2, line_spacing=2.0):
    x, y = position
    for i, text in enumerate(texts):
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_size, font_thickness)
        text_width, text_height = text_size
        y_text = y + int(i * text_height * line_spacing)
        cv2.rectangle(frame, (x, y_text - text_height - 5), (x + text_width + 10, y_text + 5), bg_color, -1)
        cv2.putText(frame, text, (x + 5, y_text), cv2.FONT_HERSHEY_SIMPLEX, font_size, text_color, font_thickness, cv2.LINE_AA)
    return frame

# Histórico para anomalias e atividades
emotion_history = []
anomaly_threshold = 7  # Ajustado para um histórico maior e mais seletivo

def detect_activities(pose_results):
    activities = []
    if pose_results.pose_landmarks:
        landmarks = pose_results.pose_landmarks.landmark
        left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        nose = landmarks[mp_pose.PoseLandmark.NOSE]

        # Detectar mãos levantadas
        if left_hand.y < left_shoulder.y and abs(left_hand.x - left_shoulder.x) > 0.1 and abs(left_hand.x - nose.x) > 0.15:
            activities.append("Mao esquerda levantada")
        if right_hand.y < right_shoulder.y and abs(right_hand.x - right_shoulder.x) > 0.1 and abs(right_hand.x - nose.x) > 0.15:
            activities.append("Mao direita levantada")
        if left_hand.y < left_shoulder.y and right_hand.y < right_shoulder.y and abs(left_hand.x - nose.x) > 0.15 and abs(right_hand.x - nose.x) > 0.15:
            activities.append("Maos levantadas")

        # Detectar dança (movimento significativo do torso e ombros)
        shoulder_rotation = abs(left_shoulder.x - right_shoulder.x) / max(abs(left_shoulder.y - right_shoulder.y), 0.01)
        shoulder_movement = abs(left_shoulder.y - right_shoulder.y)
        arm_movement = max(abs(left_hand.x - left_shoulder.x), abs(right_hand.x - right_shoulder.x))

        if 0.5 < shoulder_rotation < 1.1 and (shoulder_movement > 0.25 or arm_movement > 0.4):
            activities.append("Dancando")

        # Detectar aperto de mãos (melhorado)
        if (
            left_hand.y > left_shoulder.y and right_hand.y > right_shoulder.y and  # Mãos abaixo dos ombros
            abs(left_hand.x - right_hand.x) < 0.015 and  # Ajuste horizontal mais permissivo
            abs(left_hand.y - right_hand.y) < 0.015 and  # Altura semelhante
            abs(left_hand.z - right_hand.z) < 0.015  # Profundidade realista
        ):
            activities.append("Aperto de maos")

    return activities

def analyze_emotion(frame):
    result = fer_detector.detect_emotions(frame)
    if result:
        emotions = result[0]['emotions']
        dominant_emotion = max(emotions, key=emotions.get)
        emotion_history.append(dominant_emotion)

        if len(emotion_history) > 15:
            emotion_history.pop(0)

        recent_changes = sum(1 for i in range(1, len(emotion_history)) if emotion_history[i] != emotion_history[i - 1])

        if recent_changes >= 8:
            return "Anomaly Detected"
        return dominant_emotion
    else:
        return "Not Detected"

def process_video_emotions_activities(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_video_path = os.path.join(output_dir, 'fdetection_video_emotions_activities_unique_anomalies.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    events_summary = {'emotions': {}, 'activities': {}, 'unknown_emotions': 0, 'anomalies': 0, 'anomaly_frames': [], 'activity_frames': {}}
    last_emotion = None
    last_activities = set()

    # Inicialização das variáveis de histórico para legenda
    last_displayed_emotion = None
    last_displayed_activities = set()



    with tqdm(total=total_frames, desc="Analisando vídeo") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pose_results = pose.process(frame_rgb)
            face_results = face_detection.process(frame_rgb)

            # Desenhar o esqueleto do MediaPipe Pose no frame
            if pose_results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    pose_results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),  # Cor verde para linhas
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)   # Cor azul para pontos
                )

            if face_results.detections:
                emotion = analyze_emotion(frame)
            else:
                emotion = "Not Detected"

            if emotion == "Anomaly Detected":
                frame_name = f"anomaly_frame_{pbar.n}.jpg"
                cv2.imwrite(os.path.join(anomaly_dir, frame_name), frame)
                events_summary['anomaly_frames'].append(frame_name)
                events_summary['anomalies'] += 1  # Incrementa corretamente o contador

            #if emotion != last_emotion:
                #events_summary['emotions'][emotion] = events_summary['emotions'].get(emotion, 0) + 1
                #last_emotion = emotion


            # Inicialização segura da variável activities
            activities = set(detect_activities(pose_results))

            # Atualizar a legenda apenas para eventos únicos
            if emotion != last_displayed_emotion or activities != last_displayed_activities:
                texts = [f"Emotion: {emotion}", f"Activities: {', '.join(activities) if activities else 'None'}"]
                frame = add_text_with_background(frame, texts)
                last_displayed_emotion = emotion
                last_displayed_activities = activities


            activities = set(detect_activities(pose_results))
            if activities != last_activities:
                for activity in activities:
                    events_summary['activities'][activity] = events_summary['activities'].get(activity, 0) + 1
                    if activity in ["Dancando", "Aperto de maos"]:
                        frame_name = f"{activity.lower().replace(' ', '_')}_frame_{pbar.n}.jpg"
                        cv2.imwrite(os.path.join(anomaly_dir, frame_name), frame)
                        events_summary['activity_frames'].setdefault(activity, []).append(frame_name)
                last_activities = activities

            out.write(frame)
            pbar.update(1)

    cap.release()
    out.release()
    print(f"🎬 Vídeo processado e salvo em: {output_video_path}")

    # Função para gerar relatório
def generate_emotions_activities_report(total_frames, events_summary):
    report_path = os.path.join(output_dir, 'emotions_activities_report_fdetection49.txt')

    emotion_icons = {"neutral": "😐", "sad": "😢", "angry": "😠", "fear": "😨", "happy": "😊", "surprise": "😲", "Not Detected": "❓"}
    activity_icons = {"Mao esquerda levantada": "✋ (Esq)", "Mao direita levantada": "✋ (Dir)", "Maos levantadas": "🙌", "Dancando": "💃", "Aperto de maos": "🤝"}

    with open(report_path, 'w') as f:
        f.write("# 📊 Resumo de Emoções, Atividades e Anomalias\n\n")
        f.write(f"**🎥 Total de frames analisados:** {total_frames}\n\n")
        f.write("## 😊 Emoções detectadas (eventos únicos):\n")
        for emotion, count in events_summary['emotions'].items():
            icon = emotion_icons.get(emotion, "❓")
            f.write(f"- {icon} **{emotion.capitalize()}**: {count} vezes\n")
        f.write("\n## 🔍 Atividades detectadas (eventos únicos):\n")
        for activity, count in events_summary['activities'].items():
            icon = activity_icons.get(activity, "🔹")
            f.write(f"- {icon} **{activity.capitalize()}**: {count} vezes\n")

    print("\n📊 **Resumo do relatório:**")
    with open(report_path, 'r') as file:
        print(file.read())

    generate_emotions_activities_report(total_frames, events_summary)

# Caminho do vídeo de entrada
video_path = '/content/drive/MyDrive/Analise_Emocoes_TC4/analisado35e_video_faces_only.mp4'
process_video_emotions_activities(video_path)

"""## 📦 Criando o Requirements"""

!pip freeze > requirements.txt