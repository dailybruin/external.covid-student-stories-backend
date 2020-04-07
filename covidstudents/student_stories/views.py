from django.shortcuts import render
# from django.views import View
from django.db import connection
from django import http
from django.db.models import Q
from .models import Story
from django.core.paginator import Paginator
from rest_framework.views import APIView


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class TestView(APIView):
    def get(self, request):
        return http.HttpResponse("Hello World")


class StoryView(APIView):
    def get(self, request):
        # def build_sql_param(field: str, params):
        #     return " OR ".join([field + " = '" + param.replace("'", "") + "'" for param in params])

        cursor = connection.cursor()
        param_exists = False
        # sql_query = "SELECT * FROM student_stories_story"
        where_queries = []

        schools = request.GET.get("school", None)
        years = request.GET.get("year", None)
        majors = request.GET.get("major", None)
        try:
            i = max(int(request.GET.get("i", 1)), 1)
        except:
            i = 1

        # below this line is using django queries
        query = Story.objects.all()
        if schools:
            schools = schools.split(" ")
            school_query = None
            for school in schools:
                try:
                    school_query |= Q(school=school.replace("'", ""))
                except:
                    school_query = Q(school=school.replace("'", ""))
            query = query.filter(school_query)

        if years:
            years = years.split(" ")
            year_query = None
            for year in years:
                try:
                    year_query |= Q(year=year.replace("'", ""))
                except:
                    year_query = Q(year=year.replace("'", ""))
            query = query.filter(year_query)

        if majors:
            majors = majors.split(" ")
            major_query = None
            for major in majors:
                try:
                    major_query |= Q(major=major.replace("'", ""))
                except:
                    major_query = Q(major=major.replace("'", ""))
            query = query.filter(major_query)

        paginator = Paginator(query, 10)
        return http.JsonResponse(list(paginator.page(i)), safe=False)

        # if schools or years or majors:
        #     sql_query += " WHERE "

        # if schools:
        #     schools = schools.split(" ")
        #     where_queries.append(
        #         "(" + build_sql_param("school", schools) + ")")

        # if years:
        #     years = years.split(" ")
        #     where_queries.append("(" + build_sql_param("year", years) + ")")

        # if majors:
        #     majors = majors.split(" ")
        #     where_queries.append("(" + build_sql_param("major", majors) + ")")

        # if i != 0:
        #     i = int(i)
        # offset = i * 10

        # sql_query += " AND ".join(where_queries)
        # sql_query += " ORDER BY timestamp DESC OFFSET " + \
        #     str(offset) + " ROWS FETCH NEXT 10 ROWS ONLY"

        # cursor.execute(sql_query)
        # return http.JsonResponse(dictfetchall(cursor), safe=False)


class CreateStoryView(APIView):
    def post(self, request):
        # keys = []
        # vals = []
        # for key, val in request.POST.items():
        #     keys.append(key)
        #     vals.append(val)
        # vals = ["'" + val.replace("'", "") + "'" for val in vals]

        # sql_query = "INSERT INTO student_stories_story (" + ", ".join(
        #     keys) + ") VALUES (" + ", ".join(vals) + ")"

        try:
            # cursor = connection.cursor()
            # cursor.execute(sql_query)
            # connection.commit()
            Story.objects.create(**request.POST)
            return http.JsonResponse(request.POST)
        except:
            return http.JsonResponse({"error": "Invalid post request"})


class StatisticsView(APIView):
    def get(self, request):
        return http.JsonResponse({"error": "hi"})
