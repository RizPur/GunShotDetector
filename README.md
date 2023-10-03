## 🏆 JAIA Hackathon 2023 Winner

### 📣 Synopsis - Gunshot Detection and Classification System

This project won the first-ever JAIA Hackathon. It's designed to detect and classify gunshots in real-time. When a gunshot is detected, the audio is parsed, processed, and sent through two machine learning models. The first model identifies whether the sound is a gunshot or not. If it is, the second model classifies the type of gun the shot originated from. All the data, along with geolocation and timestamp, is then displayed on a real-time map interface built with React.
🛠️ Tech Stack

- Machine Learning Models: Python, Torch
- Audio Preprocessing: Python scripts to convert .wav to MFCCs
- Backend: Django
- Frontend: React
- Communication: Webhooks, Django channel server

### 🧑‍💻 Team Roles

#### 🤖 Model Training and Prediction (Team)

- Model Selection: CNN for audio classification.

1. **Train Model: Used preprocessed audio data to train the model.**
2. **Prediction: Made predictions and sent data to David's script.**

#### 🎧 Douglas: Data Collection and Preprocessing

- Collected audio data of common gunshots in Kingston.
- Preprocessed the raw audio into MFCCs.

```python
mfccs = librosa.feature.mfcc(audio_data, sr)
```
Performed data augmentation for model robustness.
```python
predictions = model.predict(preprocessed_audio)
```

#### 🚨 David: Alerting and Backend-Frontend Integration

- Created a system to alert authorities in real-time.

- Ensured seamless communication between the Django backend, ml models, and React frontend.

```python
def initiate_client(data):
    ws = create_connection("ws://localhost:8000/ws/chat/gunsession/")
    ws.send(json.dumps({"message": data}))
    ws.close()
```

#### 🗺️ Joel: User Interface

- Built a real-time dashboard using React and Leaflet.

```javascript
ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const message = data.message;
      console.log('Received:', message);
    
      if (message && message.geo) {
        const [x, y] = message.geo;
        setGunShot(message)
        // console.log(gunShot)
        flyMap(x, y, 11);
      }
    
      setGunShots(prevGunshots => [...prevGunshots, message]);
      console.log(gunShot,gunShots)
    };
```

---

## 🚀 Steps to Run the Project

### 🐍 Django Backend Setup

1. **Create a Python Virtual Environment**  
   - Use Python 3.10.
   
2. **Activate the Virtual Environment**  
   - Activate the virtual environment that you just created.

3. **Install Required Packages**  
   - Run the command `pip install -r requirements.txt` in the root of the project.

4. **Make Migrations**  
   - Navigate to the `gun_shot_detector` folder.
   - Run the command `python manage.py makemigrations`. (This file should already exist in most cases).

5. **Apply Migrations**  
   - Run the command `python manage.py migrate`.

### 🛢️ Redis Setup

#### General Steps
- Download the Redis server for your respective environment.

#### macOS
- Run the command `brew install redis`.

#### Windows
- Follow the instructions outlined in this [article](https://redis.io/docs/getting-started/installation/install-redis-on-windows/) or install using Docker.

#### Ubuntu
```bash
sudo apt install lsb-release curl gpg
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis
```

### 🏃‍♂️ Running the Applications

1. **Start Redis Server**  
   - Run the command `redis-server --port 6379`.

2. **Start Django Server**  
   - Navigate to the `gun_shot_detector` folder.
   - Make sure the virtual environment is activated.
   - Run the command `python manage.py runserver`.

### 🌐 Frontend Setup

1. **Navigate to Frontend Directory**  
   - Go to the `/frontend` folder.

2. **Install Node Modules**  
   - Run the command `npm install` to install modules from `package.json`.

3. **Start the Frontend**  
   - Run the command `npm start`.
   - Make sure the webhook address matches what you have in the Django channel configs.
   ```javascript
   // Example from line 89
   const ws = new WebSocket('ws://***.***.**.**:8000/ws/chat/gunsession/');
   ```

### 🎧 Machine Learning Models
- Run main.py in each ml folder to train model.
---
