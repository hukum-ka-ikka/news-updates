## Features
------------
- **React + Vite Frontend**: Handles all frontend operations for news updates.
- **Component based Architecture**: Component based frontend architecture for readability and reusability.
- **Responsive Frontend**: Adjusts UI according to screen size.
- **Django Backend**: Handles all backend operations for news updates.
- **Server Side Events**: Updates clients feed as and when it refreshes feed on server.
- **CORS Support**: Allows cross-origin requests from the frontend application.
- **API Only**: Purely a backend application that serves data to a frontend, without any direct views or templates.

## Tech Stack
------------
- **React**: (version 18.3.1)
- **Vite**: (version 6.0.1)
- **Django** (version 4.2.16)
- **Daphne for ASGI Support**: For asynchronous request handling.
- **SQLite Database**: Lightweight and simple database for storage.

# Deployment
This project is deployed on Vercel(frontend) and Render(backend)

## Steps to Deploy on Vercel 
-----------
- **1.** Push your project to GitHub.
- **2.** Signup or Login to Vercel (preferably using github).
- **3.** Go to Home and click Add New.
- **4.** Select your project from the repository and follow the steps (pretty straight forward).
- **5.** Add env variables accordingly.

## Steps to Deploy on Render
-----------
- **1.** Go to Render and create a new web service.
- **2.** Select your GitHub repository and configure it to use Python.
- **3.** Set up ALLOWED_HOSTS = ["your-host-name"] (without https and www) in setting.py
- **4.** Render will automatically install the dependencies and start the server using daphne automation_backend.asgi:application --bind 0.0.0.0 --port $PORT.