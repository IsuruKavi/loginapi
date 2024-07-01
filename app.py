from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flasgger import Swagger, swag_from

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Setup the Flask-Swagger extension
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "My API",
        "description": "API for demonstrating JWT with Swagger",
        "version": "1.0.0"
    },
     "produces": [
        "application/json",
        "text/html"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
})

@app.route("/login", methods=["POST"])
@swag_from({
    'responses': {
        200: {
            'description': 'Login successful',
            'examples': {
                'application/json': {
                    'access_token': 'string'
                }
            }
        },
        401: {
            'description': 'Bad username or password',
            'examples': {
                'application/json': {
                    'msg': 'Bad username or password'
                }
            }
        }
    }
})
def login():
    """
    User login endpoint.
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Bad username or password
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route("/homepage", methods=["GET"])
@jwt_required()
@swag_from({
    'responses': {
        200: {
            'description': 'Access granted',
            'examples': {
                'application/json': {
                    'logged_in_as': 'string'
                },
                'text/html': {
                    'example': '<html><body><h1>Welcome, test</h1></body></html>'
                }
            }
        },
        401: {
            'description': 'Missing or invalid JWT',
            'examples': {
                'application/json': {
                    'msg': 'Missing or invalid JWT'
                }
            }
        }
    },
    'security': [
        {
            'Bearer': []
        }
    ]
})
def homepage():
    """
    Protected homepage endpoint.
    ---
    tags:
      - Homepage
    responses:
      200:
        description: Access granted
      401:
        description: Missing or invalid JWT
    """
    current_user = get_jwt_identity()

    if request.headers.get('Accept', type=str) == "application/json":
        return jsonify(logged_in_as=current_user), 200
    else:
        return render_template('homepage.html', current_user=current_user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
