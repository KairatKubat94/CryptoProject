// ==================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ====================
const API_BASE = 'http://127.0.0.1:5000/api';

// ==================== ПЕРЕКЛЮЧЕНИЕ АЛГОРИТМОВ ====================
document.querySelectorAll('.algo-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const algo = this.dataset.algo;
        
        // Обновляем активную кнопку
        document.querySelectorAll('.algo-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        // Скрываем все секции
        document.querySelectorAll('.algo-section').forEach(section => {
            section.classList.remove('active');
        });
        
        // Показываем нужную секцию
        document.getElementById(`${algo}-section`).classList.add('active');
    });
});

// ==================== CAESAR CIPHER ====================
async function encryptCaesar() {
    const text = document.getElementById('caesar-input').value.trim();
    const shift = parseInt(document.getElementById('caesar-shift').value) || 3;
    
    if (!text) {
        showError('caesar-steps', 'Пожалуйста, введите текст');
        return;
    }
    
    if (shift < 1 || shift > 25) {
        showError('caesar-steps', 'Смещение должно быть от 1 до 25');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/caesar/encrypt`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, shift })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('caesar-steps', data.error);
            return;
        }
        
        // Показываем результат
        document.getElementById('caesar-result').textContent = data.encrypted;
        
        // Показываем шаги
        displayCaesarSteps(data.steps);
    } catch (error) {
        showError('caesar-steps', 'Ошибка соединения: ' + error.message);
    }
}

async function decryptCaesar() {
    const text = document.getElementById('caesar-input').value.trim();
    const shift = parseInt(document.getElementById('caesar-shift').value) || 3;
    
    if (!text) {
        showError('caesar-steps', 'Пожалуйста, введите текст');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/caesar/decrypt`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, shift })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('caesar-steps', data.error);
            return;
        }
        
        document.getElementById('caesar-result').textContent = data.encrypted;
        displayCaesarSteps(data.steps);
    } catch (error) {
        showError('caesar-steps', 'Ошибка соединения: ' + error.message);
    }
}

function displayCaesarSteps(steps) {
    const container = document.getElementById('caesar-steps');
    container.innerHTML = '';
    
    steps.forEach((step, index) => {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'step';
        
        if (step.encrypted === undefined) {
            stepDiv.innerHTML = `
                <span class="step-number">${step.step}</span>
                <strong>${step.original}</strong> → <strong>${step.encrypted}</strong>
                <div class="step-content">${step.explanation}</div>
            `;
        } else {
            stepDiv.innerHTML = `
                <span class="step-number">${step.step}</span>
                <strong>${step.original}</strong> → <strong>${step.encrypted}</strong>
                <div class="step-content">${step.explanation}</div>
            `;
        }
        
        container.appendChild(stepDiv);
        
        // Анимация появления
        setTimeout(() => {
            stepDiv.style.opacity = '0';
            stepDiv.style.transform = 'translateX(-20px)';
            stepDiv.offsetHeight; // Перефорс
            stepDiv.style.transition = 'all 0.3s ease-out';
            stepDiv.style.opacity = '1';
            stepDiv.style.transform = 'translateX(0)';
        }, index * 50);
    });
}

// ==================== AES CIPHER ====================
async function encryptAES() {
    const text = document.getElementById('aes-input').value.trim();
    const password = document.getElementById('aes-password').value.trim();
    
    if (!text) {
        showError('aes-steps', 'Пожалуйста, введите текст');
        return;
    }
    
    if (!password) {
        showError('aes-steps', 'Пожалуйста, введите пароль');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/aes/encrypt`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, password })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('aes-steps', data.error);
            return;
        }
        
        document.getElementById('aes-result').textContent = data.encrypted;
        document.getElementById('aes-encrypted-input').value = data.encrypted;
        displayAESSteps(data.steps);
        
        // Показываем панель расшифрования
        document.getElementById('aes-decrypt-panel').style.display = 'block';
    } catch (error) {
        showError('aes-steps', 'Ошибка соединения: ' + error.message);
    }
}

function showDecryptAES() {
    document.getElementById('aes-decrypt-panel').style.display = 
        document.getElementById('aes-decrypt-panel').style.display === 'none' ? 'block' : 'none';
}

async function decryptAES() {
    const encrypted = document.getElementById('aes-encrypted-input').value.trim();
    const password = document.getElementById('aes-decrypt-password').value.trim();
    
    if (!encrypted) {
        showError('aes-steps', 'Пожалуйста, введите зашифрованный текст');
        return;
    }
    
    if (!password) {
        showError('aes-steps', 'Пожалуйста, введите пароль');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/aes/decrypt`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ encrypted, password })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('aes-steps', data.error);
            return;
        }
        
        document.getElementById('aes-result').textContent = data.decrypted;
        displayAESSteps(data.steps);
    } catch (error) {
        showError('aes-steps', 'Ошибка соединения: ' + error.message);
    }
}

