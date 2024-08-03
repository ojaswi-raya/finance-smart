from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Dummy database for demonstration
users_db = {}
feedback_db = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users_db.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if username in users_db:
            flash('Username already exists.')
        else:
            users_db[username] = {'password': hashed_password}
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/financial_tips')
def financial_tips():
    tips = {
        "Budgeting Tips": ["Create a monthly budget", "Track your expenses", "Set financial goals"],
        "Saving Strategies": ["Automate savings", "Use savings apps", "Find high-interest savings accounts"],
        "Investment Advice": ["Start investing early", "Diversify your investments", "Consult a financial advisor"],
        "Debt Management": ["Create a debt repayment plan", "Prioritize high-interest debts", "Consider debt consolidation"],
        "Income Generation": ["Freelancing", "Side gigs", "Passive income streams"]
    }
    return render_template('financial_tips.html', tips=tips)

@app.route('/scholarships')
def scholarships():
    scholarships = [
        {"name": "Scholarship 1", "description": "Description of Scholarship 1"},
        {"name": "Scholarship 2", "description": "Description of Scholarship 2"},
    ]
    return render_template('scholarships.html', scholarships=scholarships)

@app.route('/calculators')
def calculators():
    return render_template('calculators.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        comments = request.form.get('comments')
        feedback_db.append({"name": name, "comments": comments})
        flash('Feedback submitted successfully.')
        return redirect(url_for('feedback'))
    
    return render_template('feedback.html', feedback=feedback_db)

if __name__ == "__main__":
    app.run(debug=True)
