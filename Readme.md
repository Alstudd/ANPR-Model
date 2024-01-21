# Project: Hawkeye - Automatic Number Plate Detection (ANPR)

## Introduction

The surge in vehicular traffic in urban areas has necessitated the adoption of advanced technologies to enhance traffic management, law enforcement, and public safety. Traditional methods of vehicle identification are proving inadequate, prompting the need for an automated solution. This project proposes the implementation of Automatic Number Plate Detection (ANPR) technology to overcome the challenges associated with manual identification.

## Motivation

The motivation to solve the ANPR problem stems from the potential to significantly enhance public safety, traffic efficiency, crime prevention, and economic benefits. With over 1.35 million road traffic fatalities globally each year, timely identification of vehicles involved in accidents can contribute to reducing this alarming number. The economic benefits, including cost savings and the projected growth of the global ANPR market, further emphasize the importance of solving this problem.

## Technology Stack

The project utilizes a comprehensive technology stack comprising Visual Studio Code, SQLite for database management, Python as the primary programming language, and Flask as the web framework. The incorporation of HTML, CSS, and JavaScript ensures a seamless user interface. Key libraries such as OpenCV, EasyOCR, and NumPy play a pivotal role in implementing the ANPR technology.

## Implementation

The user-centric approach begins with Flask login and authentication, ensuring a secure and personalized experience. Once logged in, users can access the ANPR model, which employs the `haarcascade_russian_plate_number.xml` for plate detection. Images and videos are processed using OpenCV, where the number plates are highlighted, and results are displayed using `cv2.rectangle()` and `cv2.putText()`.

The system supports live camera functionality, leveraging `cv2.VideoCapture(0)` to integrate with CCTV systems. This allows users to detect number plates in real-time, enhancing surveillance capabilities.

## Tagline

"License to Locate: Hawkeye, Your Ultimate Number Plate Mate!"

## Problem It Solves

- Efficient Traffic Management
- Enhanced Security
- Law Enforcement Support
- Parking Management Efficiency
- Rapid Emergency Response
- Accurate Traffic Violation Detection
- Data-Driven Decision Making
- User-Centric Live Camera Integration
- Economic Benefits
- Global ANPR Market Growth
