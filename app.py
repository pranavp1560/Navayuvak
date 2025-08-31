# from flask import Flask, render_template, request, redirect, url_for, flash, session,send_file
# from pymongo import MongoClient
# from werkzeug.utils import secure_filename
# from bson.objectid import ObjectId
# from functools import wraps
# import os
# import requests
# from datetime import datetime
# from dotenv import load_dotenv
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api
# from io import BytesIO
# import pandas as pd
# import openpyxl
# import io
# load_dotenv()

# app = Flask(__name__)
# app.secret_key = 'ganesh_secret'

# cloudinary.config(
#   cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
#   api_key=os.getenv('CLOUDINARY_API_KEY'),
#   api_secret=os.getenv('CLOUDINARY_API_SECRET')
# )

# # MongoDB setup
# client = MongoClient(os.getenv("MONGO_URI"))
# db = client["ganesh_mandal"]
# expenses_collection = db["expenses"]
# collection = db['bhandi_records']


# # ========== DECORATOR ==========
# # def login_required(f):
# #     @wraps(f)
# #     def decorated_function(*args, **kwargs):
# #         if not session.get('admin_logged_in'):
# #             return redirect('/admin')
# #         return f(*args, **kwargs)
# #     return decorated_function
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not session.get('admin_logged_in'):
#             return redirect('/admin')
#         return f(*args, **kwargs)
#     return decorated_function

# # @app.route('/')
# # def homepage():
# #     events = list(db.events.find().sort("event_date", -1))
# #     gallery = list(db.gallery.find().sort("_id", -1))[:3]
# #     return render_template('index.html', events=events, gallery=gallery)

# @app.route('/')
# def homepage():
#     settings = db.settings.find_one() or {}
#     show_aahaval = settings.get("aahaval_visible", False)

#     vargani_data = []
#     expense_data = []
#     total_vargani = 0
#     total_expense = 0
#     remaining = 0

#     if show_aahaval:
#         vargani_data = list(db.vargani.find())
#         expense_data = list(db.expense.find())
#         total_vargani = sum(v['amount'] for v in vargani_data)
#         total_expense = sum(e['amount'] for e in expense_data)
#         remaining = total_vargani - total_expense

#     events = list(db.events.find().sort("event_date", -1))
#     gallery = list(db.gallery.find().sort("_id", -1))[:10]

#     return render_template(
#         'index.html',
#         events=events,
#         gallery=gallery,
#         show_aahaval=show_aahaval,
#         vargani_data=vargani_data,
#         expense_data=expense_data,
#         total_vargani=total_vargani,
#         total_expense=total_expense,
#         remaining=remaining
#     )


# # @app.route('/admin', methods=['GET', 'POST'])
# # def admin_login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         admin = db.admin.find_one({'username': username, 'password': password})
# #         if admin:
# #             session['admin_logged_in'] = True
# #             return redirect('/dashboard')
# #         flash('Invalid credentials')
# #     return render_template('admin_login.html')
# @app.route('/admin', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         admin = db.admin.find_one({'username': username, 'password': password})

#         if admin:
#             session['admin_logged_in'] = True
#             return redirect('/dashboard')
#         else:
#             flash('Invalid credentials', 'error')  # optional message flashing

#     return render_template('admin_login.html')




# @app.route('/about')
# def about():
#     return render_template('about.html')

# # @app.route('/logout')
# # def logout():
# #     session.clear()
# #     return redirect('/admin')
# @app.route('/logout')
# def logout():
#     session.pop('admin_logged_in', None)
#     return redirect('/')



# # @app.route('/dashboard')
# # @login_required
# # def dashboard():
# #     settings = db.settings.find_one() or {}
# #     show_aahaval = settings.get('aahaval_visible', False)
# #     return render_template("admin_dashboard.html", show_aahaval=show_aahaval)
# @app.route('/dashboard')
# @login_required
# def dashboard():
#     settings = db.settings.find_one() or {}
#     show_aahaval = settings.get('aahaval_visible', False)
#     return render_template("admin_dashboard.html", show_aahaval=show_aahaval)



# @app.route('/events', methods=['GET', 'POST'])
# @login_required
# def manage_events():
#     if request.method == 'POST':
#         image = request.files['image']
#         upload_result = cloudinary.uploader.upload(image)
#         image_url = upload_result['secure_url']
#         public_id = upload_result['public_id']

#         db.events.insert_one({
#             'title': request.form['title'],
#             'description': request.form['description'],
#             'event_date': request.form['event_date'],
#             'image_url': image_url,
#             'public_id': public_id
#         })

#     events = list(db.events.find().sort("event_date", -1))
#     return render_template('events_manage.html', events=events)

# @app.route('/delete_event/<string:event_id>')
# @login_required
# def delete_event(event_id):
#     event = db.events.find_one({'_id': ObjectId(event_id)})
#     if event:
#         if 'public_id' in event:
#             cloudinary.uploader.destroy(event['public_id'])
#         db.events.delete_one({'_id': ObjectId(event_id)})
#     return redirect('/events')

# @app.route('/view_events')
# def view_events():
#     events = list(db.events.find().sort("event_date", -1))
#     return render_template('view_events.html', events=events)

