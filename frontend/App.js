import React, { useRef, useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from "react-native";
import { CameraView, useCameraPermissions } from "expo-camera";
import * as Speech from "expo-speech";

export default function App() {
  const cameraRef = useRef(null);
  const [permission, requestPermission] = useCameraPermissions();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("No object scanned yet");
  const [confidence, setConfidence] = useState(null);

  const BACKEND_URL = "http://YOUR_LAPTOP_IP:5000/detect";

  if (!permission) {
    return (
      <View style={styles.center}>
        <Text>Loading camera permission...</Text>
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={styles.center}>
        <Text style={styles.permissionText}>
          Camera permission is needed to scan objects.
        </Text>

        <TouchableOpacity style={styles.button} onPress={requestPermission}>
          <Text style={styles.buttonText}>Allow Camera</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const scanObject = async () => {
    try {
      if (!cameraRef.current) {
        Alert.alert("Camera not ready");
        return;
      }

      setLoading(true);
      setResult("Scanning...");
      setConfidence(null);

      const photo = await cameraRef.current.takePictureAsync({
        base64: true,
        quality: 0.5,
      });

      const response = await fetch(BACKEND_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          image: photo.base64,
        }),
      });

      const data = await response.json();

      if (data.error) {
        setResult(`Error: ${data.error}`);
        Speech.speak("There was an error detecting the object.");
        return;
      }

      if (!data.detected) {
        setResult("No object detected");
        Speech.speak(data.speech || "No object detected. Please try again.");
        return;
      }

      const best = data.best_detection;
      const confidencePercent = Math.round(best.confidence * 100);
      const outputText = `${best.label}\nCategory: ${best.category}`;

      setResult(outputText);
      setConfidence(confidencePercent);

      Speech.speak(data.speech, {
        language: "en",
        pitch: 1.0,
        rate: 0.9,
      });
    } catch (error) {
      console.log(error);
      setResult("Could not connect to backend.");
      setConfidence(null);
      Speech.speak("Could not connect to the detection system.");
    } finally {
      setLoading(false);
    }
  };

  const repeatSpeech = () => {
    const text = result.replace("\n", ". ");
    Speech.speak(text, {
      language: "en",
      pitch: 1.0,
      rate: 0.9,
    });
  };

  return (
    <View style={styles.container}>
      <CameraView ref={cameraRef} style={styles.camera} facing="back" />

      <View style={styles.bottomPanel}>
        <Text style={styles.title}>Assistive Visual Recognition</Text>
        <Text style={styles.resultText}>{result}</Text>

        {confidence !== null && (
          <Text style={styles.confidenceText}>Confidence: {confidence}%</Text>
        )}

        {loading ? (
          <ActivityIndicator size="large" />
        ) : (
          <TouchableOpacity style={styles.button} onPress={scanObject}>
            <Text style={styles.buttonText}>Scan Object</Text>
          </TouchableOpacity>
        )}

        <TouchableOpacity style={styles.secondaryButton} onPress={repeatSpeech}>
          <Text style={styles.secondaryButtonText}>Repeat Audio</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  camera: {
    flex: 1,
  },
  bottomPanel: {
    padding: 20,
    backgroundColor: "#ffffff",
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 10,
  },
  resultText: {
    fontSize: 18,
    marginBottom: 6,
  },
  confidenceText: {
    fontSize: 15,
    marginBottom: 15,
  },
  button: {
    backgroundColor: "#003b5c",
    padding: 15,
    borderRadius: 10,
    alignItems: "center",
    marginBottom: 10,
  },
  buttonText: {
    color: "#ffffff",
    fontSize: 16,
    fontWeight: "bold",
  },
  secondaryButton: {
    borderWidth: 1,
    borderColor: "#003b5c",
    padding: 15,
    borderRadius: 10,
    alignItems: "center",
  },
  secondaryButtonText: {
    color: "#003b5c",
    fontSize: 16,
    fontWeight: "bold",
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 25,
  },
  permissionText: {
    fontSize: 16,
    textAlign: "center",
    marginBottom: 20,
  },
});
