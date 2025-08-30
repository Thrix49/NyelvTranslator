from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------- Codexian mapping ----------
codexian = {
    "a": "7", "b": "37", "c": "8", "d": "65", "e": "3", "f": "46",
    "g": "5", "h": "2", "i": "0", "j": "91", "k": "20", "l": "47",
    "m": "11", "n": "12", "o": "13", "p": "14", "q": "15", "r": "16",
    "s": "17", "t": "18", "u": "19", "v": "21", "w": "22", "x": "23",
    "y": "24", "z": "25",
    "0": "203", "1": "214", "2": "225", "3": "236", "4": "247",
    "5": "258", "6": "269", "7": "280", "8": "291", "9": "302",
    " ": "99",
    "?": "517", ",": "684", ".": "729", "'": "845", '"': "906",
    "@": "392", "&": "478", "$": "563", ")": "821", "(": "742",
    ";": "655", ":": "834", "/": "903", "-": "776", "[": "512",
    "]": "624", "{": "871", "}": "958", "#": "439", "%": "627",
    "^": "713", "*": "894", "+": "550", "=": "688", "_": "799",
    "\\": "941", "|": "860", "~": "732", "<": "519", ">": "640",
    "€": "875", "£": "921", "¥": "999", "•": "888"
}

reverse_codexian = {v: k for k, v in codexian.items()}

# ---------- Translation functions ----------
def encode_text(text):
    result = ""
    for char in text:
        char_lower = char.lower()
        if char_lower in codexian:
            result += codexian[char_lower]
        else:
            result += char
    return result

def decode_text(code):
    i = 0
    result = ""
    while i < len(code):
        found = False
        for length in [3,2,1]:
            piece = code[i:i+length]
            if piece in reverse_codexian:
                result += reverse_codexian[piece]
                i += length
                found = True
                break
        if not found:
            result += code[i]
            i += 1
    return result

# ---------- Routes ----------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text","")
    direction = data.get("direction","encode")
    if direction == "encode":
        return jsonify({"result": encode_text(text)})
    else:
        return jsonify({"result": decode_text(text)})

if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
