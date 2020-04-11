from django.shortcuts import render
from django import http
from django.db.models import Q
from django.core import serializers
from .models import Story
from django.core.paginator import Paginator
from rest_framework.views import APIView
from datetime import datetime, timedelta


class TestView(APIView):
    def get(self, request):
        return http.HttpResponse("Hello World")


class StoryView(APIView):
    def get(self, request):
        schools = request.GET.get("school", None)
        years = request.GET.get("year", None)
        majors = request.GET.get("major", None)
        # 0 for latest, 1 for most top, 2 for hot
        try:
            sort = max(int(request.GET.get("sort", 0)), 0)
        except:
            sort = 0
        try:
            i = max(int(request.GET.get("i", 1)), 1)
        except:
            i = 1
        # 0 for none, 1 love, 2 sad, 3 up, 4 angry
        try:
            reax = max(int(request.GET.get("reax", 0)), 0)
        except:
            reax = 0

        query = Story.objects.exclude(responseCommunity__isnull=True, responseCommunity__exact='',
                                      responseAffected__isnull=True, responseAffected__exact='',
                                      responseElse__isnull=True, responseElse__exact='',
                                      responseDoneDifferently__isnull=True, responseDoneDifferently__exact='')
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

        query = query.filter(created__gt=datetime.now() - timedelta(hours=8)).order_by("-reactTotal") if sort == 2 \
            else query.order_by("-reactTotal") if sort == 1 \
            else query.order_by("-timestamp")

        query = query.order_by("-reactLove") if reax == 1 \
            else query.order_by("-reactSad") if reax == 2 \
            else query.order_by("-reactUp") if reax == 3 \
            else query.order_by("reactAngry") if reax == 4 \
            else query

        paginator = Paginator(query, 10)
        post_list = serializers.serialize('json', list(paginator.page(i)))
        return http.HttpResponse(post_list, content_type="text/json-comment-filtered")


class ReactView(APIView):
    def post(self, request):
        try:
            if "pk" not in request.data:
                return http.JsonResponse({"error": "React update invalid"})

            post = Story.objects.get(pk=request.data["pk"])

            if "react" in request.data:
                react = request.data["react"]
            else:
                react = None

            if "oldReact" in request.data:
                old_react = request.data["oldReact"]
            else:
                old_react = None

            if react is None:
                if react == 0:
                    post.reactLove += 1
                elif react == 1:
                    post.reactSad += 1
                elif react == 2:
                    post.reactUp += 1
                else:
                    post.reactAngry += 1

            if old_react is None:
                if old_react == 0:
                    post.reactLove -= 1
                elif old_react == 1:
                    post.reactSad -= 1
                elif old_react == 2:
                    post.reactUp -= 1
                else:
                    post.reactAngry -= 1

            post.save()
            return http.JsonResponse({"message": "React update successful"})
        except:
            return http.JsonResponse({"error": "React update invalid"})


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


def wordfreq(string):
    # all the words to filter out...
    stopwords = set()
    with open("stopwords.txt", "r") as f:
        for line in f:
            word = line[:-1]
            stopwords.add(word)

    # Clean text and lower case all words
    for char in "1234567890-.,\n":
        string = string.replace(char, " ")
    string = string.lower()

    # turn string into array of words
    wordlist = string.split()

    # filter out garbage words
    wordlist = [w for w in wordlist if w not in stopwords]

    # Given a list of words, return a dictionary of word-frequency pairs.
    wordfreq = [wordlist.count(p) for p in wordlist]
    wordfreq_map = dict(list(zip(wordlist, wordfreq)))

    # sort in descending order
    aux = [(wordfreq_map[key], key) for key in wordfreq_map]
    aux.sort()
    aux.reverse()
    wordfreq_map = aux

    # do something to combine corona, coronavirus, corona virus, corona-virus, covid, covid19, covid 19, and covid-19
    # or just filter them idk lol

    return wordfreq_map
