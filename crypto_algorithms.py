"""
Модуль визуализации алгоритмов шифрования
Caesar, AES, RSA с пошаговым объяснением
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import base64


class CaesarCipher:
    """Шифр Цезаря - простой шифр подстановки"""
    
    @staticmethod
    def encrypt(text, shift=3):
        """Шифрует текст со смещением"""
        result = []
        steps = []
        
        for i, char in enumerate(text):
            if char.isalpha():
                # Определяем, прописная или строчная буква
                if char.isupper():
                    base = ord('A')
                    shifted = (ord(char) - base + shift) % 26
                    encrypted_char = chr(base + shifted)
                else:
                    base = ord('a')
                    shifted = (ord(char) - base + shift) % 26
                    encrypted_char = chr(base + shifted)
                
                result.append(encrypted_char)
                steps.append({
                    'step': i + 1,
                    'original': char,
                    'code': ord(char),
                    'shift_by': shift,
                    'new_code': ord(encrypted_char),
                    'encrypted': encrypted_char,
                    'explanation': f"Буква '{char}' → смещение на {shift} → '{encrypted_char}'"
                })
            else:
                result.append(char)
                steps.append({
                    'step': i + 1,
                    'original': char,
                    'encrypted': char,
                    'explanation': f"Символ '{char}' не меняется (не буква)"
                })
        
        return {
            'encrypted': ''.join(result),
            'steps': steps,
            'summary': f"Caesar cipher с смещением {shift}"
        }
    
    @staticmethod
    def decrypt(text, shift=3):
        """Расшифровывает текст со смещением"""
        return CaesarCipher.encrypt(text, -shift)
    
    @staticmethod
    def get_info():
        return {
            'name': 'Шифр Цезаря',
            'description': 'Каждая буква смещается на фиксированное количество позиций в алфавите.',
            'key': 'Смещение (обычно 3)',
            'complexity': 'Очень низкая - легко подбирается перебором (26 вариантов)',
            'example': 'A → D, B → E, C → F при смещении 3'
        }


class AESCipher:
    """Симметричный шифр AES (Advanced Encryption Standard)"""
    
    @staticmethod
    def encrypt(text, password):
        """Шифрует текст с использованием AES (через Fernet)"""
        # Генерируем ключ из пароля
        key = base64.urlsafe_b64encode(password.encode().ljust(32)[:32])
        cipher = Fernet(key)
        
        # Кодируем текст
        text_bytes = text.encode()
        encrypted = cipher.encrypt(text_bytes)
        encrypted_b64 = encrypted.decode()
        
        steps = [
            {
                'step': 1,
                'phase': 'Подготовка',
                'explanation': f"Исходный текст: '{text}' ({len(text)} символов)"
            },
            {
                'step': 2,
                'phase': 'Генерация ключа',
                'explanation': f"Пароль '{password}' преобразуется в 256-битный ключ"
            },
            {
                'step': 3,
                'phase': 'Инициализация',
                'explanation': 'Создается IV (вектор инициализации) случайно'
            },
            {
                'step': 4,
                'phase': 'Шифрование',
                'explanation': 'Текст разбивается на блоки по 128 бит и каждый блок шифруется отдельно'
            },
            {
                'step': 5,
                'phase': 'Кодирование',
                'explanation': f"Зашифрованные данные кодируются в Base64\nРезультат: {encrypted_b64[:50]}..."
            }
        ]
        
        return {
            'encrypted': encrypted_b64,
            'steps': steps,
            'summary': 'AES-256 (симметричное шифрование)',
            'can_decrypt': True,
            'key': key.decode()
        }
    
    @staticmethod
    def decrypt(encrypted_text, password):
        """Расшифровывает текст AES"""
        try:
            key = base64.urlsafe_b64encode(password.encode().ljust(32)[:32])
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_text.encode())
            
            steps = [
                {
                    'step': 1,
                    'phase': 'Зашифрованные данные',
                    'explanation': f"Base64: {encrypted_text[:50]}..."
                },
                {
                    'step': 2,
                    'phase': 'Декодирование',
                    'explanation': 'Данные преобразуются из Base64'
                },
                {
                    'step': 3,
                    'phase': 'Восстановление ключа',
                    'explanation': f"Пароль '{password}' преобразуется в тот же 256-битный ключ"
                },
                {
                    'step': 4,
                    'phase': 'Расшифрование',
                    'explanation': 'Каждый блок расшифровывается с использованием ключа'
                },
                {
                    'step': 5,
                    'phase': 'Результат',
                    'explanation': f"Исходный текст восстановлен: '{decrypted.decode()}'"
                }
            ]
            
            return {
                'decrypted': decrypted.decode(),
                'steps': steps,
                'summary': 'AES-256 расшифрование'
            }
        except Exception as e:
            return {
                'error': f'Ошибка расшифрования: {str(e)}',
                'steps': []
            }
    
    @staticmethod
    def get_info():
        return {
            'name': 'AES (Advanced Encryption Standard)',
            'description': 'Симметричный алгоритм, где один ключ используется для шифрования и расшифрования.',
            'key': 'Пароль (преобразуется в 256-битный ключ)',
            'complexity': 'Очень высокая - стандарт для защиты данных',
            'block_size': '128 бит',
            'key_sizes': '128, 192, 256 бит',
            'use_case': 'Защита файлов, общие ключи для шифрования'
        }


class RSACipher:
    """Асимметричный шифр RSA (Rivest-Shamir-Adleman)"""
    
    @staticmethod
    def generate_keys(key_size=2048):
        """Генерирует пару ключей RSA"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
        )
        public_key = private_key.public_key()
        
        steps = [
            {
                'step': 1,
                'phase': 'Выбор простых чисел',
                'explanation': f'Выбираются два больших простых числа p и q (размер ключа: {key_size} бит)'
            },
            {
                'step': 2,
                'phase': 'Расчет n',
                'explanation': 'n = p × q (это число будет в обоих ключах)'
            },
            {
                'step': 3,
                'phase': 'Расчет функции Эйлера',
                'explanation': 'φ(n) = (p-1) × (q-1)'
            },
            {
                'step': 4,
                'phase': 'Выбор открытого показателя e',
                'explanation': 'e = 65537 (стандартное значение, взаимно просто с φ(n))'
            },
            {
                'step': 5,
                'phase': 'Расчет секретного показателя d',
                'explanation': 'd рассчитывается так, что e × d ≡ 1 (mod φ(n))'
            },
            {
                'step': 6,
                'phase': 'Формирование ключей',
                'explanation': 'Открытый ключ: (e, n) | Секретный ключ: (d, n)'
            }
        ]
        
        return {
            'public_key_generated': True,
            'private_key_generated': True,
            'key_size': key_size,
            'steps': steps,
            'summary': f'RSA пара ключей {key_size} бит'
        }
    
    @staticmethod
    def encrypt(text):
        """Шифрует текст с использованием RSA"""
        # Генерируем ключи
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        
        # Шифруем
        text_bytes = text.encode()
        encrypted = public_key.encrypt(
            text_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted_hex = encrypted.hex()
        
        steps = [
            {
                'step': 1,
                'phase': 'Генерация пары ключей',
                'explanation': 'Создаются открытый и секретный ключи (2048 бит)'
            },
            {
                'step': 2,
                'phase': 'Подготовка текста',
                'explanation': f"Текст '{text}' преобразуется в байты"
            },
            {
                'step': 3,
                'phase': 'Добавление padding',
                'explanation': 'Применяется OAEP padding для безопасности'
            },
            {
                'step': 4,
                'phase': 'Шифрование открытым ключом',
                'explanation': 'Каждый блок шифруется по формуле: C = M^e mod n'
            },
            {
                'step': 5,
                'phase': 'Кодирование результата',
                'explanation': f"Зашифрованные данные: {encrypted_hex[:50]}..."
            }
        ]
        
        return {
            'encrypted': encrypted_hex,
            'steps': steps,
            'summary': 'RSA шифрование открытым ключом',
            'key_size': 2048
        }
    
    @staticmethod
    def get_info():
        return {
            'name': 'RSA (Rivest-Shamir-Adleman)',
            'description': 'Асимметричный алгоритм - разные ключи для шифрования и расшифрования.',
            'key': 'Пара ключей (открытый и секретный)',
            'complexity': 'Очень высокая - сложность основана на факторизации больших чисел',
            'public_key_uses': 'Шифрование, проверка подписей',
            'private_key_uses': 'Расшифрование, подпись документов',
            'key_sizes': 'Минимум 2048 бит (рекомендуется 4096)',
            'use_case': 'Цифровые подписи, обмен ключами, защита интернета (HTTPS)'
        }


if __name__ == '__main__':
    # Примеры использования
    print("=== CAESAR CIPHER ===")
    caesar = CaesarCipher.encrypt("Hello World", shift=3)
    print(f"Зашифровано: {caesar['encrypted']}")
    print(f"Шаги: {len(caesar['steps'])}")
    
    print("\n=== AES CIPHER ===")
    aes = AESCipher.encrypt("Secret Message", "mypassword")
    print(f"Зашифровано: {aes['encrypted'][:50]}...")
    
    print("\n=== RSA CIPHER ===")
    rsa_info = RSACipher.generate_keys()
    print(f"Ключи созданы: {rsa_info['key_size']} бит")
