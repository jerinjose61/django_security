from django.shortcuts import render, redirect
from app.models import Employee, Blog
from app.forms import BlogForm
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db import connection
import subprocess, shlex
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "app/index.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "New user created! Please sign in.")
            return redirect('app:index')
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form":form})

@login_required
def home(request):
    return render(request, "app/home.html")

@login_required
def employees(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        department = request.POST.get("department")
        designation = request.POST.get("designation")

        # Saving to DB using Django ORM - the best way
        Employee.objects.create(emp_id=emp_id, first_name=first_name, last_name=last_name,
        age=age, sex=sex, department=department, designation=designation)

        # # Direct SQL Queries - the wrong way
        # cursor = connection.cursor()
        # query = "INSERT INTO app_employee (emp_id, first_name, last_name, age, sex, department, designation) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (emp_id, first_name, last_name, age, sex, department, designation)
        # cursor.execute(query)

        # # Direct SQL Queries - the correct way
        # cursor = connection.cursor()
        # cursor.execute("INSERT INTO app_employee (emp_id, first_name, last_name, age, sex, department, designation) VALUES (%s, %s, %s, %s, %s, %s, %s)", [emp_id, first_name, last_name, age, sex, department, designation])

        return redirect("app:employees")
    else:
        # Fetch all employees using Django ORM
        employees = Employee.objects.all()

        return render(request, 'app/employees.html',
        {"employees":employees})

@login_required
@csrf_exempt
def search_employees(request):
    if request.is_ajax():
        search_term = request.POST.get('searchTerm')

        # Searching employees using Django ORM - the best way
        employees = Employee.objects.filter(first_name__icontains=search_term)

        # # Searching employees using raw() - the wrong way
        # query = "SELECT * FROM app_employee WHERE first_name ILIKE '%s';" % search_term
        # employees = Employee.objects.raw(query)

        # # Searching employees using raw() - the correct way
        # employees = Employee.objects.raw('SELECT * FROM app_employee WHERE first_name ILIKE %s;',[search_term])

        # # Searching employees using extra() - the wrong way
        # employees = Employee.objects.extra(where=["first_name ILIKE '%s'" % search_term])

        # # Searching employees using extra() - the correct way
        # employees = Employee.objects.extra(where=['first_name ILIKE %s'], params=[search_term])

        html = render_to_string('app/search_employees.html',
        {'employees':employees})

        return HttpResponse(html)

@login_required
def dns_lookup(request):
    if request.method == "POST":
        domain_name = request.POST.get("domain_name")

        # # DNS Lookup - the wrong way
        # command = "nslookup {}".format(domain_name)
        # output = subprocess.check_output(command, shell=True, encoding='UTF-8')
        # return render(request, 'app/dns_lookup.html', {'output':output,
        # 'domain_name':domain_name})

        # # DNS Lookup - the better way
        # try:
        #     safe_domain_name = shlex.quote(domain_name)
        #     command = "nslookup {}".format(safe_domain_name)
        #     output = subprocess.check_output(command, shell=True, encoding='UTF-8')
        #
        #     return render(request, 'app/dns_lookup.html', {'output':output,
        #     'domain_name':domain_name})
        # except subprocess.CalledProcessError:
        #     return render(request, 'app/dns_lookup.html', {'output':"Invalid Input",
        #     'domain_name':domain_name})


        # DNS Lookup - the best way - without shell=True
        try:
            raw_command = "nslookup {}".format(domain_name)
            safe_command = shlex.split(raw_command)
            print(safe_command)
            output = subprocess.check_output(safe_command, encoding='UTF-8')

            return render(request, 'app/dns_lookup.html', {'output':output,
            'domain_name':domain_name})
        except subprocess.CalledProcessError:
            return render(request, 'app/dns_lookup.html', {'output':"Invalid Input",
            'domain_name':domain_name})

        ## Note - Avoid using the deprecated os module

    else:
        return render(request, "app/dns_lookup.html")