function displayAESSteps(steps) {
    const container = document.getElementById('aes-steps');
    container.innerHTML = '';
    
    steps.forEach((step, index) => {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'step';
        
        stepDiv.innerHTML = `
            <span class="step-number">${step.step}</span>
            <strong>${step.phase}</strong>
            <div class="step-content">${step.explanation}</div>
        `;
        
        container.appendChild(stepDiv);
        
        setTimeout(() => {
            stepDiv.style.opacity = '0';
            stepDiv.style.transform = 'translateX(-20px)';
            stepDiv.offsetHeight;
            stepDiv.style.transition = 'all 0.3s ease-out';
            stepDiv.style.opacity = '1';
            stepDiv.style.transform = 'translateX(0)';
        }, index * 100);
    });
}

// ==================== RSA CIPHER ====================
async function generateRSAKeys() {
    const keySize = document.getElementById('rsa-key-size').value;
    
    const container = document.getElementById('rsa-steps');
    container.innerHTML = '<div class="step loading">⏳ Генерирование ключей (может занять время)...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/rsa/generate-keys`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key_size: parseInt(keySize) })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('rsa-steps', data.error);
            return;
        }
        
        displayRSASteps(data.steps);
        document.getElementById('rsa-encrypt-panel').style.display = 'block';
        
        // Очищаем результат
        document.getElementById('rsa-result').textContent = 'Готово к шифрованию';
    } catch (error) {
        showError('rsa-steps', 'Ошибка соединения: ' + error.message);
    }
}

async function encryptRSA() {
    const text = document.getElementById('rsa-input').value.trim();
    
    if (!text) {
        showError('rsa-steps', 'Пожалуйста, введите текст для шифрования');
        return;
    }
    
    const container = document.getElementById('rsa-steps');
    container.innerHTML = '<div class="step loading">⏳ Шифрование (может занять время)...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/rsa/encrypt`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError('rsa-steps', data.error);
            return;
        }
        
        document.getElementById('rsa-result').textContent = data.encrypted;
        displayRSASteps(data.steps);
    } catch (error) {
        showError('rsa-steps', 'Ошибка соединения: ' + error.message);
    }
}

function displayRSASteps(steps) {
    const container = document.getElementById('rsa-steps');
    container.innerHTML = '';
    
    steps.forEach((step, index) => {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'step';
        
        stepDiv.innerHTML = `
            <span class="step-number">${step.step}</span>
            <strong>${step.phase}</strong>
            <div class="step-content">${step.explanation}</div>
        `;
        
        container.appendChild(stepDiv);
        
        setTimeout(() => {
            stepDiv.style.opacity = '0';
            stepDiv.style.transform = 'translateX(-20px)';
            stepDiv.offsetHeight;
            stepDiv.style.transition = 'all 0.3s ease-out';
            stepDiv.style.opacity = '1';
            stepDiv.style.transform = 'translateX(0)';
        }, index * 150);
    });
}

// ==================== УТИЛИТЫ ====================
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="error-message">❌ ${message}</div>`;
}

function showSuccess(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="success-message">✓ ${message}</div>`;
}

function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showSuccess(elementId, '✓ Скопировано в буфер обмена!');
        setTimeout(() => {
            element.textContent = text;
        }, 2000);
    }).catch(err => {
        showError(elementId, 'Ошибка при копировании');
    });
}

// ==================== ИНИЦИАЛИЗАЦИЯ ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log('Визуализатор алгоритмов шифрования загружен');
    console.log('API Base:', API_BASE);
    
    // Проверяем подключение к серверу
    checkServerConnection();
});

async function checkServerConnection() {
    try {
        const response = await fetch(`${API_BASE}/algorithms`);
        if (response.ok) {
            console.log('✓ Соединение с сервером установлено');
        }
    } catch (error) {
        console.warn('⚠️ Сервер недоступен. Убедитесь, что Flask приложение запущено на http://127.0.0.1:5000');
    }
}