# @app.route('/gallery', methods=['GET', 'POST'])
# @login_required
# def manage_gallery():
#     if request.method == 'POST':
#         file = request.files['image']
#         upload_result = cloudinary.uploader.upload(file)
#         image_url = upload_result['secure_url']
#         public_id = upload_result['public_id']

#         db.gallery.insert_one({
#             # 'caption': request.form['caption'],
#             'url': image_url,
#             'public_id': public_id
#         })

#     gallery = list(db.gallery.find().sort("_id", -1))
#     return render_template('gallery_manage.html', gallery=gallery)

# @app.route('/galleryview')
# def view_gallery():
#     gallery = list(db.gallery.find().sort("_id", -1))
#     return render_template('view_gallery.html', gallery=gallery)

# @app.route('/delete_image/<string:image_id>')
# @login_required
# def delete_image(image_id):
#     image = db.gallery.find_one({'_id': ObjectId(image_id)})
#     if image:
#         if 'public_id' in image:
#             cloudinary.uploader.destroy(image['public_id'])
#         db.gallery.delete_one({'_id': ObjectId(image_id)})
#     return redirect('/gallery')

# @app.route('/vargani')
# @login_required
# def vargani_entry():
#     return render_template('vargani.html')



# # @app.route('/submit_vargani', methods=['POST'])
# # @login_required
# # def submit_vargani():
# #     name = request.form['name']
# #     amount = int(request.form['amount'])
# #     contact = request.form['contact']

# #     now = datetime.now()
# #     year = now.year

# #     db.vargani.insert_one({
# #         'name': name,
# #         'amount': amount,
# #         'contact': contact,
# #         'year': year,  # <-- Add this line
# #         'submitted_at': now
# #     })

# #     sms_message = f"धन्यवाद आपली ₹{amount} वर्गणी प्राप्त झाली आहे. -18 House"

# #     url = "https://www.fast2sms.com/dev/bulkV2"
# #     payload = {
# #         "sender_id": "FSTSMS",
# #         "message": sms_message,
# #         "language": "unicode",
# #         "route": "q",
# #         "numbers": contact
# #     }
# #     headers = {
# #         "authorization": os.getenv("FAST2SMS_API_KEY"),
# #         "Content-Type": "application/json"
# #     }

# #     try:
# #         response = requests.post(url, json=payload, headers=headers)
# #         try:
# #             data = response.json()
# #             print("✅ SMS sent successfully:", data)
# #         except ValueError:
# #             print("❌ SMS response not JSON. Text was:", response.text)
# #     except Exception as e:
# #         print("🔥 SMS sending failed:", e)

# #     flash("वर्गणी यशस्वीरीत्या नोंदवली गेली आहे.")
# #     return redirect('/vargani_list')

# @app.route('/submit_vargani', methods=['POST'])
# @login_required
# def submit_vargani():
#     name = request.form['name'].strip()
#     amount = int(request.form['amount'])
#     contact = request.form['contact'].strip()
#     now = datetime.now()
#     year = now.year

#     # ✅ Duplicate check
#     existing_entry = db.vargani.find_one({
#         'name': name,
#         'contact': contact,
#         'year': year
#     })

#     if existing_entry:
#         flash(f" ! '{name}' ची ₹{existing_entry['amount']} वर्गणी आधीच नोंदवली आहे.", 'error')
#         return redirect('/vargani')

#     # ✅ Save entry if not duplicate
#     db.vargani.insert_one({
#         'name': name,
#         'amount': amount,
#         'contact': contact,
#         'year': year,
#         'submitted_at': now
#     })

#     # ✅ Send SMS
#     sms_message = f"धन्यवाद आपली ₹{amount} वर्गणी प्राप्त झाली आहे. -18 House"
#     url = "https://www.fast2sms.com/dev/bulkV2"
#     payload = {
#         "sender_id": "FSTSMS",
#         "message": sms_message,
#         "language": "unicode",
#         "route": "q",
#         "numbers": contact
#     }
#     headers = {
#         "authorization": os.getenv("FAST2SMS_API_KEY"),
#         "Content-Type": "application/json"
#     }

#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         try:
#             data = response.json()
#             print("✅ SMS sent successfully:", data)
#         except ValueError:
#             print("❌ SMS response not JSON. Text was:", response.text)
#     except Exception as e:
#         print("🔥 SMS sending failed:", e)

#     flash("✅ वर्गणी यशस्वीरीत्या नोंदवली गेली आहे.")
#     return redirect('/vargani_list')

# # @app.route('/vargani_list')
# # @login_required
# # def vargani_list():
# #     data = list(db.vargani.find())
# #     total = sum(item['amount'] for item in data)
# #     return render_template('vargani_list.html', vargani=data, total=total)
# @app.route('/vargani_list')
# @login_required
# def vargani_list():
#     selected_year = request.args.get('year', datetime.now().year, type=int)

#     data = list(db.vargani.find({'year': selected_year}))
#     total = sum(item['amount'] for item in data)

#     # Get distinct years for dropdown
#     all_years = db.vargani.distinct('year')
#     all_years.sort(reverse=True)

#     return render_template('vargani_list.html',
#                            vargani=data,
#                            total=total,
#                            selected_year=selected_year,
#                            years=all_years)

