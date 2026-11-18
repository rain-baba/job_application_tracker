from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Application, Company
from .serializers import ApplicationSerializer, CompanySerializer


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


@api_view(["GET", "POST"])  # Allow GET and POST requests
def company_list_api(request):

    # GET: Retrieve all companies from the database
    if request.method == "GET":
        companies = Company.objects.all()

        # Convert multiple company objects into JSON-compatible data
        serializer = CompanySerializer(companies, many=True)

        # Return the list of companies to the client
        return Response(serializer.data)

    # POST: Create a new company
    elif request.method == "POST":

        # Receive the submitted data and prepare it for validation
        serializer = CompanySerializer(data=request.data)

        # Check whether the submitted data is valid
        serializer.is_valid(raise_exception=True)

        # Save the validated company in the database
        serializer.save()

        # Return the newly created company with HTTP 201 status
        return Response(serializer.data, status=201)


@api_view(["GET", "PUT", "PATCH", "DELETE"])  # Allow GET requests only
def company_detail_api(request, company_id):

    # Find the company using its ID.
    # If it doesn't exist, return HTTP 404 Not Found.
    company = get_object_or_404(Company, id=company_id)

    if request.method == "GET":
        # Convert the company object into JSON-compatible data

        serializer = CompanySerializer(company)

        # Return the company's information to the client
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CompanySerializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "PATCH":
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        company.delete()
        return Response(status=204)


@api_view(["GET", "POST"])
def application_list_api(request):

    if request.method == "GET":
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
