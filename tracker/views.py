from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Application, Company, InterviewRound
from .serializers import (
    ApplicationSerializer,
    CompanySerializer,
    InterviewRoundSerializer,
)


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


@extend_schema(
    methods=["GET"],
    tags=["1. Companies"],
    summary="List all companies",
    description="Retrieve all companies stored in the database.",
    responses={200: CompanySerializer(many=True)},
)
@extend_schema(
    methods=["POST"],
    tags=["1. Companies"],
    summary="Create a company",
    description="Create a new company by submitting its details.",
    request=CompanySerializer,
    responses={201: CompanySerializer},
)
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


@extend_schema(
    methods=["GET"],
    tags=["1. Companies"],
    summary="Retrieve a company",
    description="Retrieve the details of a company by its ID.",
    responses={200: CompanySerializer},
)
@extend_schema(
    methods=["PUT"],
    tags=["1. Companies"],
    summary="Update a company",
    description="Replace all editable fields of a company.",
    request=CompanySerializer,
    responses={200: CompanySerializer},
)
@extend_schema(
    methods=["PATCH"],
    tags=["1. Companies"],
    summary="Partially update a company",
    description="Update selected fields of a company.",
    request=CompanySerializer,
    responses={200: CompanySerializer},
)
@extend_schema(
    methods=["DELETE"],
    tags=["1. Companies"],
    summary="Delete a company",
    description="Delete a company by its ID.",
    responses={204: None},
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def company_detail_api(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "GET":
        serializer = CompanySerializer(company)
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


@extend_schema(
    methods=["GET"],
    tags=["2. Applications"],
    summary="List applications",
    description="Retrieve all job applications. Results can be filtered by status and application date.",
    parameters=[
        OpenApiParameter(
            name="status",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter applications by status (Wishlist, Applied, Interview, Offer, or Rejected).",
        ),
        OpenApiParameter(
            name="application_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter applications by application date (YYYY-MM-DD).",
        ),
    ],
    responses={200: ApplicationSerializer(many=True)},
)
@extend_schema(
    methods=["POST"],
    tags=["2. Applications"],
    summary="Create an application",
    description="Create a new job application.",
    request=ApplicationSerializer,
    responses={201: ApplicationSerializer},
)
@api_view(["GET", "POST"])
def application_list_api(request):
    if request.method == "GET":
        applications = Application.objects.all()

        status = request.query_params.get("status")
        if status:
            applications = applications.filter(status=status)

        application_date = request.query_params.get("application_date")
        if application_date:
            applications = applications.filter(application_date=application_date)

        applications = applications.order_by("-created_at")

        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(
    methods=["GET"],
    tags=["2. Applications"],
    summary="Retrieve an application",
    description="Retrieve the details of a job application by its ID.",
    responses={200: ApplicationSerializer},
)
@extend_schema(
    methods=["PUT"],
    tags=["2. Applications"],
    summary="Update an application",
    description="Replace all editable fields of an existing job application.",
    request=ApplicationSerializer,
    responses={200: ApplicationSerializer},
)
@extend_schema(
    methods=["PATCH"],
    tags=["2. Applications"],
    summary="Partially update an application",
    description="Update selected fields of an existing job application.",
    request=ApplicationSerializer,
    responses={200: ApplicationSerializer},
)
@extend_schema(
    methods=["DELETE"],
    tags=["2. Applications"],
    summary="Delete an application",
    description="Delete a job application by its ID.",
    responses={204: None},
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def application_detail_api(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == "GET":
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ApplicationSerializer(application, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = ApplicationSerializer(
            application,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        application.delete()
        return Response(status=204)


@extend_schema(
    methods=["GET"],
    tags=["3. Interview Rounds"],
    summary="List interview rounds",
    description="Retrieve all interview rounds. Results can be filtered by outcome and interview date.",
    parameters=[
        OpenApiParameter(
            name="outcome",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter interview rounds by outcome (Pending, Passed, or Failed).",
        ),
        OpenApiParameter(
            name="interview_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter interview rounds by interview date (YYYY-MM-DD).",
        ),
    ],
    responses={200: InterviewRoundSerializer(many=True)},
)
@extend_schema(
    methods=["POST"],
    tags=["3. Interview Rounds"],
    summary="Create an interview round",
    description="Create a new interview round for an existing job application.",
    request=InterviewRoundSerializer,
    responses={201: InterviewRoundSerializer},
)
@api_view(["GET", "POST"])
def interview_round_list_api(request):
    if request.method == "GET":
        interview_rounds = InterviewRound.objects.all()

        outcome = request.query_params.get("outcome")
        if outcome:
            interview_rounds = interview_rounds.filter(outcome=outcome)

        interview_date = request.query_params.get("interview_date")
        if interview_date:
            interview_rounds = interview_rounds.filter(
                interview_date__date=interview_date
            )

        interview_rounds = interview_rounds.order_by("-interview_date")

        serializer = InterviewRoundSerializer(interview_rounds, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = InterviewRoundSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(
    summary="List upcoming interviews",
    tags=["3. Interview Rounds"],
    description="Retrieve pending interview rounds scheduled for the current time or a future date, ordered by interview date.",
    responses={200: InterviewRoundSerializer(many=True)},
)
@api_view(["GET"])
def upcoming_interviews_api(request):
    interview_rounds = InterviewRound.objects.filter(
        outcome="Pending",
        interview_date__gte=timezone.now(),
    ).order_by("interview_date")

    serializer = InterviewRoundSerializer(interview_rounds, many=True)
    return Response(serializer.data)


@extend_schema(
    methods=["GET"],
    tags=["3. Interview Rounds"],
    summary="Retrieve an interview round",
    description="Retrieve the details of an interview round by its ID.",
    responses={200: InterviewRoundSerializer},
)
@extend_schema(
    methods=["PUT"],
    tags=["3. Interview Rounds"],
    summary="Update an interview round",
    description="Replace all editable fields of an existing interview round.",
    request=InterviewRoundSerializer,
    responses={200: InterviewRoundSerializer},
)
@extend_schema(
    methods=["PATCH"],
    tags=["3. Interview Rounds"],
    summary="Partially update an interview round",
    description="Update selected fields of an existing interview round.",
    request=InterviewRoundSerializer,
    responses={200: InterviewRoundSerializer},
)
@extend_schema(
    methods=["DELETE"],
    tags=["3. Interview Rounds"],
    summary="Delete an interview round",
    description="Delete an interview round by its ID.",
    responses={204: None},
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def interview_round_detail_api(request, interview_round_id):
    interview_round = get_object_or_404(InterviewRound, id=interview_round_id)

    if request.method == "GET":
        serializer = InterviewRoundSerializer(interview_round)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = InterviewRoundSerializer(interview_round, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = InterviewRoundSerializer(
            interview_round,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        interview_round.delete()
        return Response(status=204)


@extend_schema(
    summary="Get application pipeline",
    description="Return the total number of applications and counts grouped by application status.",
    tags=["2. Applications"],
    responses={
        200: inline_serializer(
            name="ApplicationPipelineResponse",
            fields={
                "total_applications": serializers.IntegerField(),
                "pipeline": serializers.ListField(
                    child=inline_serializer(
                        name="ApplicationPipelineItem",
                        fields={
                            "status": serializers.CharField(),
                            "total": serializers.IntegerField(),
                        },
                    )
                ),
            },
        )
    },
)
@api_view(["GET"])
def application_pipeline_api(request):
    pipeline = Application.objects.values("status").annotate(total=Count("id"))

    counts = {item["status"]: item["total"] for item in pipeline}
    total_applications = Application.objects.count()

    result = [
        {
            "status": status,
            "total": counts.get(status, 0),
        }
        for status, label in Application.Status.choices
    ]

    return Response(
        {
            "total_applications": total_applications,
            "pipeline": result,
        }
    )
