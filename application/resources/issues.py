from http import HTTPStatus
from flask import request
from flask_restx import Namespace, fields, Resource, abort
from flask_jwt_extended import jwt_required

from application.models import Issue, Comment
from application.schemas import IssueSchema, CommentSchema


issues_ns = Namespace('issues', description='Issues & Comments CRUD operations')

issue = issues_ns.model('Issue', {
    'name': fields.String('Issue name'),
    'description': fields.String('Issue description'),
    "project_id": fields.Integer('Project id in which issue happened'),
    'status': fields.String('Issue status'),
    'created_at': fields.DateTime('Issue creation date', readonly=True),
    'updated_at': fields.DateTime('Issue update Date', readonly=True),
    'id': fields.Integer(readonly=True)
})
issue_pagination = issues_ns.model("IssuePagination", {
    'has_next': fields.Boolean('True if next page exists'),
    'has_prev': fields.Boolean('True if previous page exists'),
    'pages': fields.Integer('The total number of pages'),
    'page': fields.Integer('The current page number (1 indexed)'),
    'items': fields.List(fields.Nested(issue))
})
comment = issues_ns.model("Comment", {
    'text': fields.String("Comment text"),
    'issue_id': fields.Integer(),
    'author_id': fields.Integer(),
    'created_at': fields.DateTime('Comment creation date', readonly=True),
    'updated_at': fields.DateTime('Comment update Date', readonly=True),
    'id': fields.Integer(readonly=True)
})


@issues_ns.route('/paginate')
@issues_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
@issues_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Missing Authentication Token')
@issues_ns.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Bad Authentication Token')
@issues_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
class IssuesPaginate(Resource):

    @issues_ns.response(int(HTTPStatus.OK), 'Paginate through issues', issue_pagination)
    def get(self):
        args = request.args
        pagination = Issue.paginate(int(args.get("page", 1)), 25)
        return {
                   'has_next': pagination.has_next,
                   'has_prev': pagination.has_prev,
                   'pages': pagination.pages,
                   'page': pagination.page,
                   'items': IssueSchema(many=True).dump(pagination.items)
               }, 200


@issues_ns.route('/')
@issues_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
@issues_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Missing Authentication Token')
@issues_ns.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Bad Authentication Token')
@issues_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
class Issues(Resource):

    @issues_ns.response(int(HTTPStatus.OK), 'Fetch full list of  issues', [issue])
    def get(self):
        data = Issue.filter_by()
        return IssueSchema(many=True).dump(data)

    @issues_ns.expect(issue, validate=True)
    @issues_ns.response(int(HTTPStatus.CREATED), 'Created issue', issue)
    def post(self):
        json = request.get_json()
        data = IssueSchema().load(json)

        data.save()
        return IssueSchema().dump(data), 201


@issues_ns.route('/<issue_id>')
@issues_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
@issues_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Missing Authentication Token')
@issues_ns.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Bad Authentication Token')
@issues_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
class IssuesId(Resource):

    @issues_ns.response(int(HTTPStatus.OK), 'Get specific issue', issue)
    def get(self, issue_id):
        data = Issue.get(id=issue_id)

        if not data:
            abort(404, 'Issue not found')

        return IssueSchema().dump(data)

    @issues_ns.response(int(HTTPStatus.OK), 'Deleted issue')
    def delete(self, issue_id):
        data = Issue.get(id=issue_id)

        if not data:
            abort(404, 'Issue not found')

        data.delete()

        return "", 200

    @issues_ns.expect(issue, validate=True)
    @issues_ns.response(int(HTTPStatus.OK), 'Updated issue', issue)
    def put(self, issue_id):
        data_json = request.get_json()
        data = Issue.get(id=issue_id)

        if not data:
            abort(404, 'Issue not found')

        data.update(data_json)

        return IssueSchema.dump(data), 200


@issues_ns.route('/<issue_id>/comments')
class Comments(Resource):

    @issues_ns.response(int(HTTPStatus.OK), 'Fetch full list of comments', [comment])
    def get(self, issue_id):
        data = Comment.filter_by(issue_id=issue_id)
        return CommentSchema(many=True).dump(data)

    @jwt_required(optional=True)
    @issues_ns.expect(comment, validate=True)
    @issues_ns.response(int(HTTPStatus.CREATED), 'Created issue', comment)
    def post(self, issue_id):
        json = request.get_json()
        data = CommentSchema().load(json)

        data.save()
        return CommentSchema().dump(data), 201


@issues_ns.route('/<issue_id>/comments/<id>')
@issues_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation Error')
@issues_ns.response(int(HTTPStatus.UNAUTHORIZED), 'Missing Authentication Token')
@issues_ns.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Bad Authentication Token')
@issues_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error')
class CommentsId(Resource):

    @issues_ns.response(int(HTTPStatus.OK), 'Deleted comment')
    def delete(self, issue_id, id):
        data = Comment.get(issue_id=issue_id, id=id)

        if not data:
            abort(404, 'Comment not found')

        data.delete()

        return "", 200

    @issues_ns.expect(comment, validate=True)
    @issues_ns.response(int(HTTPStatus.OK), 'Created comment', comment)
    def put(self, issue_id, id):
        data_json = request.get_json()
        data = Comment.get(issue_id=issue_id, id=id)

        if not data:
            abort(404, 'Comment not found')

        data.update(data_json)
        return CommentSchema().dump(data), 200
