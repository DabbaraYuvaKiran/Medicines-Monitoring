from flask import Flask, request, jsonify, render_template, url_for
from models import db, Medicine
from preprocess import predict_quality
import os
import matplotlib.pyplot as plt

def setup_routes(app):
    @app.route('/')
    def home():
        return render_template("index.html")

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        template_path = os.path.abspath("templates/upload.html")

        if not os.path.exists(template_path):
            return jsonify({"error": "upload.html not found!"}), 404  

        if request.method == 'GET':
            return render_template("upload.html")

        name = request.form.get('name')
        ingredients = request.form.get('ingredients')

        if not name or not ingredients:
            return jsonify({"error": "Both 'name' and 'ingredients' are required!"}), 400  

        try:
            quality = predict_quality(ingredients)
        except Exception as e:
            return jsonify({"error": f"Prediction failed: {str(e)}"}), 500  

        try:
            # Save to database FIRST
            new_medicine = Medicine(name=name, ingredients=ingredients, quality=quality)
            db.session.add(new_medicine)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Database error: {str(e)}"}), 500  

        # **Generate graph AFTER committing to database**
        generate_bar_chart()

        return render_template("result.html", name=name, quality=quality, graph_url=url_for('static', filename='graph.png'))

    @app.route('/medicines', methods=['GET'])
    def get_medicines():
        medicines = Medicine.query.all()
        return jsonify([{'id': m.id, 'name': m.name, 'quality': m.quality} for m in medicines])

def generate_bar_chart():
    """Generates and saves a bar chart of quality distribution."""
    medicines = Medicine.query.all()
    quality_counts = {"Good": 0, "Poor": 0}

    for medicine in medicines:
        if medicine.quality in quality_counts:
            quality_counts[medicine.quality] += 1

    labels = list(quality_counts.keys())
    values = list(quality_counts.values())

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['green', 'red'])
    plt.xlabel("Quality")
    plt.ylabel("Count")
    plt.title("Medicine Quality Distribution")
    
    # Save with overwrite
    plt.savefig("static/graph.png")
    plt.close()
