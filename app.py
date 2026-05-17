import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

FILE_DU_LIEU = "taikhoan.txt"

def doc_danh_sach_tai_khoan():
    danh_sach = {}
    if not os.path.exists(FILE_DU_LIEU):
        with open(FILE_DU_LIEU, "w", encoding="utf-8") as f:
            f.write("admin:123456\n")
        return {"admin": "123456"}
    
    with open(FILE_DU_LIEU, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and ":" in line:
                user, pas = line.split(":", 1)
                danh_sach[user] = pas
    return danh_sach

def luu_tai_khoan_moi(username, password):
    with open(FILE_DU_LIEU, "a", encoding="utf-8") as f:
        f.write(f"{username}:{password}\n")

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_input = request.form.get('username').strip()
    pass_input = request.form.get('password')
    
    danh_sach_tk = doc_danh_sach_tai_khoan()
    
    if user_input in danh_sach_tk and danh_sach_tk[user_input] == pass_input:
        return redirect(url_for('soikeo'))
    else:
        loi = "Sai tài khoản hoặc mật khẩu, vui lòng thử lại!"
        return render_template('login.html', error=loi)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_new = request.form.get('username').strip()
        pass_new = request.form.get('password')
        confirm_pass = request.form.get('confirm_password')

        danh_sach_tk = doc_danh_sach_tai_khoan()

        if user_new in danh_sach_tk:
            return render_template('register.html', error="Tài khoản này đã tồn tại!")
        if pass_new != confirm_pass:
            return render_template('register.html', error="Mật khẩu xác nhận không trùng khớp!")
        if len(pass_new) < 6:
            return render_template('register.html', error="Mật khẩu phải có ít nhất 6 ký tự!")

        luu_tai_khoan_moi(user_new, pass_new)
        return render_template('register.html', success="Đăng ký thành công! Hãy quay lại LOGIN.")

    return render_template('register.html')

@app.route('/soikeo')
def soikeo():
    cac_tran_dau = [
        {"thoi_gian": "2:00", "chu_nha": "Man United", "khach": "Liverpool", "keo_asia": "Liverpool -0.75", "tai_xiu": "3.0", "ai_du_doan": "NẰM XỈU (84%)"},
        {"thoi_gian": "00:30", "chu_nha": "Arsenal", "khach": "Chelsea", "keo_asia": "Arsenal -1.25", "tai_xiu": "2.75", "ai_du_doan": "ARSENAL (78%)"},
        {"thoi_gian": "02:45", "chu_nha": "Real Madrid", "khach": "Barcelona", "keo_asia": "0 : 0", "tai_xiu": "3.25", "ai_du_doan": "NẰM TÀI (91%)"}
    ]
    return render_template('soikeo.html', danh_sach_tran=cac_tran_dau)

if __name__ == '__main__':
    app.run(debug=True, port=8080)