from flask import Flask, request, redirect, url_for, render_template_string
import urllib.parse
import os

app = Flask(__name__)

COACH_WHATSAPP = "254746150576"
MPESA_NUMBER = "0746150576"

sessions = [
    {"id": 1, "title": "1-on-1 Life Coaching", "desc": "Personal coaching to help you get clarity, set goals and take action in your life.", "price": "KES 3,000", "duration": "60 mins"},
    {"id": 2, "title": "Business & Freelancing Coaching", "desc": "Learn how to start, grow and make money from your business or freelancing skills.", "price": "KES 3,000", "duration": "60 mins"},
    {"id": 3, "title": "Mindset & Confidence Coaching", "desc": "Build unshakeable confidence, overcome fear and develop a winning mindset.", "price": "KES 3,000", "duration": "60 mins"},
    {"id": 4, "title": "Group Coaching - Weekly", "desc": "Join a powerful group of people growing together every week. Learn, share and stay accountable.", "price": "KES 1,500", "duration": "90 mins"},
    {"id": 5, "title": "Tennis Coaching - Learn to Play Tennis", "desc": "Learn tennis from scratch or level up your game. ALL LEVELS welcome - Beginner, Intermediate and Advanced. Fun, patient coaching on technique, footwork, serve, rally and match confidence.", "price": "KES 500", "duration": "60 mins"},
]

