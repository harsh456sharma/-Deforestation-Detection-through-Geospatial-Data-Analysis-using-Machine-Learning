from flask import Blueprint, render_template, request, current_app
from app.utils import preprocess_image, postprocess_mask, generate_csv_report
import os
import uuid
import cv2
from tensorflow.keras.models import load_model

analyze_bp = Blueprint('analyze', __name__)
model = load_model(os.path.join('app', 'model', 'model.h5'))

@analyze_bp.route('/analyze-single', methods=['GET', 'POST'])
def analyze_single():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = f"{uuid.uuid4().hex}.jpg"
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)

            img = preprocess_image(upload_path)
            pred_mask = model.predict(img)
            mask, percentage = postprocess_mask(pred_mask)

            mask_filename = f"mask_{filename}"
            result_path = os.path.join(current_app.config['RESULT_FOLDER'], mask_filename)
            cv2.imwrite(result_path, mask)

            return render_template('single.html',
                                   uploaded_image=filename,
                                   mask_image=mask_filename,
                                   deforestation_percentage=percentage)
    return render_template('single.html')

@analyze_bp.route('/analyze-batch', methods=['GET', 'POST'])
def analyze_batch():
    results = []
    if request.method == 'POST':
        location = request.form.get('location', 'Unknown')
        dates = request.form.getlist('dates')  # Should be one date per image
        files = request.files.getlist('images')[:20]  # Limit to 20 files

        for idx, file in enumerate(files):
            if file:
                filename = f"{uuid.uuid4().hex}.jpg"
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)

                img = preprocess_image(upload_path)
                pred_mask = model.predict(img)
                mask, percentage = postprocess_mask(pred_mask)

                mask_filename = f"mask_{filename}"
                result_path = os.path.join(current_app.config['RESULT_FOLDER'], mask_filename)
                cv2.imwrite(result_path, mask)

                date = dates[idx] if idx < len(dates) else ''
                results.append({
                    'uploaded_image': filename,
                    'mask_image': mask_filename,
                    'deforestation_percentage': percentage,
                    'date': date
                })

        # Generate CSV report
        report_folder = os.path.join(current_app.root_path, 'static', 'report')
        os.makedirs(report_folder, exist_ok=True)
        report_path = os.path.join(report_folder, 'report.csv')
        generate_csv_report(results, location, report_path)

    return render_template('batch.html', results=results)