# @app.route('/edit_vargani/<id>', methods=['GET', 'POST'])
# @login_required
# def edit_vargani(id):
#     if request.method == 'POST':
#         db.vargani.update_one(
#             {'_id': ObjectId(id)},
#             {'$set': {
#                 'name': request.form['name'],
#                 'amount': int(request.form['amount']),
#                 'contact': request.form['contact']
#             }}
#         )
#         return redirect('/vargani_list')
#     vargani = db.vargani.find_one({'_id': ObjectId(id)})
#     return render_template('edit_vargani.html', vargani=vargani)

# @app.route('/delete_vargani/<string:id>')
# @login_required
# def delete_vargani(id):
#     db.vargani.delete_one({"_id": ObjectId(id)})
#     return redirect('/vargani_list')

# @app.route('/delete_all_vargani')
# @login_required
# def delete_all_vargani():
#     db.vargani.delete_many({})
#     return redirect('/vargani_list')

# @app.route('/download_vargani_excel')
# @login_required
# def download_vargani_excel():
#     data = list(db.vargani.find())
#     for item in data:
#         item.pop('_id', None)  # Remove MongoDB ID
#     df = pd.DataFrame(data)

#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         df.to_excel(writer, index=False, sheet_name='Vargani_List')

#     output.seek(0)
#     return send_file(output, download_name='vargani_list.xlsx', as_attachment=True)


# # @app.route('/expense', methods=['GET', 'POST'])
# # @login_required
# # def manage_expense():
# #     if request.method == 'POST':
# #         new_expense = {
# #             "title": request.form['title'],
# #             "amount": int(request.form['amount']),
# #             "description": request.form['description'],
# #             "created_at": datetime.utcnow()
# #         }
# #         db.expense.insert_one(new_expense)

# #     expenses = list(db.expense.find().sort("created_at", -1))
# #     total_expense = sum(exp["amount"] for exp in expenses)
# #     vargani_entries = list(db.vargani.find())
# #     total_vargani = sum(v["amount"] for v in vargani_entries)
# #     remaining = total_vargani - total_expense

# #     return render_template(
# #         'expense.html',
# #         expenses=expenses,
# #         total_expense=total_expense,
# #         total_vargani=total_vargani,
# #         remaining=remaining
# #     )
# @app.route('/expense', methods=['GET', 'POST'])
# @login_required
# def manage_expense():
#     selected_year = request.args.get('year', datetime.now().year, type=int)

#     if request.method == 'POST':
#         new_expense = {
#             "title": request.form['title'],
#             "amount": int(request.form['amount']),
#             "description": request.form['description'],
#             "created_at": datetime.utcnow()
#         }
#         db.expense.insert_one(new_expense)
#         return redirect(url_for('manage_expense', year=selected_year))  # preserve selected year on submit

#     # Filter expenses by selected year
#     start_of_year = datetime(selected_year, 1, 1)
#     end_of_year = datetime(selected_year + 1, 1, 1)
#     expenses = list(db.expense.find({
#         "created_at": {"$gte": start_of_year, "$lt": end_of_year}
#     }).sort("created_at", -1))
#     total_expense = sum(exp["amount"] for exp in expenses)

#     # Get vargani entries of selected year too
#     vargani_entries = list(db.vargani.find({'year': selected_year}))
#     total_vargani = sum(v["amount"] for v in vargani_entries)

#     remaining = total_vargani - total_expense

#     # Fetch all available years
#     all_years = db.expense.distinct("created_at")
#     years = sorted(list({d.year for d in all_years if d}), reverse=True)

#     return render_template(
#         'expense.html',
#         expenses=expenses,
#         total_expense=total_expense,
#         total_vargani=total_vargani,
#         remaining=remaining,
#         selected_year=selected_year,
#         years=years
#     )


# @app.route("/delete_expense/<string:id>")
# def delete_expense(id):
#     db.expense.delete_one({"_id": ObjectId(id)})
#     return redirect('/expense')

# @app.route('/bhandi', methods=['GET'])
# @login_required
# def bhandi_form():
#     return render_template('bhandi.html') 

# @app.route('/submit_bhandi', methods=['POST'])
# @login_required
# def submit_bhandi():
#     receiver_name = request.form.get('receiver_name')
#     receiver_contact = request.form.get('receiver_contact')

    
#     bhande = [
#         'पातेले व झाकण ४ पायली', 'पातेले व झाकण ५ पायली', 'पातेले व झाकण ८ पायली', 'पातेले व झाकण ९ पायली',
#         'बॅरल', 'स्टील बकेट', 'प्लास्टिक बकेट', 'बस्कर', 'जग', 'वगराळे',
#         'बादली', 'चौफुला', 'शेगडी', 'प्लेटर', 'पळी'
#     ]

#     utensils = {}
#     for i, item in enumerate(bhande, start=1):
#         qty = request.form.get(f'quantity_{i}')
#         if qty and int(qty) > 0:
#             utensils[item] = int(qty)

#     data = {
#         'receiver_name': receiver_name,
#         'receiver_contact': receiver_contact,
#         'utensils': utensils,
#         'submitted_at': datetime.now()
#     }

#     collection.insert_one(data)