registrations = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Coach Solomon</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #0a0f2e; color: white; }
        .hero { text-align: center; padding: 60px 20px; background: #0a0f2e; }
        .hero h1 { font-size: 48px; color: #ffcc00; margin: 0; }
        .hero h2 { font-size: 22px; }
        .btn { background: #ffcc00; color: black; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 8px; display: inline-block; margin-top: 15px; }
        .wa-btn { background: #25D366; color: white; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 8px; display: inline-block; margin-top: 15px; }
        .section { background: white; color: #111; padding: 40px 20px; max-width: 900px; margin: 20px auto; border-radius: 12px; }
        .card { background: #f8f8f8; border: 1px solid #ddd; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .card h3 { margin-top: 0; }
        .price { color: green; font-weight: bold; }
        input, select { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        button { background: #ffcc00; border: none; padding: 15px; width: 100%; font-weight: bold; font-size: 16px; border-radius: 6px; cursor: pointer; }
        .tennis-box { background: #e8f5e9; border-left: 5px solid green; padding: 15px; border-radius: 8px; margin-top: 15px; }
        .mpesa-box { background: #e8f5e9; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; }
        .footer { text-align: center; padding: 30px; color: #ccc; }
        .success-box { background: #e8f5e9; padding: 25px; border-radius: 10px; text-align: center; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>COACH SOLOMON</h1>
        <h2>Your Coach. Your Growth. Your Next Level.</h2>
        <p>Rongai, Nairobi | Online Worldwide | 5.0 Stars</p>
        <a class="btn" href="#sessions">Book A Session</a><br>
        <a class="wa-btn" href="https://wa.me/254746150576?text=Hi%20Coach%20Solomon%2C%20I%20want%20to%20book%20a%20session" target="_blank">Chat on WhatsApp</a>
    </div>

    <div class="section">
        <h2>About Coach Solomon</h2>
        <p>Hi, I am Solomon - Life Coach, Business Coach and Tennis Coach based in Rongai, Nairobi.</p>
        <p>I help people build confidence, grow their business, improve their mindset, and become the best version of themselves - on and off the court.</p>
        <div class="tennis-box">
            <h3>Tennis Coaching - ALL LEVELS</h3>
            <p>I teach Tennis for ALL levels - Beginner, Intermediate and Advanced.</p>
            <p>Never held a racket before? I will teach you from zero. Already playing? I will help you fix your technique, improve your serve, footwork and win more matches.</p>
            <p><b>Training Locations:</b><br>
            Karen<br>
            Absa Ground<br>
            Muthale Academy<br>
            Or at your preferred location - I come to you!</p>
            <p>Private 1-on-1 tennis lessons, group lessons, and kids coaching available.</p>
        </div>
        <div class="mpesa-box">
            <b>Pay via M-Pesa</b><br>
            Send to: <b>0746150576</b> - Solomon<br>
            Send screenshot on WhatsApp after payment
        </div>
    </div>

    <div class="section" id="sessions">
        <h2>Choose Your Session</h2>
        {% for s in sessions %}
        <div class="card">
            <h3>{{ s.title }}</h3>
            <p>{{ s.desc }}</p>
            <p>{{ s.duration }} | <span class="price">{{ s.price }}</span></p>
            <form method="POST" action="/book">
                <input type="hidden" name="session_id" value="{{ s.id }}">
                <input type="text" name="name" placeholder="Your Full Name" required>
                <input type="text" name="phone" placeholder="Phone / WhatsApp" required>
                <select name="location">
                    <option value="Online">Online</option>
                    <option value="Rongai">Rongai</option>
                    <option value="Karen">Karen - Tennis</option>
                    <option value="Absa Ground">Absa Ground - Tennis</option>
                    <option value="Muthale Academy">Muthale Academy - Tennis</option>
                    <option value="My Preferred Location">My Preferred Location</option>
                </select>
                <button type="submit">Register For This Session</button>
            </form>
        </div>
        {% endfor %}
    </div>

    <div class="section">
        <h2>Already Registered? ({{ registrations|length }} Clients)</h2>
        {% if registrations %}
            {% for r in registrations %}
            <p>{{ r.name }} - {{ r.session_title }} ({{ r.location }}) - {{ r.phone }}</p>
            {% endfor %}
        {% else %}
            <p>No registrations yet. Be the first!</p>
        {% endif %}
    </div>

    <div class="footer">
        <p>Coach Solomon | Rongai, Nairobi | Tennis in Karen, Absa Ground, Muthale Academy and Your Location</p>
        <p>WhatsApp: 0746150576 | M-Pesa: 0746150576</p>
    </div>
</body>
</html>
"""

SUCCESS_HTML = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Booking Received</title>
<style>body{font-family:Arial;background:#0a0f2e;margin:0;padding:20px} .box{max-width:500px;margin:auto;background:white;padding:25px;border-radius:12px;text-align:center;color:#111} .wa-btn{display:block;background:#25D366;color:white;padding:16px;border-radius:10px;text-decoration:none;font-weight:bold;margin-top:20px} .back{display:block;margin-top:15px;color:#111}</style>
</head>
<body><div class="box">
<h2>Booking Received!</h2>
<p><b>{{ name }}</b><br>{{ session_title }}<br>{{ location }}<br>{{ phone }}</p>
<p>Tap below to confirm on WhatsApp so Coach Solomon sees it instantly:</p>
<a class="wa-btn" href="{{ wa_link }}" target="_blank">Confirm on WhatsApp</a>
<p style="margin-top:20px;">Step 2: Pay via M-Pesa to <b>0746150576</b><br>Then send screenshot on WhatsApp</p>
<a class="back" href="/">Back to Home</a>
</div></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, sessions=sessions, registrations=registrations)

@app.route('/book', methods=['POST'])
def book():
    session_id = int(request.form.get('session_id'))
    session = next((s for s in sessions if s['id'] == session_id), None)
    name = request.form.get('name')
    phone = request.form.get('phone')
    location = request.form.get('location')
    session_title = session['title'] if session else 'Unknown'
    registrations.append({'name': name, 'phone': phone, 'location': location, 'session_title': session_title})
    message = "Hi Coach Solomon, I just booked! Name: " + str(name) + " Phone: " + str(phone) + " Session: " + str(session_title) + " Location: " + str(location) + " Please confirm. I will send M-Pesa screenshot."
    wa_link = "https://wa.me/" + COACH_WHATSAPP + "?text=" + urllib.parse.quote(message)
    return render_template_string(SUCCESS_HTML, name=name, phone=phone, location=location, session_title=session_title, wa_link=wa_link)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)