# IoT-Based Driver Behaviour Analysis System

A Raspberry Pi-based system that monitors selected driving behaviours and generates a **Driver Behaviour Score** based on unsafe distance, braking events and horn usage. The system provides visual and audio feedback to encourage safer driving habits.

## Overview

Road safety is strongly influenced by driver behaviour. Unsafe following distance, unnecessary braking and excessive honking can indicate risky or aggressive driving patterns.

The proposed system works as a **driver behaviour monitoring and feedback system**. It observes selected driving-related events, evaluates them using a weighted scoring model and generates a measurable Driver Behaviour Score.

The project is implemented as a prototype using a **Raspberry Pi 4**, with a **Wokwi Raspberry Pi Pico simulation** for testing the system logic.

## Problem Statement

Traditional road safety approaches often focus on identifying and penalizing violations after they occur. They provide limited continuous feedback about a driver's overall behaviour.

Drivers may repeatedly develop unsafe habits such as maintaining an unsafe distance, unnecessary braking or excessive honking without having an objective way to recognize these patterns.

Therefore, there is a need for a **cost-effective system that can monitor selected driving behaviours, quantify unsafe events and provide understandable feedback to encourage safer driving practices**.

## Proposed Solution

The system addresses this problem by converting driving-related events into a **Driver Behaviour Score**.
The overall process is:

Driving Behaviour
↓
Sensor / Input Monitoring
↓
Unsafe Event Detection
↓
Weighted Scoring
↓
Driver Behaviour Score
↓
LED / Buzzer Feedback
↓
Awareness and Behaviour Improvement

## Objectives

- Monitor selected driving-related events using IoT components.
- Detect and count selected driving events for behaviour analysis.
- Generate a measurable Driver Behaviour Score.
- Provide feedback through LEDs and a buzzer.
- Demonstrate a low-cost approach to driver behaviour monitoring.
- Provide a foundation for future automotive and data-driven applications.

## Components

### Hardware

- Raspberry Pi 4
- HC-SR04 Ultrasonic Sensor
- 2 Push Buttons
- Green, Yellow and Red LEDs
- Active Buzzer
- Resistors, Breadboard and Jumper Wires

### Software

- Python 3
- Raspberry Pi OS
- RPi.GPIO
- Wokwi
- MicroPython

## Working

The system evaluates driving behaviour over a **30-second interval**.

### Distance Monitoring

The HC-SR04 measures the distance from an object in front of the vehicle. A distance below **15 cm** is treated as an unsafe-distance event. A continuous unsafe-distance condition is counted only once until the distance returns to the safe range.

### Braking Detection

A push button represents the brake. Each separate press is counted as one braking event. Holding the button does not continuously increase the count(as the driver maybe waiting at a signal).

In a planned implementation, a **rheostat (potentiometer)** can be used to simulate braking intensity or braking speed. This would allow the system to distinguish between gradual and sudden braking.

The braking event can also be evaluated according to the surrounding situation:

- **Obstacle detected + sudden braking:** considered an appropriate alert response.
- **No obstacle + sudden braking:** considered potentially unsafe or aggressive behaviour.

This would make the braking analysis more **context-aware**, rather than treating every braking event as unsafe.

### Horn Detection

A push button represents the vehicle horn. Horn usage is counted using a **0.5-second interval**.

## Driver Behaviour Scoring

Different weights are assigned to the monitored events:

| Event           | Weight |
| --------------- | ------ |
| Unsafe Distance | 0.45   |
| Braking         | 0.40   |
| Horn Usage      | 0.15   |

The weighted penalty is calculated as:
Penalty = (0.45 × Distance Count) + (0.40 × Brake Count) + (0.15 × Horn Count)

The final score is:
Score = 100 − (Penalty × 5)

If the calculated score becomes negative, it is set to **0**.

## Feedback System

| Score        | Feedback                     |
| ------------ | ---------------------------- |
| **85–100**   | 🟢 Green LED — Safe          |
| **70–84**    | 🟡 Yellow LED — Moderate     |
| **Below 70** | 🔴 Red LED + Buzzer — Unsafe |

The calculated event counts and score are also displayed in the terminal.

## 🌍 Impact and Applications

The purpose of the system is not simply to generate a score, but to **make driving behaviour measurable and provide feedback that can encourage improvement over time**.

### Driving Schools

Driving instructors can use behaviour scores to identify habits such as unsafe distance maintenance, frequent braking or excessive horn usage. This provides an objective supplement to instructor observation and can help learners understand areas that require improvement.

### Individual Drivers

Drivers can monitor their behaviour over multiple trips and use the score as a simple indicator of whether their driving habits are improving.

### Fleet Management

Companies can monitor driver behaviour across multiple vehicles and identify drivers who may benefit from additional safety training.

### Road Safety Programs

Aggregated and anonymized behavioural data could potentially help identify recurring unsafe driving patterns and support road-safety planning.

Overall, the system aims to shift driver monitoring from simply **detecting violations** toward **continuous awareness, feedback and behavioural improvement**.

## 🧪 Wokwi Simulation

The system is simulated using a **Raspberry Pi Pico and MicroPython** in Wokwi. The simulation is used to test distance detection, input handling, event counting and the scoring logic.

## ⚠️ Limitations

The current prototype uses push buttons to represent braking and horn actions, while the distance threshold is fixed at 15 cm. It does not currently measure braking intensity, vehicle speed, road conditions or identify the type of object detected by the ultrasonic sensor.

## 🚀 Future Scope

The prototype can be extended using **Radar, LiDAR and IMUs**, along with vehicle data integration, mobile dashboards, cloud connectivity and machine-learning techniques for more advanced driver behaviour analysis.

Future versions could also support **driving-school training systems, fleet analytics and gamified driver improvement programs**.

## 👨‍💻 Project

**IoT-Based Driver Behaviour Analysis System**

An academic IoT project demonstrating how driving-related events can be monitored, scored and used to provide feedback for safer driving behaviour.