#     return redirect('/bhandi_list')  # Redirect to form or a success page


# @app.route('/bhandi_list')
# @login_required
# def bhandi_list():
#     entries = list(collection.find({'rent_paid': {'$ne': True}}).sort("submitted_at", -1))
#     return render_template("bhandi_list.html", entries=entries)


# @app.route('/mark_paid/<entry_id>', methods=['POST'])
# def mark_paid(entry_id):
#     rent_amount = request.form.get('rent_amount')
#     missing_description = request.form.get('missing_description', 'nil')
    
#     collection.update_one(
#         {'_id': ObjectId(entry_id)},
#         {'$set': {
#             'rent_paid': True,
#             'rent_amount': int(rent_amount),
#             'paid_at': datetime.now(),
#             'missing_description': missing_description
#         }}
#     )
#     return redirect('/paid_rent')



# @app.route('/delete_paid/<entry_id>', methods=['POST'])
# def delete_paid(entry_id):
#     collection.delete_one({'_id': ObjectId(entry_id), 'rent_paid': True})
#     return redirect('/paid_rent')

# @app.route('/delete_all_paid', methods=['POST'])
# def delete_all_paid():
#     collection.delete_many({'rent_paid': True})
#     return redirect('/paid_rent')

# @app.route('/download_paid_excel')
# def download_paid_excel():
#     paid_entries = list(collection.find({'rent_paid': True}))
#     data = [{
#         'नाव': e['receiver_name'],
#         'संपर्क': e.get('receiver_contact', ''),
#         'रक्कम': e['rent_amount'],
#         'हरवलेली भांडी': e.get('missing_description', 'Nil'),
#         'जमा तारीख': e.get('paid_at').strftime('%d-%m-%Y') if e.get('paid_at') else ''
        
#     } for e in paid_entries]

#     for item in data:
#         item.pop('_id', None)  # Remove MongoDB ID
#     df = pd.DataFrame(data)

#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         df.to_excel(writer, index=False, sheet_name='Bhandi_Bhade_List')

#     output.seek(0)
#     return send_file(output, download_name='Bhandi_Bhade_List.xlsx', as_attachment=True)

# # @app.route('/paid_rent')
# # def paid_rent():
# #     paid_entries = list(collection.find({'rent_paid': True}))
# #     total_amount = sum(entry.get('rent_amount', 0) for entry in paid_entries)
# #     return render_template("paid_rent.html", paid_entries=paid_entries, total_amount=total_amount)

# @app.route('/paid_rent')
# def paid_rent():
#     selected_year = request.args.get('year', datetime.now().year, type=int)

#     start_of_year = datetime(selected_year, 1, 1)
#     end_of_year = datetime(selected_year + 1, 1, 1)

#     paid_entries = list(collection.find({
#         'rent_paid': True,
#         'paid_at': {'$gte': start_of_year, '$lt': end_of_year}
#     }).sort("paid_at", -1))

#     total_amount = sum(entry.get('rent_amount', 0) for entry in paid_entries)

#     # Distinct years from paid_at field
#     all_paid_dates = collection.find({'rent_paid': True}, {'paid_at': 1})
#     years = sorted({e['paid_at'].year for e in all_paid_dates if 'paid_at' in e}, reverse=True)

#     return render_template("paid_rent.html", 
#         paid_entries=paid_entries, 
#         total_amount=total_amount, 
#         years=years,
#         selected_year=selected_year
#     )

# # @app.route('/toggle_aahaval', methods=['POST'])
# # @login_required
# # def toggle_aahaval():
# #     current = db.settings.find_one()
# #     if current:
# #         db.settings.update_one({}, {"$set": {"aahaval_visible": not current.get('aahaval_visible', False)}})
# #     else:
# #         db.settings.insert_one({"aahaval_visible": True})
# #     return redirect('/dashboard')
# @app.route('/toggle_aahaval', methods=['POST'])
# @login_required
# def toggle_aahaval():
#     visible = request.form.get('visible') == 'on'
#     db.settings.update_one({}, {'$set': {'aahaval_visible': visible}}, upsert=True)
#     return redirect('/dashboard')

# @app.route('/aahaval')
# def full_aahaval():
#     vargani_data = list(db.vargani.find().sort('amount', -1))
#     expense_data = list(db.expense.find().sort('created_at', -1))
#     total_vargani = sum(v['amount'] for v in vargani_data)
#     total_expense = sum(e['amount'] for e in expense_data)
#     remaining = total_vargani - total_expense
#     return render_template("aahaval.html", vargani_data=vargani_data, expense_data=expense_data,
#                            total_vargani=total_vargani, total_expense=total_expense, remaining=remaining)


# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, render_template, request, redirect, url_for, flash, session,send_file
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
import io
import requests
import unicodedata
from functools import lru_cache
from flask import jsonify, request

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
collection = db['bhandi_records']



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin')
        return f(*args, **kwargs)
    return decorated_function
