# Assistive Visual Recognition for the Visually Impaired

University implementation project by Omar Mohammad Alfalasi (10201351).

## Week 2 goal
Build the first working prototype:

Camera -> React Native/Expo app -> Flask backend -> YOLOv8n object detection -> object/category result -> text-to-speech.

## Project structure

```text
Final-project/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   └── App.js
└── README.md
```

## Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The backend runs on `http://0.0.0.0:5000`.

## Frontend setup

Create an Expo project locally, then replace its `App.js` with the file in this repository:

```bash
npx create-expo-app frontend-app
cd frontend-app
npx expo install expo-camera expo-speech
```

Copy `frontend/App.js` into the Expo project and replace `YOUR_LAPTOP_IP` with your computer IPv4 address, for example:

```js
const BACKEND_URL = "http://192.168.1.25:5000/detect";
```

Run:

```bash
npx expo start
```

The phone and laptop should be on the same Wi-Fi network.

## Week 2 scope
This version is intentionally basic. Testing, confidence analysis, custom categories, and custom training are planned for later weeks.
