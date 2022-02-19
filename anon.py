import psycopg2
import sys
import os
import blur_persons.blur_persons
from anonymizer.anonymizer.detection import Detector, get_weights_path
from PIL import Image, ImageDraw, ImageFilter
import numpy
import argparse
import sys

def main(argv):
    parser = argparse.ArgumentParser(description="Anonymise OpenWanderer panoramas.")
    parser.add_argument('-f', dest='startid', type=int, default=0)
    parser.add_argument('-t', dest='endid', type=int, default=sys.maxsize)
    parser.add_argument('-a', dest='anonymiser', type=str, default='understandai')
    parser.add_argument('-i',dest='srcdir', type=str, required=True)
    parser.add_argument('-o',dest='destdir', type=str, required=True)

    args = parser.parse_args()

    results = find_unauthorised(args.startid, args.endid)
    if(len(results) == 0):
        print ("No Results")
    else:
        ids = [result[0] for result in results]
        if args.anonymiser == 'blur_persons':
            detect_blur_persons(ids, args.srcdir, args.destdir)
        else:
            detect_understandai_anonymizer(ids, args.srcdir, args.destdir)
                

def find_unauthorised(startid=1, endid=9999):
    conn = psycopg2.connect('dbname=gis user=gis')
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM panoramas WHERE authorised=0 AND id BETWEEN {startid} AND {endid} ORDER BY id")
    results = cur.fetchall()
    return results

def detect_blur_persons(ids, input_path, output_path):
    filenames = [f"{input_path}/{i}.jpg" for i in ids]
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    blur_persons.blur_persons.blur_in_files(
        files=filenames,
        model='xception_coco_voctrainval',
        blur=30,
        classes=['person','car','motorbike'],
        dest=output_path,
        suffix=None,
        quality=None,
        mask=None,
        lite=None,
        dezoom=1.0)
            

def detect_understandai_anonymizer(ids, input_path, output_path, threshold=0.1, weights_path="./anonymizer/weights"):
    print(threshold)
    detectors = {
        'face': Detector(kind='face', weights_path=get_weights_path(weights_path, kind='face')),
        'plate': Detector(kind='plate', weights_path=get_weights_path(weights_path, kind='plate'))
    }
    detection_thresholds = {
        'face': threshold,
        'plate': threshold
    }

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for id in ids:
        print(f"Loading {input_path}/{id}.jpg")
        with Image.open(f"{input_path}/{id}.jpg") as image:
            npimage = numpy.array(image.convert('RGB'))
            detected_boxes = []
            for kind,detector in detectors.items():
                new_boxes = detector.detect(npimage, detection_thresholds[kind])
                detected_boxes.extend(new_boxes)
            
            draw = ImageDraw.Draw(image) 

            for box in detected_boxes:
                print(f"{box.x_min} {box.y_min} {box.x_max} {box.y_max} {box.score} {box.kind}")

                cropbox = (int(box.x_min), int(box.y_min), int(box.x_max), int(box.y_max))
                crop = image.crop(cropbox)
                for i in range(20):
                    crop = crop.filter(ImageFilter.BLUR)
                image.paste(crop, cropbox)


            image.save(f"{output_path}/{id}.jpg", "JPEG")

if __name__ == "__main__":
    main(sys.argv[1:])
