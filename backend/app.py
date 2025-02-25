from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_portfolio():
    try:
        with open("portfolio.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()