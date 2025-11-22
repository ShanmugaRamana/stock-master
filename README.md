<div align="center">

<h1>Stock Master - Inventory Management System</h1>
This project is a robust, Inventory management solution designed to streamline business operations. It features a Python Tkinter desktop client for a responsive UI and a FastAPI backend for high-performance data handling and logic.

<strong><h3>BUILT WITH</h3></strong>


<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" /> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" /> <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" /> <img src="https://img.shields.io/badge/Tkinter-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/ReportLab-333333?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" /> <img src="https://img.shields.io/badge/Requests-000000?style=for-the-badge&logo=googlechrome&logoColor=white" />

<table> <tr> <td valign="top" width="40%">

<h2><div align="center"> Key Features</div></h2>

Secure Authentication (Login, Signup, OTP Reset)

Dashboard Analytics (KPIs, Trend Graphs)

Inventory Management (CRUD Products)

Stock Operations (Inbound/Outbound workflows)

Audit Logs (Detailed Movement History)

Visual Reporting (Matplotlib Charts)

PDF Generation (Transaction Receipts)

Role-Based Views (Admin Controls)

</td> <td valign="top" width="60%" style="border-left:1px solid #ccc; padding-left:20px;">

<h2><div align="center"> API Endpoints Overview</div></h2>

POST /signup — User registration & token generation

POST /login — Secure login & session management

POST /forgot-password/* — OTP request & verification

GET/POST /products — Manage product inventory & pricing

GET/POST /stock-moves — Record In/Out transactions

POST /update-password — Security settings update

GET / — Server health check

<h2><div align="center"> Environment Variables (.env)</div></h2>

To run the Server, create a .env file in the root directory with the following credentials:

Code snippet

DATABASE_URL=postgresql://username:password@hostname/databasename
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
Developer
<div style="display: flex; align-items: center; gap: 16px;">

</div>
