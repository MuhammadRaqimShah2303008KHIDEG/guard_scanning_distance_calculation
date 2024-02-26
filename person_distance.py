import math
import cv2
from ultralytics import YOLO
from datetime import datetime
import time
from datetime import datetime, timezone, timedelta

def calculate_centroid(box1):
    """
    Calculate the centroid of bounding box
    Args:
        box (list): Bounding box data
    """
    x_min, y_min, x_max, y_max = box1
    centroid_x = (x_min + x_max) / 2
    centroid_y = (y_min + y_max) / 2
    centroid = [centroid_x,centroid_y]
    return centroid

def pixels_to_inches_cv2(pixels, width_pixels, width_inches=None):
    """
    Convert pixels to inches based on the width of the image in pixels and inches (optional).
    If width_inches is not provided, it calculates the PPI based on the image's width in pixels.

    Args:
    - pixels: The number of pixels to convert to inches.
    - width_pixels: The width of the image in pixels.
    - width_inches (optional): The width of the image in inches. Default is None.

    Returns:
    - The equivalent distance in inches.
    """
    if width_inches is None:
        # Calculate the PPI based on the image's width in pixels
        ppi = width_pixels / pixels
    else:
        # Calculate the PPI based on the provided width in inches
        ppi = width_pixels / width_inches
    inches = pixels / ppi
    return inches

def calculate_distance(centroid1, centroid2):
    """
    Calculate distance between two centroids
    Args:
        centroid1 (point): First bounding box data
        centroid2 (point): Second bounding box data
    """
    conversion_factor = 100
    pixel_distance = math.sqrt((centroid1[0] - centroid2[0]) ** 2 + (centroid1[1] - centroid2[1]) ** 2)

    # distance_in_centimeters = pixel_distance / conversion_factor
    return pixel_distance 

# ATM functionality check 
def detect_atm_usage(model_path, video_path, target_fps):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    frame_no = 0
    count = 0
    frame_interval = int(cap.get(cv2.CAP_PROP_FPS) / target_fps)

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            print(f"Working with frame {frame_no}, no frame detected")
            break
        else:
            results = model.track(source=frame, show=True, project='./result', tracker="bytetrack.yaml", conf=0.4)
            for result in results:
                if result.boxes.id is not None:
                    trk_ids = result.boxes.id.int().cpu().tolist()
                    class_name = result.boxes.cls.tolist()
                    conf_name = result.boxes.conf.tolist()
                    boxes = result.boxes.xyxy.cpu().tolist()
                    cls_conf = res = dict(zip(class_name, conf_name))
                    res = dict(zip(class_name, boxes))
                    keys = list(res)
                    height, width, _ = frame.shape


                    if len(class_name) >= 2:

                        if 1.0 in class_name and cls_conf[1.0] >= 0.3 and 2.0 in class_name and cls_conf[2.0] >= 0.3:
                            print(class_name)
                            print(boxes)
                            print(trk_ids)
                            print(res)
                            # print(res[0])
                            box1=res[1.0]
                            box2=res[2.0]
                            centroid1 = calculate_centroid(box1)
                            centroid2 = calculate_centroid(box2)
                            print("Centroid:", centroid1)
                            print("Centroid:", centroid2)
                            distance_pixels = calculate_distance(centroid1, centroid2)
                            print('distance = ',distance_pixels, 'inches')
                            distance_inches = pixels_to_inches_cv2(distance_pixels, width)
                            print('distance = ',distance_inches, 'inches')
                            if distance_inches <= 125:
                                count = 0
                                return 'distance = ',distance_inches, 'Guard is Scanning' 

                            elif count >= 1000:
                                atm_detected = False
                                return 'Guard is not Scanning' 

                            else:
                                print(count)
                                count +=1
                        
                        else:
                            pass
                    else:
                        pass 
                            
                        # calculate_distance(self.centroids[0], self.centroids[1])
            # Increment frame counter
        frame_no += 1
    # Release video capture
    cap.release()


if __name__ == '__main__':
    model_path = 'best (5).pt'
    video_path = "yt5s.io-Airport security goes too far!-(1080p).mp4"
    target_fps = 8
    print(detect_atm_usage(model_path, video_path, target_fps))


'''
Class, label
0, Guard
1, Person
2, Scanner
'''