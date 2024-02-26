import cv2
import ultralytics
from ultralytics import YOLO

model = YOLO('best (5).pt')
results = model.track(source='yt5s.io-Airport security goes too far!-(1080p).mp4', \
save=True, show=True, project='./result', tracker="bytetrack.yaml", conf=0.35)