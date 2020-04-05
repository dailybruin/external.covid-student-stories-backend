from django.shortcuts import render
from django.views import View
from django.db import connection
from django import http


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class StoryView(View):
    def get(self, request):
        def build_sql_param(field: str, params):
            return " OR ".join([field + " = '" + param.replace("'", "") + "'" for param in params])

        cursor = connection.cursor()
        param_exists = False
        sql_query = "SELECT * FROM student_stories_story"
        where_queries = []

        schools = request.GET.get("school", None)
        years = request.GET.get("year", None)
        if schools or years:
            sql_query += " WHERE "

        if schools:
            schools = schools.split(" ")
            where_queries.append(
                "(" + build_sql_param("school", schools) + ")")

        if years:
            years = years.split(" ")
            where_queries.append("(" + build_sql_param("year", years) + ")")

        sql_query += " AND ".join(where_queries)
        sql_query += " ORDER BY timestamp DESC"

        cursor.execute(sql_query)
        return http.JsonResponse(dictfetchall(cursor), safe=False)


class CreateStoryView(View):
    def post(self, request):
        keys = []
        vals = []
        for key, val in request.POST.items():
            keys.append(key)
            vals.append(val)
        vals = ["'" + val.replace("'", "") + "'" for val in vals]

        sql_query = "INSERT INTO student_stories_story (" + ", ".join(
            keys) + ") VALUES (" + ", ".join(vals) + ")"

        try:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            connection.commit()
            return http.JsonResponse(request.POST)
        except:
            return http.JsonResponse({"error": "Invalid post request"})
