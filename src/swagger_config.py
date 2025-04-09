swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "TaskUp - API de Autoaperfeiçoamento",
        "description": "Uma API para gerenciar tarefas com sistema de evolução de personagem.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT: Bearer <token>"
        }
    }
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
        }
    ],
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}