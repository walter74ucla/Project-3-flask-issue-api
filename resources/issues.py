import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

# first argument is blueprints name
# second argument is it's import_name
issue = Blueprint('issues', 'issue')


# Get (index route)
@issue.route('/', methods=["GET"])
def get_all_issues():
    ## find the issues and change each one to a dictionary into a new array
    try:
        issues = [model_to_dict(issue) for issue in models.Issue.select()]
        print(issues)
        return jsonify(data=issues, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


# Post Route (create)
@issue.route('/', methods=["POST"])
def create_issues():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    issue = models.Issue.create(**payload)
    ## see the object
    print(issue.__dict__)
    ## Look at all the methods
    print(dir(issue))
    # Change the model to a dict
    print(model_to_dict(issue), 'model to dict')
    issue_dict = model_to_dict(issue)
    return jsonify(data=issue_dict, status={"code": 201, "message": "Success"})
