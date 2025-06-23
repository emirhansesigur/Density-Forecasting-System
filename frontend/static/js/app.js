// Backend API base URL
const API_BASE_URL = 'http://127.0.0.1:8000';

// DOM yüklendiğinde çalışacak
document.addEventListener('DOMContentLoaded', function() {
    // Veri çekme butonu
    const fetchDataBtn = document.getElementById('fetchDataBtn');
    const dataResult = document.getElementById('dataResult');
    
    // Form elementi
    const dataForm = document.getElementById('dataForm');
    const submitResult = document.getElementById('submitResult');
    
    // Backend'den veri çekme
    fetchDataBtn.addEventListener('click', async function() {
        try {
            showLoading(dataResult);
            
            // İstek atılan endpoint değiştirildi
            const response = await fetch(`${API_BASE_URL}/api/users`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            showSuccess(dataResult, `Başarılı! Data: ${JSON.stringify(data)}`);
            
        } catch (error) {
            showError(dataResult, `Hata: ${error.message}`);
        }
    });
    
    // Form gönderme
    dataForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const name = document.getElementById('nameInput').value;
        const email = document.getElementById('emailInput').value;
        
        try {
            showLoading(submitResult);
            
            const response = await fetch(`${API_BASE_URL}/api/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    email: email
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            showSuccess(submitResult, `Başarılı! Status: ${result.status}`);
            
            // Formu temizle
            dataForm.reset();
            
        } catch (error) {
            showError(submitResult, `Hata: ${error.message}`);
        }
    });
});

// Yardımcı fonksiyonlar
function showLoading(element) {
    element.innerHTML = 'Yükleniyor...';
    element.className = '';
}

function showSuccess(element, message) {
    element.innerHTML = message;
    element.className = 'success';
}

function showError(element, message) {
    element.innerHTML = message;
    element.className = 'error';
}

// Gelişmiş API fonksiyonları
const API = {
    // GET isteği
    get: async function(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    },
    
    // POST isteği
    post: async function(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    },
    
    // PUT isteği
    put: async function(endpoint, data) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    },
    
    // DELETE isteği
    delete: async function(endpoint) {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }
};