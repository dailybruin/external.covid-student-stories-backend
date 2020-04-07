from django.shortcuts import render
from django import http
from django.db.models import Q
from django.core import serializers
from .models import Story
from django.core.paginator import Paginator
from rest_framework.views import APIView


class TestView(APIView):
    def get(self, request):
        return http.HttpResponse("Hello World")


class StoryView(APIView):
    def get(self, request):
        schools = request.GET.get("school", None)
        years = request.GET.get("year", None)
        majors = request.GET.get("major", None)
        try:
            i = max(int(request.GET.get("i", 1)), 1)
        except:
            i = 1

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
        post_list = serializers.serialize('json', list(paginator.page(i)))
        return http.HttpResponse(post_list, content_type="text/json-comment-filtered")


class CreateStoryView(APIView):
    def post(self, request):
        try:
            Story.objects.create(**request.data)
            return http.JsonResponse(request.data)
        except:
            return http.JsonResponse({"error": "Invalid post request"})


class StatisticsView(APIView):
    def get(self, request):
        response = {'feelings': {}, 'curr_location_breakdown': {}}

        num_know_positives = Story.objects.filter(knowPositive="Y").count()
        response["numKnowPositives"] = num_know_positives

        num_stories = Story.objects.all().count()
        num_offcampus = Story.objects.filter(
            currentLocation="School (Off-campus)").count()
        num_oncampus = Story.objects.filter(
            currentLocation="School (On-campus)").count()
        num_home = Story.objects.filter(currentLocation="Home").count()
        num_other = Story.objects.exclude(currentLocation="Home").exclude(
            currentLocation="School (On-campus)").exclude(currentLocation="School (Off-campus)").count()

        response['curr_location_breakdown']['offCampus'] = num_offcampus / num_stories
        response['curr_location_breakdown']['onCampus'] = num_oncampus / num_stories
        response['curr_location_breakdown']['home'] = num_home / num_stories
        response['curr_location_breakdown']['other'] = num_other / num_stories

        response['count'] = num_stories

        feelings = {'NW': 'Not worried',
                    'SW': 'Somewhat worried', 'VW': 'Very Worried'}
        response["feelings"]["finance"] = {}
        response["feelings"]["housing"] = {}
        response["feelings"]["academic"] = {}
        response["feelings"]["government"] = {}
        response["feelings"]["physical"] = {}
        response["feelings"]["mental"] = {}
        for abbrev, feel in feelings.items():
            result = Story.objects.filter(worryFinancial=abbrev).count()
            response["feelings"]["finance"][feel] = result

            result = Story.objects.filter(worryHousing=abbrev).count()
            response["feelings"]["housing"][feel] = result

            result = Story.objects.filter(worryAcademic=abbrev).count()
            response["feelings"]["academic"][feel] = result

            result = Story.objects.filter(worryGovernment=abbrev).count()
            response["feelings"]["government"][feel] = result

            result = Story.objects.filter(worryPhysical=abbrev).count()
            response["feelings"]["physical"][feel] = result

            result = Story.objects.filter(worryMental=abbrev).count()
            response["feelings"]["mental"][feel] = result

        return http.JsonResponse(response)
