from flask import Flask, request, jsonify, render_template
import unicodedata

app = Flask(__name__)

# ------------------------- MAPPINGS -------------------------
letters_lower = "abcdefghijklmnopqrstuvwxyz"
letters_upper = letters_lower.upper()

char_to_num = {}
for i,ch in enumerate(letters_lower):
    char_to_num[ch] = f"{i+1:02d}"
for i,ch in enumerate(letters_upper):
    char_to_num[ch] = f"{i+27:02d}"
for i in range(10):
    char_to_num[str(i)] = f"{i+53:02d}"
symbols = ["?","/",",",".","'","\"","@","&","$","(",")",";","-",":",
           "[","]","{","}","#","%","^","*","+","=","_","\\","|","~","<",">","€","£","¥","•"]
for i,s in enumerate(symbols):
    char_to_num[s] = f"{i+63:02d}"
char_to_num[" "] = "99"

num_to_char = {v:k for k,v in char_to_num.items()}

# ------------------------- FUNCTIONS -------------------------
def text_to_numbers(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = (text.replace("ą","a").replace("ć","c").replace("ę","e").replace("ł","l")
                .replace("ń","n").replace("ó","o").replace("ś","s").replace("ź","z")
                .replace("ż","z")
                .replace("Ą","A").replace("Ć","C").replace("Ę","E").replace("Ł","L")
                .replace("Ń","N").replace("Ó","O").replace("Ś","S").replace("Ź","Z")
                .replace("Ż","Z"))
    return "".join(char_to_num.get(ch,"") for ch in text)

def numbers_to_text(s: str) -> str:
    i, n = 0, len(s)
    res = []
    while i < n:
        code = s[i:i+2]  # fixed 2-digit mapping
        if code in num_to_char:
            res.append(num_to_char[code])
        i += 2
    return "".join(res)

# ------------------------- ROUTES -------------------------
@app.route("/")
def index():
    return render_template("index.html")  # frontend HTML

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text","")
    direction = data.get("direction","encode")  # "encode" or "decode"
    if direction=="encode":
        return jsonify({"result": text_to_numbers(text)})
    else:
        return jsonify({"result": numbers_to_text(text)})

if __name__=="__main__":
    app.run(debug=True)
