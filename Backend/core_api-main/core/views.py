from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Website, Category, EntryCount, websiteFlagCount
from django.db.models import Count, Sum
from django.http import JsonResponse
from utils.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict
from django.db.models.functions import ExtractMonth, ExtractYear
from calendar import month_name


@staff_member_required
def statistics_view(request):
    return render(request, "statistics.html", {})


@staff_member_required
def getMonths(request):
    
    all_web = list(Website.objects.all().order_by('webName').values_list('webName', flat=True)) 
    res = ['All']
    res.extend(all_web)
    return JsonResponse({'options' : res})

@staff_member_required
def getYear(request):
    return JsonResponse({'options': [2024, 2023]})


@staff_member_required
def monthDist(request, year):
    entry_counts = EntryCount.objects.filter(year=year)

    # Initialize lists to store names of months and counts
    months_list = []
    counts_list = []

    # Iterate through the months of the year
    for month in range(1, 13):
        # Get the entry count for the current month, or 0 if not found
        entry_count = entry_counts.filter(month=month).first()
        entry_count = entry_count.count if entry_count else 0


        # Append the month name and count to the respective lists
        months_list.append(month_name[month])
        counts_list.append(entry_count)

    return JsonResponse({
        "title": f"Monthly distribution for {year}",
        "data": {
            "labels": months_list,
            "datasets": [{
                "label": "Counts",
                "data": counts_list,
                "backgroundColor": "rgba(75, 192, 192, 0.6)",
                "borderColor": "rgba(75, 192, 192)"
            }]
        },
    })

@staff_member_required
def get_web_vs_count(request, webName):
    websites = []
    category_counts = []
    
    websites_with_counts = Website.objects.annotate(category_count=Count('category'))
    # Retrieve websites along with the count of categories using annotate
    if(webName=='All'):
    # Iterate through the queryset and populate the lists
        for website in websites_with_counts:
            websites.append(website.webName)
            category_counts.append(website.category_count)
    
    else:
        cnt = Website.objects.filter(webName=webName).annotate(category_count=Count('category'))
        websites.append(webName)
        category_counts.append(cnt.first().category_count)

    return JsonResponse({
        "title": "Website vs Catrgory Count",
        "data": {
            "labels": websites,
            "datasets": [{
                "label": "Count",
                "backgroundColor": [
          "rgba(255, 99, 132, 0.4)",
          "rgba(54, 162, 235, 0.4)",
          "rgba(255, 206, 86, 0.4)",
          "rgba(75, 192, 192, 0.4)",
          "rgba(153, 102, 255, 0.4)",
          "rgba(255, 159, 64, 0.4)",
          "rgba(255, 99, 132, 0.4)",
          "rgba(54, 162, 235, 0.4)",
          "rgba(255, 206, 86, 0.4)",
          "rgba(75, 192, 192, 0.4)",
          "rgba(153, 102, 255, 0.4)",
          "rgba(255, 159, 64, 0.4)"
        ],
        "borderColor": [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)"
        ],
        "borderWidth" : 1,
                "data": category_counts,
            }]
        },
    })

@staff_member_required
def categoryDist(request):
    all_categories = Category.objects.all()
    total_count = sum(category.count for category in all_categories)
    category_names = []
    category_percentages = []
    for category in all_categories:
        category_names.append(category.patternName)
        percentage = (category.count / total_count) * 100 if total_count > 0 else 0
        category_percentages.append(percentage)
    return JsonResponse({
        "title": "Category Share in Market",
        "data": {
            "labels": category_names,
            "datasets": [{
                "label": "Percentage (%)",
                "backgroundColor": [
          "rgba(255, 99, 132, 0.4)",
          "rgba(54, 162, 235, 0.4)",
          "rgba(255, 206, 86, 0.4)",
          "rgba(75, 192, 192, 0.4)",
          "rgba(153, 102, 255, 0.4)",
          "rgba(255, 159, 64, 0.4)",
          "rgba(255, 99, 132, 0.4)",
          "rgba(54, 162, 235, 0.4)",
          "rgba(255, 206, 86, 0.4)",
          "rgba(75, 192, 192, 0.4)",
          "rgba(153, 102, 255, 0.4)",
          "rgba(255, 159, 64, 0.4)"
        ],
        "borderColor": [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)"
        ],
        "borderWidth" : 1,
                "data": category_percentages,
            }]
        },
    })

@staff_member_required
def get_monthly_counts_for_website(request, year, webName):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    try:
        # Get the website instance
        website = Website.objects.get(webName=webName)

        # Initialize a list to store counts for all months
        monthly_counts = [0] * 12

        # Query WebsiteVisitCount for the given website and year
        website_visit_counts = websiteFlagCount.objects.filter(
            website=website,
            year=year
        )

        # Update the list with counts for each month
        for visit_count in website_visit_counts:
            monthly_counts[visit_count.month - 1] = visit_count.count

        return JsonResponse({
        "title": f"Monthly distribution of {webName} for {year}",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Counts",
                "data": monthly_counts,
                "backgroundColor": "rgba(255, 99, 132, 0.4)",
                "borderColor": "rgba(255, 99, 132)"
            }]
        },
    })

    except Website.DoesNotExist:
        # Return a list of 12 zeros if the website is not found
        return JsonResponse({
        "title": f"Monthly distribution of {webName} for {year}",
        "data": {
            "labels": months,
            "datasets": [{
                "label": "Counts",
                "data": [0]*12,
                "backgroundColor": "rgba(75, 192, 192, 0.6)",
                "borderColor": "rgba(75, 192, 192)"
            }]
        },
    })
