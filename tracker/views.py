from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Company
from .serializers import CompanySerializer


def home(request):
    return HttpResponse("Welcome to Job Application Tracker!")


def company_list(request):
    if request.method == "GET":
        company_name = request.GET.get("name")

        if company_name:
            return HttpResponse(f"Searching for {company_name}")

        return HttpResponse("Showing all companies.")

    return HttpResponse("Method not allowed.")


def company_detail(request, company_id):
    if request.method == "GET":
        return HttpResponse(f"Details for company number {company_id}")

    return HttpResponse("Method not allowed.")


@api_view(["GET", "POST"])
def company_list_api(request):

    if request.method == "GET":
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
