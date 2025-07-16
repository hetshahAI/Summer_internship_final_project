# 🚀 Quarky GO v0.0.1 – ESP32 MicroPython Firmware Project

> **“From joystick wake-up to arcade games – all on a 128×32 OLED.”**

A complete interactive firmware written in **MicroPython** for the **Quarky GO (ESP32-WROOM-32E)** board.  
This project was developed during my **Summer Internship @ STEMpedia** as an embedded systems intern.

The system includes joystick-driven navigation, OLED UI rendering, deep-sleep handling, motor/servo control, and two original games (Catch Game & Dino Game) – all running on bare metal ESP32 using Thonny IDE.

---

## 🧠 Summary of Features

| Feature             | Description |
|---------------------|-------------|
| 🧭 **Menu UI**       | Scrollable OLED menu with joystick control & splash screen |
| 🌙 **Sleep Mode**    | Auto deep-sleep after 30s inactivity; joystick wake-up |
| 🦾 **Servo Control** | Control two servos (0–180°) with smooth slider UI |
| ⚙ **Motor Control** | PWM speed fade logic on two DC motors |
| 🎮 **Catch Game**    | Falling-ball game with lives, score, and life powerups |
| 🦖 **Dino Game**     | Jump over obstacles, side-scrolling, score-based Dino game |
| 🛑 **Exit Option**   | Clean shutdown or REPL drop after quitting |

---

## 🛠️ Hardware & Tools

| Category         | Details                              |
|------------------|--------------------------------------|
| **MCU**          | ESP32-WROOM-32E                      |
| **Language**     | MicroPython v1.25.0                  |
| **IDE**          | Thonny                               |
| **Display**      | SSD1306 OLED (128x32) via I2C (GPIO 18/19) |
| **Joystick**     | Center Button → GPIO 13 (IN), ADC → GPIO 36 |
| **Servo Pins**   | GPIO 22 and GPIO 0 (PWM)             |
| **Motor Pins**   | GPIO 27 and GPIO 26 (PWM)            |
| **Libraries**    | `framebuf`, custom `ssd1306.py` driver |

---

## 📁 Folder Structure

Summer_Internship_Final_Project/
├── main.py # Full firmware with all features integrated
├── boot.py # Optional (used for boot tasks if needed)
├── lib/
│ └── ssd1306.py # Custom SSD1306 OLED driver
├── features/ # Separated modular feature files
│ ├── sleep_mode.py
│ ├── servo_control.py
│ ├── motor_control.py
│ ├── catch_game.py
│ ├── dino_game.py
├── demo_video.mp4 # 🎥 Demo (optional)
├── README.md # 📘 You're here


---
##📄 [Internship Project Report (PDF)](docs/project_report.pdf)
---
## 📷 Screenshots (Optional)

> Add visuals here to make it eye-catching:  
> - Menu UI  
> - Servo slider  
> - Catch game in action  
> - Dino game jump moment  
> *(Use `.gif` or small `.png` inside a `screenshots/` folder)*

---

## 🎥 Project Demo

[![Watch the demo](https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg)](https://youtu.be/dQw4w9WgXcQ)



---

## 🧩 Feature Modules (Inside `/features`)

Each feature from `main.py` is available as a standalone Python file for quick testing or reuse:

| File               | Purpose                              |
|--------------------|--------------------------------------|
| `sleep_mode.py`    | Deep sleep + inactivity logic        |
| `servo_control.py` | Servo slider UI + PWM control        |
| `motor_control.py` | Motor PWM fade test menu             |
| `catch_game.py`    | Arcade ball-catching game with lives |
| `dino_game.py`     | Side-scrolling Dino jumping game     |

---

## 🔌 How to Run

1. Flash your **ESP32** board with **MicroPython v1.25.0**
2. Open the project in **Thonny IDE**
3. Copy the following files to your ESP32:
   - `main.py`
   - `lib/ssd1306.py`
4. Hit **Run** ▶ — navigate using joystick and enjoy!

---

## ⚙️ Future Improvements

- 🎵 Add buzzer/sound output on events
- 🌐 Add Bluetooth/Wi-Fi integration
- 💾 Store game high scores to Flash
- 🕹 Add more joystick-driven mini-games
- 🧠 Optimize memory & CPU usage for larger displays

---

## 👨‍💻 Author

**Het Shah**  
🎓 B.Tech ICT @ PDEU | 🔬 AI, ML, IoT & Robotics Enthusiast  
🧠 Embedded Systems Intern @ STEMpedia

- 🔗 [LinkedIn](https://www.linkedin.com/in/hetshah-ai-tech/)
- 💻 [GitHub](https://github.com/hetshahAI)
- 🌐 [Portfolio](https://hetshah1704.wixsite.com/het-portfolio217)

---




