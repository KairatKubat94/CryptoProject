"""
Flask приложение для визуализации алгоритмов шифрования
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from crypto_algorithms import CaesarCipher, AESCipher, RSACipher
import json

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    """Возвращает информацию о всех алгоритмах"""
    return jsonify({
        'caesar': CaesarCipher.get_info(),
        'aes': AESCipher.get_info(),
        'rsa': RSACipher.get_info()
    })


@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    """Шифрует текст методом Caesar"""
    data = request.json
    text = data.get('text', '')
    shift = data.get('shift', 3)
    
    if not text:
        return jsonify({'error': 'Текст не может быть пустым'}), 400
    
    try:
        result = CaesarCipher.encrypt(text, shift)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    """Расшифровывает текст методом Caesar"""
    data = request.json
    text = data.get('text', '')
    shift = data.get('shift', 3)
    
    if not text:
        return jsonify({'error': 'Текст не может быть пустым'}), 400
    
    try:
        result = CaesarCipher.decrypt(text, shift)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/aes/encrypt', methods=['POST'])
def aes_encrypt():
    """Шифрует текст методом AES"""
    data = request.json
    text = data.get('text', '')
    password = data.get('password', '')
    
    if not text or not password:
        return jsonify({'error': 'Текст и пароль обязательны'}), 400
    
    try:
        result = AESCipher.encrypt(text, password)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/aes/decrypt', methods=['POST'])
def aes_decrypt():
    """Расшифровывает текст методом AES"""
    data = request.json
    encrypted = data.get('encrypted', '')
    password = data.get('password', '')
    
    if not encrypted or not password:
        return jsonify({'error': 'Зашифрованный текст и пароль обязательны'}), 400
    
    try:
        result = AESCipher.decrypt(encrypted, password)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rsa/generate-keys', methods=['POST'])
def rsa_generate_keys():
    """Генерирует пару ключей RSA"""
    data = request.json
    key_size = data.get('key_size', 2048)
    
    try:
        result = RSACipher.generate_keys(key_size)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    """Шифрует текст методом RSA"""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'Текст не может быть пустым'}), 400
    
    try:
        result = RSACipher.encrypt(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rsa/info', methods=['GET'])
def rsa_info():
    """Информация о RSA"""
    return jsonify(RSACipher.get_info())


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Страница не найдена'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
