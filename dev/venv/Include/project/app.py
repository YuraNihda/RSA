from flask import Flask, request, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Розширений алгоритм Евкліда
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = egcd(b, a % b)
    return d, y, x - (a // b) * y

# Функція Ейлера
def eiler_fun(a, b):
    return (a - 1) * (b - 1)

# Перевірка на просте число
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Модульна обернена
def modinv(a, m):
    gcd, x, _ = egcd(a, m)
    if gcd != 1:
        raise Exception("Оберненого не існує")
    return x % m

# Генерація ключів RSA
def generate_keys():
    p, q = 61, 53  # Простi числа
    n = p * q
    phi = eiler_fun(p, q)
    e = 17  # Вибрано взаємно просте до phi
    d = modinv(e, phi)
    return (e, n), (d, n)

# Шифрування
def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

# Розшифрування
def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

# Створення ключів один раз
public_key, private_key = generate_keys()

@app.route('/', methods=['GET', 'POST'])
def index():
    encrypted_text = ''
    decrypted_text = ''
    file_name = None

    if request.method == 'POST':
        action = request.form.get('action')  # "encrypted" або "decrypted"
        text_data = request.form.get('text')
        file_data = request.files.get('file')

        if action == 'encrypt' and text_data:
            encrypted = encrypt(text_data, public_key)
            encrypted_text = ' '.join(map(str, encrypted))

        elif action == 'decrypt' and text_data:
            try:
                numbers = list(map(int, text_data.strip().split()))
                decrypted = decrypt(numbers, private_key)
                decrypted_text = decrypted
            except Exception as e:
                decrypted_text = f"Помилка при розшифруванні: Введіть коректні символи"

        if file_data and file_data.filename:
            file_path = os.path.join(UPLOAD_FOLDER, file_data.filename)
            file_data.save(file_path)
            file_name = file_data.filename

    return render_template('index.html',
                           encrypted=encrypted_text,
                           decrypted=decrypted_text,
                           file=file_name)

if __name__ == '__main__':
    app.run(debug=True)
