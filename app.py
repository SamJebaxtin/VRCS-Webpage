from flask import Flask, render_template, request, jsonify
import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)

app = Flask(__name__)

DEFAULT_SAVE_PATH = r"\\kor2fs03\V-V--Testing$\03_Validation_Software\VRCS_GUI"
os.makedirs(DEFAULT_SAVE_PATH, exist_ok=True)

if not os.path.exists(DEFAULT_SAVE_PATH):
    os.makedirs(DEFAULT_SAVE_PATH)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_file', methods=['POST'])
def create_file():
    data = request.json
    filename = f"{data['firstName']}_{data['lastName']}.txt"
    filepath = os.path.join(DEFAULT_SAVE_PATH, filename)

    lines = []
    for i in range(1, data['acCount'] + 1):
        lines.append(f"AC {i}: OFF")
    for i in range(1, data['dcCount'] + 1):
        lines.append(f"DC {i}: OFF")

    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))

    return jsonify(success=True, filename=filename, content=lines)


@app.route('/open_file', methods=['POST'])
def open_file():
    content = request.json['content']
    filename = request.json['filename']
    filepath = os.path.join(DEFAULT_SAVE_PATH, filename)

    try:
        # Save content to file
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"File content saved: {filename}")  # Debugging line
        lines = content.strip().split('\n')  # Split the content into lines
        return jsonify(success=True, lines=lines)
    except Exception as e:
        print(f"Error while saving file: {e}")  # Debugging line
        return jsonify(success=False, error=str(e))




@app.route('/toggle', methods=['POST'])
def toggle():
    filename = request.json['filename']
    index = request.json['index']
    filepath = os.path.join(DEFAULT_SAVE_PATH, filename)

    try:
        with open(filepath, 'r') as f:
            lines = f.read().splitlines()

        label, state = lines[index].split(": ")
        new_state = "OFF" if state == "ON" else "ON"
        lines[index] = f"{label}: {new_state}"

        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))

        return jsonify(success=True, updated=lines)
    except Exception as e:
        return jsonify(success=False, error=str(e))


if __name__ == '__main__':
    app.run(debug=True)