@lru_cache(maxsize=2048)
def transliterate_google(text: str) -> str | None:
    """
    Hit Google Input Tools to get phonetic Marathi (Devanagari) for normal English text.
    Returns Devanagari string on success, or None on failure.
    """
    text = (text or "").strip()
    if not text:
        return None

    url = "https://inputtools.google.com/request"
    params = {
        "text": text,
        "itc": "mr-t-i0-und",  # Marathi transliteration keyboard
        "num": 1
    }

    try:
        resp = requests.get(url, params=params, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        # Data format may vary a bit so be defensive in parsing.
        # Try a few patterns, then fallback to finding first string recursively.
        candidate = None
        # Pattern-based tries:
        try:
            # common layout: ["SUCCESS", [[ "<orig>", [ [ "<candidate>", ... ] ] ]]]
            if isinstance(data, list) and len(data) > 1:
                # attempt pattern access
                candidate = data[1][0][1][0]
        except Exception:
            candidate = None

        # fallback: find first string anywhere in nested JSON
        if not candidate:
            def find_first_str(obj):
                if isinstance(obj, str) and obj.strip():
                    return obj
                if isinstance(obj, list):
                    for e in obj:
                        s = find_first_str(e)
                        if s:
                            return s
                if isinstance(obj, dict):
                    for v in obj.values():
                        s = find_first_str(v)
                        if s:
                            return s
                return None
            candidate = find_first_str(data)

        if candidate:
            # normalize and return
            return unicodedata.normalize("NFC", candidate)

    except Exception as e:
        # keep logs for debugging
        print("Transliteration request failed:", e)

    return None

@app.route('/_transliterate', methods=['POST'])
@login_required
def transliterate_api():
    payload = request.get_json(silent=True) or {}
    text = payload.get('text', '') or ''
    marathi = transliterate_google(text)
    # fallback: if not available, return original text (or empty)
    if not marathi:
        marathi = ''
    return jsonify({'marathi': marathi})


@app.route('/')
def homepage():
    settings = db.settings.find_one() or {}
    show_aahaval = settings.get("aahaval_visible", False)

    vargani_data = []
    expense_data = []
    total_vargani = 0
    total_expense = 0
    remaining = 0

    if show_aahaval:
        vargani_data = list(db.vargani.find())
        expense_data = list(db.expense.find())
        total_vargani = sum(v['amount'] for v in vargani_data)
        total_expense = sum(e['amount'] for e in expense_data)
        remaining = total_vargani - total_expense

    events = list(db.events.find().sort("event_date", -1))
    gallery = list(db.gallery.find().sort("_id", -1))[:10]

    return render_template(
        'index.html',
        events=events,
        gallery=gallery,
        show_aahaval=show_aahaval,
        vargani_data=vargani_data,
        expense_data=expense_data,
        total_vargani=total_vargani,
        total_expense=total_expense,
        remaining=remaining
    )


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = db.admin.find_one({'username': username, 'password': password})

        if admin:
            session['admin_logged_in'] = True
            return redirect('/dashboard')
        else:
            flash('Invalid credentials', 'error')  

    return render_template('admin_login.html')




@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/')


@app.route('/dashboard')
@login_required
def dashboard():
    settings = db.settings.find_one() or {}
    show_aahaval = settings.get('aahaval_visible', False)
    return render_template("admin_dashboard.html", show_aahaval=show_aahaval)




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
            # 'caption': request.form['caption'],
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



# @app.route('/submit_vargani', methods=['POST'])
# @login_required
# def submit_vargani():
#     name = request.form['name'].strip()
#     amount = int(request.form['amount'])
#     contact = request.form['contact'].strip()
#     now = datetime.now()
#     year = now.year

#     # ✅ Duplicate check
#     existing_entry = db.vargani.find_one({
#         'name': name,
#         'contact': contact,
#         'year': year
#     })

#     if existing_entry:
#         flash(f" ! '{name}' ची ₹{existing_entry['amount']} वर्गणी आधीच नोंदवली आहे.", 'error')
#         return redirect('/vargani')

#     # ✅ Save entry if not duplicate
#     db.vargani.insert_one({
#         'name': name,
#         'amount': amount,
#         'contact': contact,
#         'year': year,
#         'submitted_at': now
#     })

#     # ✅ Send SMS
#     sms_message = f"धन्यवाद आपली ₹{amount} वर्गणी प्राप्त झाली आहे. -18 House"
#     url = "https://www.fast2sms.com/dev/bulkV2"
#     payload = {
#         "sender_id": "FSTSMS",
#         "message": sms_message,
#         "language": "unicode",
#         "route": "q",
#         "numbers": contact
#     }
#     headers = {
#         "authorization": os.getenv("FAST2SMS_API_KEY"),
#         "Content-Type": "application/json"
#     }

#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         try:
#             data = response.json()
#             print("✅ SMS sent successfully:", data)
#         except ValueError:
#             print("❌ SMS response not JSON. Text was:", response.text)
#     except Exception as e:
#         print("🔥 SMS sending failed:", e)

#     flash("✅ वर्गणी यशस्वीरीत्या नोंदवली गेली आहे.")
#     return redirect('/vargani_list')



@app.route('/vargani_list')
@login_required
def vargani_list():
    selected_year = request.args.get('year', datetime.now().year, type=int)

    data = list(db.vargani.find({'year': selected_year}).sort("amount", -1))
    total = sum(item['amount'] for item in data)

    # Get distinct years for dropdown
    all_years = db.vargani.distinct('year')
    all_years.sort(reverse=True)

    return render_template('vargani_list.html',
                           vargani=data,
                           total=total,
                           selected_year=selected_year,
                           years=all_years)

# @app.route('/edit_vargani/<id>', methods=['GET', 'POST'])
# @login_required
# def edit_vargani(id):
#     if request.method == 'POST':
#         db.vargani.update_one(
#             {'_id': ObjectId(id)},
#             {'$set': {
#                 'name': request.form['name'],
#                 'amount': int(request.form['amount']),
#                 'contact': request.form['contact']
#             }}
#         )
#         return redirect('/vargani_list')
#     vargani = db.vargani.find_one({'_id': ObjectId(id)})
#     return render_template('edit_vargani.html', vargani=vargani)

@app.route('/submit_vargani', methods=['POST'])
@login_required
def submit_vargani():
    # original typed name (English)
    name_input = request.form.get('name', '').strip()

    # If client sends a precomputed marathi value (JS sets it), prefer that.
    name_marathi_from_client = request.form.get('name_marathi', '').strip()
    if name_marathi_from_client:
        name_marathi = name_marathi_from_client
    else:
        # Server-side transliteration (Google Input Tools)
        name_marathi = transliterate_google(name_input) or name_input  # fallback to original if translit fails

    amount = int(request.form['amount'])
    contact = request.form['contact'].strip()
    now = datetime.now()
    year = now.year

    # Duplicate check with Marathi-normalized name and contact
    existing_entry = db.vargani.find_one({
        'name': name_marathi,
        'contact': contact,
        'year': year
    })

    if existing_entry:
        flash(f" ! '{name_marathi}' ची ₹{existing_entry['amount']} वर्गणी आधीच नोंदवली आहे.", 'error')
        return redirect('/vargani')

    db.vargani.insert_one({
        'name_english': name_input,
        'name': name_marathi,
        'amount': amount,
        'contact': contact,
        'year': year,
        'submitted_at': now
    })

    #  ✅ Send SMS
    sms_message = f"धन्यवाद आपली ₹{amount} वर्गणी प्राप्त झाली आहे. -18 House"
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

    flash("✅ वर्गणी यशस्वीरीत्या नोंदवली गेली आहे.")
    return redirect('/vargani_list')





@app.route('/edit_vargani/<id>', methods=['GET', 'POST'])
@login_required
def edit_vargani(id):
    if request.method == 'POST':
        name_input = request.form.get('name', '').strip()
        name_marathi_from_client = request.form.get('name_marathi', '').strip()
        if name_marathi_from_client:
            name_marathi = name_marathi_from_client
        else:
            name_marathi = transliterate_google(name_input) or name_input

        db.vargani.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': name_marathi,
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
        item.pop('_id', None)  
    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Vargani_List')

    output.seek(0)
    return send_file(output, download_name='vargani_list.xlsx', as_attachment=True)


# @app.route('/expense', methods=['GET', 'POST'])
# @login_required
# def manage_expense():
#     selected_year = request.args.get('year', datetime.now().year, type=int)

#     if request.method == 'POST':
#         new_expense = {
#             "title": request.form['title'],
#             "amount": int(request.form['amount']),
#             "description": request.form['description'],
#             "created_at": datetime.utcnow()
#         }
#         db.expense.insert_one(new_expense)
#         return redirect(url_for('manage_expense', year=selected_year))  # preserve selected year on submit
    
    

#     # Filter expenses by selected year
#     start_of_year = datetime(selected_year, 1, 1)
#     end_of_year = datetime(selected_year + 1, 1, 1)
#     expenses = list(db.expense.find({
#         "created_at": {"$gte": start_of_year, "$lt": end_of_year}
#     }).sort("created_at", -1))
#     total_expense = sum(exp["amount"] for exp in expenses)

#     # Get vargani entries of selected year too
#     vargani_entries = list(db.vargani.find({'year': selected_year}))
#     total_vargani = sum(v["amount"] for v in vargani_entries)

#     remaining = total_vargani - total_expense

#     # Fetch all available years
#     all_years = db.expense.distinct("created_at")
#     years = sorted(list({d.year for d in all_years if d}), reverse=True)

#     return render_template(
#         'expense.html',
#         expenses=expenses,
#         total_expense=total_expense,
#         total_vargani=total_vargani,
#         remaining=remaining,
#         selected_year=selected_year,
#         years=years
#     )

@app.route('/expense', methods=['GET', 'POST'])
@login_required
def manage_expense():
    selected_year = request.args.get('year', datetime.now().year, type=int)

    if request.method == 'POST':
        # Get English title
        title_english = request.form.get('title', '').strip()
        dis_english = request.form.get('description', '').strip()

        # Prefer client-side Marathi transliteration if provided
        title_marathi_from_client = request.form.get('title_marathi', '').strip() 
        dis_marathi_from_client = request.form.get('dis_marathi', '').strip()
        if title_marathi_from_client and dis_marathi_from_client:
            title_marathi = title_marathi_from_client
            dis_marathi = dis_marathi_from_client
        else:
            # Server-side transliteration (same helper as vargani)
            title_marathi = transliterate_google(title_english) or title_english
            dis_marathi = transliterate_google(dis_english) or dis_english

        new_expense = {
            # "title_english": title_english,
            "title": title_marathi,
            "amount": int(request.form['amount']),
            "description": dis_marathi,
            # "description_eng": request.form['description'],
            "created_at": datetime.utcnow()
        }
        db.expense.insert_one(new_expense)
        return redirect(url_for('manage_expense', year=selected_year))  # preserve selected year on submit

    # Filter expenses by selected year
    start_of_year = datetime(selected_year, 1, 1)
    end_of_year = datetime(selected_year + 1, 1, 1)
    expenses = list(db.expense.find({
        "created_at": {"$gte": start_of_year, "$lt": end_of_year}
    }).sort("created_at", -1))
    total_expense = sum(exp["amount"] for exp in expenses)

    # Get vargani entries of selected year too
    vargani_entries = list(db.vargani.find({'year': selected_year}))
    total_vargani = sum(v["amount"] for v in vargani_entries)

    remaining = total_vargani - total_expense

    # Fetch all available years
    all_years = db.expense.distinct("created_at")
    years = sorted(list({d.year for d in all_years if d}), reverse=True)

    return render_template(
        'expense.html',
        expenses=expenses,
        total_expense=total_expense,
        total_vargani=total_vargani,
        remaining=remaining,
        selected_year=selected_year,
        years=years
    )

@app.route("/delete_expense/<string:id>")
def delete_expense(id):
    db.expense.delete_one({"_id": ObjectId(id)})
    return redirect('/expense')

@app.route('/bhandi', methods=['GET'])
@login_required
def bhandi_form():
    return render_template('bhandi.html') 

@app.route('/submit_bhandi', methods=['POST'])
@login_required
def submit_bhandi():
    receiver_name = request.form.get('receiver_name' , '').strip()
    receiver_contact = request.form.get('receiver_contact')

    
    bhande = [
        'पातेले व झाकण ४ पायली', 'पातेले व झाकण ५ पायली', 'पातेले व झाकण ८ पायली', 'पातेले व झाकण ९ पायली',
        'बॅरल', 'स्टील बकेट', 'प्लास्टिक बकेट', 'बस्कर', 'जग', 'वगराळे',
        'बादली', 'चौफुला', 'शेगडी', 'प्लेटर', 'पळी'
    ]

    utensils = {}
    for i, item in enumerate(bhande, start=1):
        qty = request.form.get(f'quantity_{i}')
        if qty and int(qty) > 0:
            utensils[item] = int(qty)

    receiver_name_marathi_from_client = request.form.get('receiver_name_marathi', '').strip()
    if receiver_name_marathi_from_client:
        receiver_name_marathi = receiver_name_marathi_from_client
    else:
       receiver_name_marathi = transliterate_google(receiver_name) or receiver_name

    data = {
        'receiver_name': receiver_name_marathi,
        'receiver_contact': receiver_contact,
        'utensils': utensils,
        'submitted_at': datetime.now()
    }

    collection.insert_one(data)

    return redirect('/bhandi_list')  # Redirect to form or a success page


@app.route('/bhandi_list')
@login_required
def bhandi_list():
    entries = list(collection.find({'rent_paid': {'$ne': True}}).sort("submitted_at", -1))
    return render_template("bhandi_list.html", entries=entries)


@app.route('/mark_paid/<entry_id>', methods=['POST'])
def mark_paid(entry_id):
    rent_amount = request.form.get('rent_amount')
    missing_description = request.form.get('missing_description', 'nil')
    
    collection.update_one(
        {'_id': ObjectId(entry_id)},
        {'$set': {
            'rent_paid': True,
            'rent_amount': int(rent_amount),
            'paid_at': datetime.now(),
            'missing_description': missing_description
        }}
    )
    return redirect('/paid_rent')



@app.route('/delete_paid/<entry_id>', methods=['POST'])
def delete_paid(entry_id):
    collection.delete_one({'_id': ObjectId(entry_id), 'rent_paid': True})
    return redirect('/paid_rent')

@app.route('/delete_all_paid', methods=['POST'])
def delete_all_paid():
    collection.delete_many({'rent_paid': True})
    return redirect('/paid_rent')

@app.route('/download_paid_excel')
def download_paid_excel():
    paid_entries = list(collection.find({'rent_paid': True}))
    data = [{
        'नाव': e['receiver_name'],
        'संपर्क': e.get('receiver_contact', ''),
        'रक्कम': e['rent_amount'],
        'हरवलेली भांडी': e.get('missing_description', 'Nil'),
        'जमा तारीख': e.get('paid_at').strftime('%d-%m-%Y') if e.get('paid_at') else ''
        
    } for e in paid_entries]

    for item in data:
        item.pop('_id', None)  # Remove MongoDB ID
    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Bhandi_Bhade_List')

    output.seek(0)
    return send_file(output, download_name='Bhandi_Bhade_List.xlsx', as_attachment=True)



@app.route('/paid_rent')
def paid_rent():
    selected_year = request.args.get('year', datetime.now().year, type=int)

    start_of_year = datetime(selected_year, 1, 1)
    end_of_year = datetime(selected_year + 1, 1, 1)

    paid_entries = list(collection.find({
        'rent_paid': True,
        'paid_at': {'$gte': start_of_year, '$lt': end_of_year}
    }).sort("paid_at", -1))

    total_amount = sum(entry.get('rent_amount', 0) for entry in paid_entries)

    # Distinct years from paid_at field
    all_paid_dates = collection.find({'rent_paid': True}, {'paid_at': 1})
    years = sorted({e['paid_at'].year for e in all_paid_dates if 'paid_at' in e}, reverse=True)

    return render_template("paid_rent.html", 
        paid_entries=paid_entries, 
        total_amount=total_amount, 
        years=years,
        selected_year=selected_year
    )


@app.route('/toggle_aahaval', methods=['POST'])
@login_required
def toggle_aahaval():
    visible = request.form.get('visible') == 'on'
    db.settings.update_one({}, {'$set': {'aahaval_visible': visible}}, upsert=True)
    return redirect('/dashboard')

@app.route('/aahaval')
def full_aahaval():
    vargani_data = list(db.vargani.find().sort('amount', -1))
    expense_data = list(db.expense.find().sort('created_at', -1))
    total_vargani = sum(v['amount'] for v in vargani_data)
    total_expense = sum(e['amount'] for e in expense_data)
    remaining = total_vargani - total_expense
    return render_template("aahaval.html", vargani_data=vargani_data, expense_data=expense_data,
                           total_vargani=total_vargani, total_expense=total_expense, remaining=remaining)

# Show registration page
@app.route("/events", methods=["GET", "POST"])
@login_required
def manage_events():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        event_date = request.form.get("event_date")

        # Image upload (mandatory)
        image_file = request.files.get("image")
        image_url, qr_url = None, None
        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result["secure_url"]

        # QR upload (only if paid)
        if "is_paid" in request.form:
            qr_file = request.files.get("qr")
            if qr_file:
                qr_upload = cloudinary.uploader.upload(qr_file)
                qr_url = qr_upload["secure_url"]

        new_event = {
            "title": title,
            "description": description,
            "event_date": event_date,
            "image_url": image_url,
            "registration_open": "registration_open" in request.form,  # ✅ Boolean
            "is_paid": "is_paid" in request.form,                      # ✅ Boolean
            "qr_url": qr_url,                                          # ✅ Only set if paid
            "upi_id": request.form.get("upi_id") if "is_paid" in request.form else None,
            "created_at": datetime.utcnow()
        }

        db.events.insert_one(new_event)
        print("✅ Saved Event:", new_event)   # <-- Debug log
        flash("✅ Event added successfully!")
        return redirect(url_for("manage_events"))

    events = list(db.events.find().sort("event_date", -1))
    return render_template("events_manage.html", events=events)

@app.route("/event_register/<string:id>", methods=["GET", "POST"])
def event_register(id):
    event = db.events.find_one({"_id": ObjectId(id)})
    if not event:
        flash("❌ Event not found")
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        mobile = request.form["mobile"]

        payment_id = None
        payment_ss_url = None

        if event.get("is_paid"):
            payment_id = request.form["payment_id"]
            payment_file = request.files["payment_ss"]
            upload_result = cloudinary.uploader.upload(payment_file)
            payment_ss_url = upload_result["secure_url"]

        registration = {
            "event_id": str(event["_id"]),
            "event_title": event["title"],
            "name": name,
            "address": address,
            "mobile": mobile,
            "payment_id": payment_id,
            "payment_ss": payment_ss_url,
            "created_at": datetime.utcnow()
        }
        db.event_registrations.insert_one(registration)
        flash("✅ Registration successful!")
        return redirect("/")

    return render_template("event_register.html", event=event)

@app.route("/delete_event/<id>")
@login_required
def delete_event(id):
    event = db.events.find_one({"_id": ObjectId(id)})
    if event:
        # Delete event image from Cloudinary (optional)
        if "image_url" in event:
            try:
                cloudinary.uploader.destroy(event.get("public_id"))
            except:
                pass
        # Delete QR code too
        if "qr_url" in event and event["qr_url"]:
            try:
                cloudinary.uploader.destroy(event["qr_url"])
            except:
                pass
        db.events.delete_one({"_id": ObjectId(id)})

    flash("🗑️ Event deleted.")
    return redirect(url_for("manage_events"))

# Page 1: Select Event
@app.route("/select_event")
@login_required
def select_event():
    events = list(db.events.find())
    return render_template("event_select.html", events=events)


# Page 2: Registrations List for Selected Event
@app.route("/event_registrations/<event_id>")
@login_required
def event_registrations(event_id):
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if not event:
        flash("❌ Event not found")
        return redirect(url_for("select_event"))

    registrations = list(db.event_registrations.find({"event_id": event_id}))
    return render_template("event_lists.html", event=event, registrations=registrations)

@app.route('/delete_registration/<reg_id>/<event_id>', methods=['POST'])
@login_required
def delete_registration(reg_id, event_id):
    try:
        db.event_registrations.delete_one({"_id": ObjectId(reg_id)})
        flash("🗑️ Registration deleted successfully!", "success")
    except Exception as e:
        flash(f"❌ Error deleting registration: {e}", "danger")

    return redirect(url_for('event_registrations', event_id=event_id))


if __name__ == '__main__':
    app.run(debug=True)
