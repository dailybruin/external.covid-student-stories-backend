from django.shortcuts import render
from django import http
from django.db.models import Q
from django.core import serializers
from .models import Story, Word
from django.core.paginator import Paginator
from rest_framework.views import APIView
from datetime import datetime, timedelta
from rest_framework.decorators import api_view

from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie


class TestView(APIView):
    def get(self, request):
        return http.HttpResponse("Hello World")


class StoryView(APIView):
    def get(self, request):
        schools = request.GET.get("school", None)
        years = request.GET.get("year", None)
        majors = request.GET.get("major", None)
        # 0 for none, 1 for CA, 2 for OOS, 3 for international
        try:
            sort = max(int(request.GET.get("home", 0)), 0)
        except:
            sort = 0
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

        commFilter = Q(responseCommunity__isnull=True) | Q(
            responseCommunity__exact='')
        affectFilter = Q(responseAffected__isnull=True) | Q(
            responseAffected__exact='')
        elseFilter = Q(responseElse__isnull=True) | Q(responseElse__exact='')
        diffFilter = Q(responseDoneDifferently__isnull=True) | Q(
            responseDoneDifferently__exact='')

        query = Story.objects.filter(approvalState="approved")
        query = query.exclude(
            commFilter & affectFilter & elseFilter & diffFilter)

        if schools:
            schools = schools.split(" ")
            school_query = None
            for school in schools:
                try:
                    school_query |= Q(school=school.replace(
                        "_", " ").replace("'", ""))
                except:
                    school_query = Q(school=school.replace(
                        "_", " ").replace("'", ""))
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
                    major_query |= Q(major=major.replace(
                        "_", " ").replace("'", ""))
                except:
                    major_query = Q(major=major.replace(
                        "_", " ").replace("'", ""))
            query = query.filter(major_query)

        query = query.filter(created__gt=datetime.now() - timedelta(hours=8)).order_by("-reactTotal") if sort == 2 \
            else query.order_by("-reactTotal") if sort == 1 \
            else query.order_by("-timestamp")

        query = query.filter(state="California") if sort == 1 \
            else query.exclude(state="California").filter(Q(country="United States of America (USA)") | Q(state__isnull=False)) if sort == 2 \
            else query.filter(country__isnull=False).exclude(country="United States of America (USA)") if sort == 3 \
            else query

        query = query.order_by("-reactLove") if reax == 1 \
            else query.order_by("-reactSad") if reax == 2 \
            else query.order_by("-reactUp") if reax == 3 \
            else query.order_by("-reactAngry") if reax == 4 \
            else query

        paginator = Paginator(query, 10)
        if i > paginator.num_pages:
            return http.HttpResponse({"totalcount": query.count(), "data": []}, content_type="text/json-comment-filtered")

        post_list = serializers.serialize('json', list(paginator.page(i)))
        return http.HttpResponse({"totalcount": query.count(), "data": post_list}, content_type="text/json-comment-filtered")


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

            if react is not None:
                if react == 0:
                    post.reactLove += 1
                elif react == 1:
                    post.reactSad += 1
                elif react == 2:
                    post.reactUp += 1
                else:
                    post.reactAngry += 1
                post.reactTotal += 1

            if old_react is not None:
                if old_react == 0:
                    post.reactLove = max(post.reactLove - 1, 0)
                elif old_react == 1:
                    post.reactSad = max(post.reactSad - 1, 0)
                elif old_react == 2:
                    post.reactUp = max(post.reactUp - 1, 0)
                else:
                    post.reactAngry = max(post.reactAngry - 1, 0)
                post.reactTotal = max(post.reactTotal - 1, 0)

            post.save()
            return http.JsonResponse({"message": "React update successful"})
        except:
            return http.JsonResponse({"error": "React update invalid"})


class CreateStoryView(APIView):
    def post(self, request):
        try:
            data = request.data
            Story.objects.create(school=data["school"],
                                 major=data["major"],
                                 year=data["year"],
                                 state=data.get("state"),
                                 city=data["city"],
                                 country=data.get("country"),
                                 worryFinancial=data["worryFinancial"],
                                 worryHousing=data["worryHousing"],
                                 worryAcademic=data["worryAcademic"],
                                 worryGovernment=data["worryGovernment"],
                                 worryPhysical=data["worryPhysical"],
                                 worryMental=data["worryMental"],
                                 responseCommunity=data.get(
                                     "responseCommunity"),
                                 responseAffected=data.get("responseAffected"),
                                 responseElse=data.get("responseElse"),
                                 comfortablePublish=data["comfortablePublish"],
                                 knowPositive=data["knowPositive"],
                                 currentLocation=data["currentLocation_other"] if data[
                                     "currentLocation"] == "" else data["currentLocation"],
                                 responseDoneDifferently=data.get(
                                     "responseDoneDifferently"),
                                 artCredit=data.get("artCredit"),
                                 approvalState='undecided' if data["comfortablePublish"] == 'Y' else 'rejected')

            return http.JsonResponse(data)
        except:
            return http.JsonResponse({"error": "Invalid post request", "data": request.data})


