import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import csv

def preprocess_image(image_path, target_size=(224, 224)):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def postprocess_mask(mask):
    mask_bin = (mask > 0.5).astype(np.uint8)[0, :, :, 0]
    percentage = (np.sum(mask_bin) / mask_bin.size) * 100
    mask_image = mask_bin * 255
    return mask_image, round(percentage, 2)

def generate_csv_report(results, location, report_path):
    with open(report_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Location', 'Date', 'Forested Area (%)', 'Deforestation Area (%)'])
        for r in results:
            writer.writerow([
                location,
                r.get('date', ''),
                round(r['deforestation_percentage'], 2),
                round(100 - r['deforestation_percentage'], 2)
            ])