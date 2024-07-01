# Clone the repository
git clone <repository_url>
cd project-directory

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run applicaiton

python app.py

# Test api endpoint
swagger-http://127.0.0.1:5000/apidocs

use this for check login endpoint,{
  "password": "test",
  "username": "test"
}