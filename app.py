from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "heli@19382",
    "database": "CAPSTONEPROJECT"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    try:
        full_name = request.form.get("full_name")
        event_name = request.form.get("event_name")
        email = request.form.get("email")

        if not full_name or not event_name:
            return jsonify({
                "success": False,
                "message": "Full Name and Event Type are required."
            }), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
            INSERT INTO registrations (full_name, event_name, email)
            VALUES (%s, %s, %s)
        """
        values = (full_name, event_name, email)
        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Registration submitted successfully!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)