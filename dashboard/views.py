from datetime import date

from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import FoodAcceptor, FoodDonare, Notification
from django.contrib.auth.decorators import login_required
from .forms import FoodRequestForm
from django.views.generic.edit import FormView 
from django.views.generic.edit import ModelFormMixin
from django.http import HttpResponseRedirect

# Create your views here.


def home_authenticated(request):
    return render(request, 'dashboard/home_authenticated.html')


def home_not_authenticated(request):
    return render(request, 'dashboard/home_not_authenticated.html')


class FoodDonareCreateView(SuccessMessageMixin, CreateView):
    model = FoodDonare
    template_name = 'dashboard/donare.html'
    fields = ["contact_number", "address", "food_details"]
    success_url = reverse_lazy("donare")
    success_message = "Information Saved Successfully."

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.save()
        return super(FoodDonareCreateView, self).form_valid(form)


class DonareDisplayView(ListView):
    model = FoodDonare
    template_name = "dashboard/donare_display.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        donare = FoodDonare.objects.filter(user=self.request.user)
        context = {"donare": donare}
        return context


class DonareDetailView(SuccessMessageMixin, DetailView):
    model = FoodDonare
    context_object_name = 'donare'
    template_name = "dashboard/donare_detail.html"

    def detail_donare(request, pk):
        donare = get_object_or_404(FoodDonare, id=pk)


class DonareUpdateView(SuccessMessageMixin, UpdateView):
    model = FoodDonare
    template_name = "dashboard/donare_update.html"
    fields = ["contact_number", "address", "food_details"]
    success_url = reverse_lazy("display_donare")
    success_message = "Information Updated successfully."

    def update_donare(request, pk):
        donare = get_object_or_404(FoodDonare, id=pk)


class DonareDeleteView(SuccessMessageMixin, DeleteView):
    model = FoodDonare
    template_name = "dashboard/donare_delete.html"
    success_messages = "Infromation Deleted Successfully."
    success_url = reverse_lazy("display_donare")

    def delete_donare(request, pk):
        donare = get_object_or_404(FoodDonare, id=pk)


def acceptor(request):
    return render(request,'dashboard/acceptor.html')


class SearchResultsView(ListView):
    model = FoodDonare
    template_name = "dashboard/acceptor.html"
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = FoodDonare.objects.filter(address__icontains=query)
        return object_list



class RequestView(CreateView):
    model = FoodAcceptor
    template_name = 'dashboard/request.html'
    fields = ["contact_number", "any_message"]
    success_url = reverse_lazy("request")
    success_message = "Request sent successfully."
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.save()
        createNotificationTo = (
            "Food request from {} on {}. ".format(
            self.request.user, date.today()
            )
        )
        notificationTo = Notification(
            user=self.request.user, notification=createNotificationTo
        )
        notificationTo.save()
        return HttpResponseRedirect(self.success_url)

    # context_object_name = 'donare'
    # template_name = "dashboard/donare_detail.html"

    # def detail(request, pk):
    #     donare = get_object_or_404(FoodDonare, id=pk)
    #     return super(RequestDetailView, request.donare)

#     def post(self,request):
#         noti_count = Notification.objects.filter(user_id=request.user.id).count()
#         form = FoodRequestForm(request.POST)
#         if request.method == "POST":
#             # form = FoodRequestForm(request.POST)
# #         if request.user.id == pk: 
#             contact_number = request.POST["contact_number"]
#             any_message = request.POST["any_message"]
#             if form.is_valid():
#                 form = FoodAcceptor(user=request.user, contact_number = contact_number, any_message= any_message )
#                 form.save()
#         form = FoodRequestForm()
#         return render(request, "dashboard/detail.html", {"form": form, "noti_count": noti_count})
    

# class RequestView(SuccessMessageMixin,FormView):
#     model = FoodAcceptor, FoodDonare
#     template_name = 'dashboard/request.html'
#     form_class = FoodRequestForm
#     success_url = reverse_lazy("home_authenticated")
#     success_message = "Request sent successfully."
    
#     # def get_queryset(self):
#     #     receiver = FoodDonare.objects.filter(user= self.donare.user)
#     #     print(receiver)
#     #     return super().get_queryset()
     

#     def form_valid(self, form):
#         user = self.request.user
        
#         form.instance.user = user
#         form.save()
#         createNotificationTo = (
#             "Food request from {} on {}. ".format(
#             self.request.user, date.today()
#             )
#         )
#         notificationTo = Notification(
#             user=self.request.user, notification=createNotificationTo
#         )
#         notificationTo.save()

#         return HttpResponseRedirect(self.success_url)
        


# @login_required
# def RequestView(request, pk):
#     # msg = ""
#     noti_count = Notification.objects.filter(user_id=request.user.id).count()
#     form = FoodRequestForm(request.POST)
#     if request.method == "POST":
#         if request.user.id == pk: 
#             contact_number = request.POST["contact_number"]
#             any_message = request.POST["any_message"]
#             receiver = request.POST.get["user"]
#         # user = get_object_or_404(User, username=user)
#         # print(user)
#             receiver = FoodDonare.objects.get(user = receiver)
#         # receiverUser = User.objects.get(username=receiver)
#             print(receiver)
#             sender = request.user
#             if form.is_valid():
#                 form = FoodAcceptor(user=request.user, contact_number = contact_number, any_message= any_message )
#                 form.save()
#         #     createNotificationFrom = (
#         #             "{}/- has been debited from your account {} on {}. ".format(
#         #                 amount, ProfileView.phonenum, date.today()
#         #             )
#         #         )
#         #         createNotificationTo = (
#         #             "{}/- has been credited to you account by {} on {}. ".format(
#         #                 amount, ProfileView.phonenum, date.today()
#         #             )
#         #         )
#         #         notificationFrom = Notification(
#         #             user=request.user, notification=createNotificationFrom
#         #         )
#         #         notificationTo = Notification(
#         #             user=customerTo.user, notification=createNotificationTo
#         #         )
#         #         notificationTo.save()
#         #         notificationFrom.save()
#         #         noti_count = noti_count + 1
#         #        
#     form = FoodRequestForm()
#     return render(
#         request,
#         "dashboard/request.html",
#         {"form": form, "noti_count": noti_count},
#     )



@login_required
def NotificationView(request):
    notifications = Notification.objects.filter(user=request.user)
    if request.method == "POST":
        notifications.delete()
    return render(
        request,
        "dashboard/see_notification.html",
        {"notifications": notifications, "noti_count": notifications.count()},
    )
