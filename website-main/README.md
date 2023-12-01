Welcome to UWTechPrep, a unique initiative designed to equip software engineering students with the necessary skills and knowledge to excel in technical interviews. The goal is to give students a curated practice plan and the ability to practice interviewing without pressure.

The motivation behind UWTechPrep stems from wanting to assist our fellow students to prepare for technical interviews. With this in mind, we decided to develop a platform where students can schedule one-on-one mentor sessions and mock-interviews with industry professionals in order to practice interviewing and gain confidence for job interviews.

The scheduling tool serves as the main interface for interaction between industry mentors and students, facilitating the scheduling of mock interviews and mentoring sessions. Mentors can indicate time block availabilities, which are broken down into 30 minute appointments for precise scheduling. Students are then able to select and book appointments. When an appointment is booked, an automated email is sent to both the mentor and student of that booking.

The user interface is crafted using HTML, JavaScript, and CSS, ensuring a responsive and intuitive design. The backend is powered by Python Flask. This framework processes mentor availability, student reservations, and triggers the automated email system. MySQL serves as the project's database engine, maintaining user accounts, records of mentor availability, student bookings, and other relevant data.

Getting Started
Welcome to UWTechPrep! This guide will help you get started with running the code locally and setting up any necessary API keys.

Installation process

Clone the Repository: If your code is hosted on Azure DevOps, you can clone the repository using the repository URL provided by Azure DevOps. Use a command similar to the following:
git clone https://dev.azure.com/software-engineering-studio/studio-course/_git/mentor-network
Navigate to the Project Directory: Change your current directory to the project's root folder:
cd your-repo-name
Install Dependencies: Install the required dependencies. You might want to use a virtual environment for this:
pip install -r requirements.txt
Configuration: Configure any settings or variables that are necessary for your project. This might include database connection strings, API endpoints, or other environment-specific settings. You may find a configuration file (e.g., config.py) where you can specify these values.
Software dependencies

Ensure you have the following software dependencies installed:

Python  (Version X.X or later)
Git 
Latest releases

To check for the latest releases and updates to this codebase, refer to the release information provided on Azure DevOps or any other release management system your project uses.

API references

SendGrid API:

Go to API Provider's Website .
Sign up for an account if required.
Generate an API key in your account settings.
Store the API key securely. Do not hardcode it in your codebase. Instead, you can store it as an environment variable or use a configuration file.
Build and Test
Getting the Source Code First, clone the repository:

git clone [URL of your repository]
cd [Your project directory name]
Setting up the Environment

Ensure you set up the necessary environment variables or configuration files. 
Refer to the sample.env for the required variables and rename it to .env after adding appropriate values.
Starting the Application

python main.py
Contribute
While the current version of the scheduling tool meets the foundational needs, there is always room for improvement.

If you want to learn more about creating good readme files then refer the following guidelines . You can also seek inspiration from the below readme files:

ASP.NET Core 
Visual Studio Code 
Chakra Core 
If you want to learn more about creating good readme files then refer the following guidelines . You can also seek inspiration from the below readme files:

ASP.NET Core 
Visual Studio Code 
Chakra Core 
