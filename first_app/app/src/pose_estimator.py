import mediapipe as mp

class PoseEstimator:
    def __init__(self, static_image_mode, model_complexity, min_detection_confidence, min_tracking_confidence):
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def process(self, image):
        return self.pose.process(image)