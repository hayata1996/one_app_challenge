import cv2
import mediapipe as mp
import numpy as np

# MediaPipeのセットアップ
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)

# ウェブカメラの準備
cap = cv2.VideoCapture(0)

# FaceMeshの設定
# リソースを使い終わったら自動的にリリースできるようにコンテキストマネージャを使用する
with mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as face_mesh:

    # while True:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # BGR画像をRGBに変換
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 検出を実行
        results = face_mesh.process(rgb_image)
        results2 = hands.process(rgb_image)

        # 黒背景の画像を作成
        height, width, _ = image.shape
        #background = np.zeros((height, width, 3), np.uint8)
        background = np.ones((height, width, 3), np.uint8)*255

        # 結果を黒背景の画像上にface描画
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=background,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION)
        #handsを描画        
        if results2.multi_hand_landmarks:
            for hand_landmarks in results2.multi_hand_landmarks:
                #print('Handedness:', results.multi_handedness)
                mp_drawing.draw_landmarks(image=background,
                                          landmark_list=hand_landmarks,
                                          connections=mp_hands.HAND_CONNECTIONS)    

        # 画像を表示
        cv2.imshow('MediaPipe FaceMesh on Black Background', background)
        # "q"を押すと終了
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
