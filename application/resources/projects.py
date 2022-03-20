from http import HTTPStatus
from flask import request
from flask_restx import Namespace, fields, Resource, abort
from flask_jwt_extended import jwt_required

from application.models import Project, Issue
from application.schemas import ProjectSchema

schema = ProjectSchema()
schema_list = ProjectSchema(many=True)
projects_ns = Namespace("projects", description="Projects CRUD operations")

model = projects_ns.model('Project', {
    'name': fields.String('Project name'),
    'description': fields.String('Project description'),
    'created_at': fields.DateTime('User creation date', readonly=True),
    'updated_at': fields.DateTime('User update date', readonly=True),
    'id': fields.Integer(readonly=True),
    'url': fields.Url()
})

model_stats = projects_ns.model('ProjectStats', {
    'name': fields.String('Project name'),
    'description': fields.String('Project description'),
    'created_at': fields.DateTime('User creation date', readonly=True),
    'updated_at': fields.DateTime('User update date', readonly=True),
    'id': fields.Integer(readonly=True),
    'open_issues': fields.Integer(),
    'wip_issues': fields.Integer(),
    'closed_issues': fields.Integer(),
    'url': fields.Url()
})


@projects_ns.route('/stats')
@projects_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
@projects_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
class ProjectsStats(Resource):

    @jwt_required(optional=True)
    @projects_ns.response(int(HTTPStatus.OK), 'Get all Projects with Statistics', fields.List(fields.Nested(model_stats)))
    def get(self):
        projects = Project.filter_by()
        data = []
        for project in projects:
            data.append({
                **ProjectSchema().dump(project),
                'open_issues': Issue.count(project_id=project.id, status='open'),
                'closed_issue': Issue.count(project_id=project.id, status='closed'),
                'wip_issues': Issue.count(project_id=project.id, status='wip'),
            })
        return data


@projects_ns.route('/')
@projects_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
@projects_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
class Projects(Resource):

    @jwt_required(optional=True)
    @projects_ns.response(int(HTTPStatus.OK), 'Get all Projects', fields.List(fields.Nested(model)))
    def get(self):
        projects = Project.filter_by()
        return schema_list.dump(projects)

    @jwt_required(optional=True)
    @projects_ns.expect(model, validate=True)
    @projects_ns.response(int(HTTPStatus.CREATED), 'Created project', model)
    def post(self):

        data = request.get_json()
        project = schema.load(data)

        project.save()
        return schema.dump(project), 201


@projects_ns.route('/<id>')
@projects_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
@projects_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
class ProjectsId(Resource):

    @jwt_required(optional=True)
    @projects_ns.response(int(HTTPStatus.OK), 'Get specific project', [model])
    def get(self, id):
        project = Project.get(id=id)

        if not project:
            abort(404, "Project not found")

        return schema.dump(project)

    @jwt_required(optional=True)
    def delete(self, id):
        project = Project.get(id=id)

        if not project:
            abort(404, "Project not found")

        project.delete()

        return "", 200

    @jwt_required(optional=True)
    @projects_ns.expect(model, validate=True)
    def put(self, id):
        data = request.get_json()
        project = Project.get(id=id)

        if not project:
            abort(404, "Project not found")

        project.update(data)

        return schema.dump(project), 200
