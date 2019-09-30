from django.shortcuts import render, redirect
from django.views import View
from charity.models import Institution, Donation, Category
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib.auth.models import User, auth


class LandingPage(View):
    def get(self,request):
        bags = list(Donation.objects.aggregate(Sum('quantity')).values())[0]    # robimy listę i wyciągamy pierwszy element
        institutions = Donation.objects.values('institution_id')
        institution_list = []
        for inst in institutions:
            if inst in institution_list:
                pass
            else:
                institution_list.append(inst)
        institution_count = len(institution_list)
        foundations_list = Institution.objects.filter(type=1)
        nongov_organizations_list = Institution.objects.filter(type=2)
        local_list = Institution.objects.filter(type=3)
        paginator_foundations = Paginator(foundations_list, 2)
        page_foundations = request.GET.get("page")
        foundations = paginator_foundations.get_page(page_foundations)
        paginator_nongov = Paginator(nongov_organizations_list, 2)
        page_nongov = request.GET.get("page")
        nongov_organizations = paginator_nongov.get_page(page_nongov)
        paginator_local = Paginator(local_list, 2)
        page_local = request.GET.get("page")
        local = paginator_local.get_page(page_local)
        return render(request, 'index.html', {"bags":bags,
                                              "institution_count": institution_count,
                                              "foundations": foundations,
                                              "nongov_organizations":nongov_organizations,
                                              "local":local})


class AddDonation(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, "form.html", {"categories":categories,
                                             "institutions": institutions})

    def post(self, request):
        quantity = request.POST["bags"]
        institution = Institution.objects.get(name=request.POST["organization"])
        selected_categories = request.POST.getlist("categories")
        address = request.POST["address"]
        phone_number = request.POST["phone"]
        city = request.POST["city"]
        zip_code = request.POST["postcode"]
        pick_up_date = request.POST["date"]
        pick_up_time = request.POST["time"]
        pick_up_comment = request.POST["more_info"]
        user = request.user
        new_donation = Donation.objects.create(quantity=quantity,
                                               institution=institution,
                                               address=address,
                                               phone_number=phone_number,
                                               city=city,
                                               zip_code=zip_code,
                                               pick_up_date=pick_up_date,
                                               pick_up_time=pick_up_time,
                                               pick_up_comment=pick_up_comment,
                                               user=user)
        for category_id in selected_categories:
            new_donation.categories.add(category_id)
        return redirect("/test")


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return redirect("/register")


class Register(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        first_name = request.POST["name"]
        last_name = request.POST["surname"]
        username = request.POST["email"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        password2 = request.POST["password2"]
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, "register.html")
            else:
                user = User.objects.create_user(username=username, password=password1, first_name=first_name,
                                                last_name=last_name, email=email)
                user.save()
        return redirect("/login")


class TestForFormConfirmation(View):
    def get(self, request):
        return render(request, "form-confirmation.html")


def logout_view(request):
    auth.logout(request)
    return redirect("/")


class UserProfileView(View):
    def get(self,request, user_id):
        user = User.objects.get(id=user_id)
        return render(request, 'user_profile.html', {"user": user})

    def post(self, request, user_id):
        if "taken" in request.POST:
            taken_status = Donation.objects.get(id=request.POST.get("taken"))
            taken_status.is_taken = True
            taken_status.save()
        else:
            not_taken_status = Donation.objects.get(pk=request.POST.get("not-taken"))
            not_taken_status.is_taken = False
            not_taken_status.save()
        return render(request, 'user_profile.html')