class StatisticsView(APIView):
    def get(self, request):
        response = {'feelings': {}, 'curr_location_breakdown': {}}

        query = Story.objects.filter(approvalState="approved")

        num_know_positives = query.filter(knowPositive="Y").count()
        response["numKnowPositives"] = num_know_positives

        num_stories = query.count()
        num_offcampus = query.filter(
            currentLocation="School (Off-campus)").count()
        num_oncampus = query.filter(
            currentLocation="School (On-campus)").count()
        num_home = query.filter(currentLocation="Home").count()
        num_other = query.exclude(currentLocation="Home").exclude(
            currentLocation="School (On-campus)").exclude(currentLocation="School (Off-campus)").count()

        response['curr_location_breakdown']['offCampus'] = num_offcampus
        response['curr_location_breakdown']['onCampus'] = num_oncampus
        response['curr_location_breakdown']['home'] = num_home
        response['curr_location_breakdown']['other'] = num_other

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
            result = query.filter(worryFinancial=abbrev).count()
            response["feelings"]["finance"][feel] = result

            result = query.filter(worryHousing=abbrev).count()
            response["feelings"]["housing"][feel] = result

            result = query.filter(worryAcademic=abbrev).count()
            response["feelings"]["academic"][feel] = result

            result = query.filter(worryGovernment=abbrev).count()
            response["feelings"]["government"][feel] = result

            result = query.filter(worryPhysical=abbrev).count()
            response["feelings"]["physical"][feel] = result

            result = query.filter(worryMental=abbrev).count()
            response["feelings"]["mental"][feel] = result

        allwords = Word.objects.all()
        response["words"] = [
            {"text": record.word, "value": record.charcount} for record in allwords]

        return http.JsonResponse(response)


def wordfreq(string):
    # all the words to filter out...
    stopwords = set()
    with open("stopwords.txt", "r") as f:
        for line in f:
            word = line[:-1]
            stopwords.add(word)

    # Clean text and lower case all words
    for char in "'’1234567890-.,\n":
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


# Approval stuff
@ensure_csrf_cookie
def admin_table_page(request):

    if not request.user.is_authenticated:
        # admin login page
        return redirect("/admin/login/?next="+reverse("vetting-table"))

    # if we got here, they are authenticated
    stories = Story.objects.all().order_by('-id')

    filterByApprovalState = request.GET.get("approvalState", None)
    if filterByApprovalState:
        stories = stories.filter(approvalState=filterByApprovalState)

    # string describing what data the server is showing
    # e.g: showing only undecided posts
    showing = "all"
    if filterByApprovalState:
        showing = filterByApprovalState

    return render(request, "vetting_table.html", {
        "stories": stories,
        "showing": showing
    }
    )


def updateCloud(res):
    if res and res != "":
        freqs = wordfreq(res)
        for num, key in freqs:
            try:
                word = Word.objects.get(word=key)
                word.charcount += num
                word.save()
            except:
                Word.objects.create(word=key, charcount=num)


@api_view(['POST'])
def approve(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'no'}, status=403)

    instance = get_object_or_404(Story, id=id)
    instance.approvalState = 'approved'
    instance.save()

    try:
        instance = get_object_or_404(Story, id=id)
        updateCloud(instance.responseElse)
        updateCloud(instance.responseCommunity)
        updateCloud(instance.responseAffected)
        updateCloud(instance.responseDoneDifferently)
        instance.save()
    except:
        return JsonResponse({"message": f'{id} has been approved, but cloud failed'})

    return JsonResponse({"success": f'{id} has been approved'})


@api_view(['POST'])
def reject(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'no'}, status=403)

    instance = get_object_or_404(Story, id=id)
    instance.approvalState = 'rejected'
    instance.save()
    return JsonResponse({"success": f'{id} has been rejected'})
