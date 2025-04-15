from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, reqparse

from src.models import Achievement, Task, User, db
from src.utils.swagger.model_to_swagger_schema import model_to_swagger_schema

task_parser = reqparse.RequestParser()
task_parser.add_argument('title', type=str, required=True)
task_parser.add_argument('description', type=str)
task_parser.add_argument('completed', type=bool)

ACHIEVEMENTS = [(50, "Primeiros Passos"), (100, "Produtivo(a)!"),
                (200, "Mestre da Organização")]


class TaskListResource(Resource):
    @swag_from({
        'tags': ['Tasks'],
        'summary': 'Listar tarefas',
        'description': 'Retorna uma lista de todas as tarefas do usuário.',
        'responses': {
            200: {
                'description': 'Lista de tarefas retornada com sucesso',
                'examples': {
                    'application/json': [{
                        'id': 1,
                        'title': 'Comprar pão'
                    }, {
                        'id': 2,
                        'title': 'Estudar Flask'
                    }]
                }
            },
            401: {
                'description': 'Usuário não autenticado'
            }
        }
    })
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=user_id).all()
        return [task.to_dict() for task in tasks], 200

    @swag_from({
        "tags": ["Tasks"],
        "summary": "Criar nova tarefa",
        'security': [{
            'BearerAuth': []
        }],
        "parameters": [{
            "name": "body",
            "in": "body",
            "required": True,
            "schema": model_to_swagger_schema(
                Task,
                exclude_fields=["id", "user_id", "completed"],
                required_fields=["title"])
        }],
        "responses": {
            201: {
                "description": "Tarefa criada com sucesso"
            },
            400: {
                "description": "Erro nos dados"
            }
        }
    })
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        args = task_parser.parse_args()
        task = Task(title=args['title'],
                    description=args.get('description', ''),
                    completed=args.get('completed', False),
                    user_id=user_id)
        print(task)
        db.session.add(task)
        db.session.commit()
        return task.to_dict(), 201


class TaskResource(Resource):
    @swag_from({
        'tags': ['Tasks'],
        'summary': 'Obter detalhes de uma tarefa específica',        
        'security': [{
            'BearerAuth': []
        }],
        'parameters': [{
            'name': 'task_id',
            'in': 'path',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }],
        'responses': {
            200: {
                'description': 'Tarefa encontrada'
            },
            404: {
                'description': 'Tarefa não encontrada'
            }
        }
    })
    @jwt_required()
    def get(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.get_or_404(task_id)
        if task.user_id != user_id:
            return {"error": "Acesso negado"}, 403
        return task.to_dict(), 200

    @swag_from({
        'tags': ['Tasks'],
        'summary': 'Atualizar uma tarefa',
        'security': [{
            'BearerAuth': []
        }],
        'parameters': [{
            'name': 'task_id',
            'in': 'path',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }],
        'requestBody': {
            'required': True,
            'content': {
                'application/json': {
                    'example': {
                        "title": "Atualizado",
                        "done": True
                    }
                }
            }
        },
        'responses': {
            200: {
                'description': 'Tarefa atualizada com sucesso'
            },
            404: {
                'description': 'Tarefa não encontrada'
            }
        }
    })
    @jwt_required()
    def put(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.get_or_404(task_id)
        if task.user_id != user_id:
            return {"error": "Acesso negado"}, 403

        args = task_parser.parse_args()

        was_completed = task.completed
        task.title = args.get('title', task.title)
        task.description = args.get('description', task.description)
        task.completed = args.get('completed', task.completed)

        user = User.query.get(user_id)

        if not was_completed and task.completed:
            if user:
                user.xp += 10
                for xp_value, name in ACHIEVEMENTS:
                    already_has = Achievement.query.filter_by(
                        user_id=user_id, name=name).first()
                    if user.xp >= xp_value and not already_has:
                        new_achievement = Achievement(name=name,
                                                      user_id=user_id)
                        db.session.add(new_achievement)
            db.session.commit()
            return task.to_dict(), 200

    @swag_from({
        'tags': ['Tasks'],
        'summary': 'Deletar uma tarefa',
        'security': [{
            'BearerAuth': []
        }],
        'parameters': [{
            'name': 'task_id',
            'in': 'path',
            'required': True,
            'schema': {
                'type': 'integer'
            }
        }],
        'responses': {
            204: {
                'description': 'Tarefa deletada com sucesso'
            },
            404: {
                'description': 'Tarefa não encontrada'
            }
        }
    })
    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.get_or_404(task_id)
        if task.user_id != user_id:
            return {"error": "Acesso negado"}, 403
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Tarefa deletada'}, 200
