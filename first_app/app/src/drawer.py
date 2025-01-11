import cv2 as cv

class Drawer:
    def __init__(self, color, bg_color):
        self.color = color
        self.bg_color = bg_color

    def draw_landmarks(self, image, landmarks, visibility_th=0.5):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []

        for index, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_z = landmark.z
            landmark_point.append([landmark.visibility, (landmark_x, landmark_y)])

            if landmark.visibility < visibility_th:
                continue

            if index == 0:  # 鼻
                cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
            if index == 1:  # 右目：目頭
                cv.circle(image, (landmark_x, landmark_y), 5, (0, 255, 0), 2)
            # Add other landmarks as needed

        return image

    def draw_stick_figure(self, image, landmarks, visibility_th=0.5):
        # Implement stick figure drawing logic
        pass