### ⚠️ Auto-generated, edit only the sections between the blockgen markers.

import django
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import path
import sys

### <<[ custom_imports ]>>
# Place your imports here
import database
import json
### <<[ end ]>>

@method_decorator(csrf_exempt, name="dispatch")
class TodosView(View):
    def get(self, request, ):
        """ List all todos """
        ### <<[ list_todos ]>>
        with database.connect() as conn:
            rows = conn.execute("SELECT * FROM todos ORDER BY id").fetchall()
        return JsonResponse([database.row_to_dict(r) for r in rows], safe=False)
        ### <<[ end ]>>

    def post(self, request, ):
        """ Create a new todo """
        ### <<[ create_todo ]>>
        data = json.loads(request.body)
        with database.connect() as conn:
            cursor = conn.execute(
                "INSERT INTO todos (title, done) VALUES (?, ?)",
                (data["title"], int(data.get("done", False)))
            )
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return JsonResponse(database.row_to_dict(row), status=201)
        ### <<[ end ]>>

@method_decorator(csrf_exempt, name="dispatch")
class Todos_IdView(View):
    def get(self, request, id):
        """ Get a todo by id """
        ### <<[ get_todo ]>>
        with database.connect() as conn:
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
        if row is None:
            return JsonResponse({"error": "not found"}, status=404)
        return JsonResponse(database.row_to_dict(row))
        ### <<[ end ]>>

    def put(self, request, id):
        """ Update a todo """
        ### <<[ update_todo ]>>
        data = json.loads(request.body)
        with database.connect() as conn:
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
            if row is None:
                return JsonResponse({"error": "not found"}, status=404)
            title = data.get("title", row["title"])
            done  = int(data.get("done", row["done"]))
            conn.execute("UPDATE todos SET title = ?, done = ? WHERE id = ?", (title, done, id))
            row = conn.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
        return JsonResponse(database.row_to_dict(row))
        ### <<[ end ]>>

    def delete(self, request, id):
        """ Delete a todo """
        ### <<[ delete_todo ]>>
        with database.connect() as conn:
            row = conn.execute("SELECT id FROM todos WHERE id = ?", (id,)).fetchone()
            if row is None:
                return JsonResponse({"error": "not found"}, status=404)
            conn.execute("DELETE FROM todos WHERE id = ?", (id,))
        return JsonResponse({}, status=204)
        ### <<[ end ]>>

urlpatterns = [
    path("todos", TodosView.as_view()),
    path("todos/<int:id>", Todos_IdView.as_view()),
]

if __name__ == "__main__":
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
    )
    django.setup()

    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "runserver", "127.0.0.1:8000"] + sys.argv[1:])
