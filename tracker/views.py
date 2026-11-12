from django.http import HttpResponse


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
