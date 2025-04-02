Flask User Registration & Login System (Ubuntu)
This guide will walk you through creating a basic Flask application with user registration and login functionality without using a database. We'll use a simple Python dictionary to store user data in memory (note: this means data will be lost when the server restarts).

Step 1: Update System Packages
> sudo apt update
> sudo apt upgrade -y

Step 2: Install Required Software
> sudo apt install python3 python3-pip python3-venv -y

Step 3: Download Repo
> git clone https://github.com/ARusama515/flaskregistrationapp.git

Step 4: Create Virtual Environment
> python3 -m venv venv && source venv/bin/activate

Step 5: Install Flask
> pip install flask

Step 6: Run the Application
> python3 app.py

Step 7: View the Application on browser
> http://your_ubbuntu_machine's_IP:5000

<img width="945" alt="Screenshot 2025-04-02 010634" src="https://github.com/user-attachments/assets/52e40291-c0f4-4cdf-858a-8b01f758b05c" />
<img width="941" alt="Screenshot 2025-04-02 010838" src="https://github.com/user-attachments/assets/0c47e49c-be3f-439a-8549-8071f4f253db" />
