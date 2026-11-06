from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

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
        .section { background: white; color: #111; padding: 40px 20px; max-width: 900px; margin: 20px auto; border-radius: 12px; }
        .card { background: #f8f8f8; border: 1px solid #ddd; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .card h3 { margin-top: 0; }
        .price { color: green; font-weight: bold; }
        input, select { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        button { background: #ffcc00; border: none; padding: 15px; width: 100%; font-weight: bold; font-size: 16px; border-radius: 6px; cursor: pointer; }
        .tennis-box { background: #e8f5e9; border-left: 5px solid green; padding: 15px; border-radius: 8px; margin-top: 15px; }
        .footer { text-align: center; padding: 30px; color: #ccc; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>COACH SOLOMON</h1>
        <h2>Your Coach. Your Growth. Your Next Level.</h2>
        <p>Rongai, Nairobi | Online Worldwide | 5.0 Stars</p>
        <a class="btn" href="#sessions">Book A Session</a>
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
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, sessions=sessions, registrations=registrations)

@app.route('/book', methods=['POST'])
def book():
    session_id = int(request.form.get('session_id'))
    session = next((s for s in sessions if s['id'] == session_id), None)
    registrations.append({
        'name': request.form.get('name'),
        'phone': request.form.get('phone'),
        'location': request.form.get('location'),
        'session_title': session['title'] if session else 'Unknown'
    })
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)