import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

# first argument is blueprints name
# second argument is it's import_name
issue = Blueprint('issues', 'issue')


# Index Route (get)
@issue.route('/', methods=["GET"])
def get_all_issues():
    ## find the issues and change each one to a dictionary into a new array
    try:
        issues = [model_to_dict(issue) for issue in models.Issue.select()]
        print(issues)
        return jsonify(data=issues, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


# Create/New Route (post)
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


# Show Route (get)
@issue.route('/<id>', methods=["GET"])
def get_one_issue(id):
    print(id, 'reserved word?')
    issue = models.Issue.get_by_id(id)
    print(issue.__dict__)
    return jsonify(data=model_to_dict(issue), status={"code": 200, "message": "Success"})


# Update/Edit Route (put)
@issue.route('/<id>', methods=["PUT"])
def update_issue(id):
    payload = request.get_json()
    # print(payload)

    query = models.Issue.update(**payload).where(models.Issue.id == id)
    query.execute()

    # print(type(query))
    # find the issue again
    issue = models.Issue.get_by_id(id)

    issue_dict = model_to_dict(issue)
    # updated_issue = model_to_dict(query)
    # print(updated_issue, type(update_issue))
    return jsonify(data=issue_dict, status={"code": 200, "message": "resource updated successfully"})


# Delete Route (delete)
@issue.route('/<id>', methods=["DELETE"])
def delete_issue(id):
    query = models.Issue.delete().where(models.Issue.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status="code": 200, "message": "resource deleted successfully" )

