# SuperRay: Web App for X-ray image Up-Scaling and Diagnostics

SuperRay is a web application designed for up-scaling and diagnostics. The application is divided into two main components: the backend built with Django (Python) and the front-end built with Next.js and Tailwind CSS (JavaScript).
## Installation


### Requirements
python 3.10

node v21.6.1

Clone of the repository:


```bash
git clone https://github.com/Sabih-Rahman5/2024-ai-challenge-superray.git
```
### Backend (Django)




1. navigate to the SuperRay-Backend folder
```
cd SuperRay-Backend
```



2. Create a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
```

3. Activate Environment:

```bash
.venv/Scripts/Activate
```
4. Install the required packages by running pip install -r requirements.txt:
```bash
pip install -r requirements.txt
```

5. Run Server:

```bash
python manage.py runserver
```

The backend development server should now be running at http://localhost:8000 with the following routes:

•	/admin

•	/api for super resolution

•	/api for login

•	/api for token refresh

•	/api for register

•	/api for logout

•	/api for to view profile

•	/api for update profile



### Front-end(Next-js)

1. Navigate to the SuperRay-NextJs-Tailwind directory:


```bash
cd SuperRay-NextJs-Tailwind
```



2. Install dependencies:


```bash
npm install
```
3. Start the development server:
```
npm run dev
```


The frontend development server should now be running at http://localhost:3000.


## License
This project is licensed under the MIT License.

















