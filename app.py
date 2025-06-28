from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from functools import wraps
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api
from io import BytesIO
import pandas as pd
import openpyxl
load_dotenv()

app = Flask(__name__)
app.secret_key = 'ganesh_secret'

cloudinary.config(
  cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key=os.getenv('CLOUDINARY_API_KEY'),
  api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["ganesh_mandal"]
expenses_collection = db["expenses"]

# ========== DECORATOR ==========
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def homepage():
    events = list(db.events.find().sort("event_date", -1))
    gallery = list(db.gallery.find().sort("_id", -1))[:3]
    return render_template('index.html', events=events, gallery=gallery)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = db.admin.find_one({'username': username, 'password': password})
        if admin:
            session['admin_logged_in'] = True
            return redirect('/dashboard')
        flash('Invalid credentials')
    return render_template('admin_login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin_dashboard.html')

@app.route('/events', methods=['GET', 'POST'])
@login_required
def manage_events():
    if request.method == 'POST':
        image = request.files['image']
        upload_result = cloudinary.uploader.upload(image)
        image_url = upload_result['secure_url']
        public_id = upload_result['public_id']

        db.events.insert_one({
            'title': request.form['title'],
            'description': request.form['description'],
            'event_date': request.form['event_date'],
            'image_url': image_url,
            'public_id': public_id
        })

    events = list(db.events.find().sort("event_date", -1))
    return render_template('events_manage.html', events=events)

@app.route('/delete_event/<string:event_id>')
@login_required
def delete_event(event_id):
    event = db.events.find_one({'_id': ObjectId(event_id)})
    if event:
        if 'public_id' in event:
            cloudinary.uploader.destroy(event['public_id'])
        db.events.delete_one({'_id': ObjectId(event_id)})
    return redirect('/events')

@app.route('/view_events')
def view_events():
    events = list(db.events.find().sort("event_date", -1))
    return render_template('view_events.html', events=events)

@app.route('/gallery', methods=['GET', 'POST'])
@login_required
def manage_gallery():
    if request.method == 'POST':
        file = request.files['image']
        upload_result = cloudinary.uploader.upload(file)
        image_url = upload_result['secure_url']
        public_id = upload_result['public_id']

        db.gallery.insert_one({
            'caption': request.form['caption'],
            'url': image_url,
            'public_id': public_id
        })

    gallery = list(db.gallery.find().sort("_id", -1))
    return render_template('gallery_manage.html', gallery=gallery)

@app.route('/galleryview')
def view_gallery():
    gallery = list(db.gallery.find().sort("_id", -1))
    return render_template('view_gallery.html', gallery=gallery)

@app.route('/delete_image/<string:image_id>')
@login_required
def delete_image(image_id):
    image = db.gallery.find_one({'_id': ObjectId(image_id)})
    if image:
        if 'public_id' in image:
            cloudinary.uploader.destroy(image['public_id'])
        db.gallery.delete_one({'_id': ObjectId(image_id)})
    return redirect('/gallery')

@app.route('/vargani')
@login_required
def vargani_entry():
    return render_template('vargani.html')

@app.route('/submit_vargani', methods=['POST'])
@login_required
def submit_vargani():
    name = request.form['name']
    amount = int(request.form['amount'])
    contact = request.form['contact']

    db.vargani.insert_one({
        'name': name,
        'amount': amount,
        'contact': contact
    })

    sms_message = f" धन्यवाद आपली ₹{amount} वर्गणी प्राप्त झाली आहे. -18 House"

    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "sender_id": "FSTSMS",
        "message": sms_message,
        "language": "unicode",
        "route": "q",
        "numbers": contact
    }
    headers = {
        "authorization": os.getenv("FAST2SMS_API_KEY"),
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        try:
            data = response.json()
            print("✅ SMS sent successfully:", data)
        except ValueError:
            print("❌ SMS response not JSON. Text was:", response.text)
    except Exception as e:
        print("🔥 SMS sending failed:", e)

    flash("वर्गणी यशस्वीरीत्या नोंदवली गेली आहे.")
    return redirect('/vargani_list')

@app.route('/vargani_list')
@login_required
def vargani_list():
    data = list(db.vargani.find())
    total = sum(item['amount'] for item in data)
    return render_template('vargani_list.html', vargani=data, total=total)

@app.route('/edit_vargani/<id>', methods=['GET', 'POST'])
@login_required
def edit_vargani(id):
    if request.method == 'POST':
        db.vargani.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': request.form['name'],
                'amount': int(request.form['amount']),
                'contact': request.form['contact']
            }}
        )
        return redirect('/vargani_list')
    vargani = db.vargani.find_one({'_id': ObjectId(id)})
    return render_template('edit_vargani.html', vargani=vargani)

@app.route('/delete_vargani/<string:id>')
@login_required
def delete_vargani(id):
    db.vargani.delete_one({"_id": ObjectId(id)})
    return redirect('/vargani_list')

@app.route('/delete_all_vargani')
@login_required
def delete_all_vargani():
    db.vargani.delete_many({})
    return redirect('/vargani_list')

@app.route('/download_vargani_excel')
@login_required
def download_vargani_excel():
    data = list(db.vargani.find())
    for item in data:
        item.pop('_id', None)  # Remove MongoDB ID
    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Vargani_List')

    output.seek(0)
    return send_file(output, download_name='vargani_list.xlsx', as_attachment=True)
  

@app.route('/expense', methods=['GET', 'POST'])
@login_required
def manage_expense():
    if request.method == 'POST':
        new_expense = {
            "title": request.form['title'],
            "amount": int(request.form['amount']),
            "description": request.form['description'],
            "created_at": datetime.utcnow()
        }
        db.expense.insert_one(new_expense)

    expenses = list(db.expense.find().sort("created_at", -1))
    total_expense = sum(exp["amount"] for exp in expenses)
    vargani_entries = list(db.vargani.find())
    total_vargani = sum(v["amount"] for v in vargani_entries)
    remaining = total_vargani - total_expense

    return render_template(
        'expense.html',
        expenses=expenses,
        total_expense=total_expense,
        total_vargani=total_vargani,
        remaining=remaining
    )

@app.route("/delete_expense/<string:id>")
def delete_expense(id):
    db.expense.delete_one({"_id": ObjectId(id)})
    return redirect('/expense')

if __name__ == '__main__':
    app.run(debug=True)
