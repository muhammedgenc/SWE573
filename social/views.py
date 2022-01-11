from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from .models import Service, UserProfile, ServiceApplication, Event, EventApplication
from .forms import ServiceForm, ServiceApplicationForm, EventForm, EventApplicationForm
from django.db import models
from django.utils import timezone
from django.contrib import messages

class ServiceCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ServiceForm()
        
        context = {
            'form': form,
        }

        return render(request, 'social/create_service.html', context)

    def post(self, request, *args, **kwargs):
        form = ServiceForm(request.POST, request.FILES)
        profile = UserProfile.objects.get(pk=request.user)

        if form.is_valid():
            totalcredit = profile.credit_hours + profile.reserved_credits
            new_service = form.save(commit=False)
            if totalcredit + new_service.duration <= 15:
                new_service.author = request.user
                profile.reserved_credits = profile.reserved_credits + new_service.duration
                profile.save()
                new_service.save()
                
                messages.success(request,'Your Service is created')
            else:
                messages.warning(request, 'Your total credits cannot be over 15.')
        else:
            messages.warning(request, 'Form is not valid, please check the values')

       
        myservices = Service.objects.filter(author=request.user).order_by('-created_on')
        return render(request, 'social/service_list.html', {'service_list':myservices})


class ServiceListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        services = Service.objects.all().order_by('-created_on')
        form = ServiceForm()

        context = {
            'service_list': services,
            'form': form,
        }

        return render(request, 'social/service_list.html', context)

    def post(self, request, *args, **kwargs):
        services = Service.objects.all().order_by('-created_on')
        form = ServiceForm(request.POST)

        if form.is_valid():
            new_service = form.save(commit=False)
            new_service.author = request.user
            new_service.save()

        context = {
            'service_list': services,
            'form': form,
        }

        return render(request, 'social/service_list.html', context)

class ServiceDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        service = Service.objects.get(pk=pk)
        form = ServiceApplicationForm()
        applications = ServiceApplication.objects.filter(applied_service=pk).order_by('-application_date')

        context = {
            'service': service,
            'form': form,
            'applications': applications
         }

        return render(request, 'social/service_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        service = Service.objects.get(pk=pk)
        form = ServiceApplicationForm(request.POST)
        applications = ServiceApplication.objects.filter(applied_service=pk).order_by('-application_date')
        profile = UserProfile.objects.get(pk=request.user)
        if len(applications) == 0:
            is_applied = False

        for application in applications:
            if application.applicant == request.user:
                is_applied = True
                break
            else:
                is_applied = False
        
        if form.is_valid():
            if is_applied == False:
                new_application = form.save(commit=False)
                new_application.applicant = request.user
                new_application.applied_service = service
                new_application.is_approved = False
                new_application.save()
    
        applications = ServiceApplication.objects.filter(applied_service=pk).order_by('-application_date')

        context = {
            'service': service,
            'form': form,
            'applications': applications,
        }

        return render(request, 'social/service_detail.html', context)


class ServiceEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    fields = ['picture', 'name', 'description', 'duration', 'category', 'service_date', 'service_time', 'capacity']
    template_name = 'social/service_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('service-detail', kwargs={'pk':pk})

    def test_func(self):
        service = self.get_object()
        return self.request.user == service.author

class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service
    template_name = 'social/service_delete.html'

    def reserved_credits_update(self, request, *args, **kwargs):
        service = self.get_object()
        profile = UserProfile.objects.get(pk=self.request.user)
        profile.reserved_credits = profile.reserved_credits - service.duration
        profile.save()
        
    success_url = reverse_lazy('service-list')

    def test_func(self):
        service = self.get_object()
        return self.request.user == service.author

class ServiceApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ServiceApplication
    template_name = 'social/application_delete.html'

    def get_success_url(self):
        pk = self.kwargs['service_pk']
        return reverse_lazy('service-detail', kwargs={'pk': pk})
    
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.applicant


class ServiceApplicationApproveView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ServiceApplication
    fields = ['is_approved']
    template_name = 'social/application_approve.html'

    def get_success_url(self):
        pk = self.kwargs['service_pk']
        return reverse_lazy('service-detail', kwargs={'pk': pk})
    
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.applied_service.author

class EventCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = EventForm()
        
        context = {
            'form': form,
        }

        return render(request, 'social/create_event.html', context)

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST, request.FILES)
        profile = UserProfile.objects.get(pk=request.user)

        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.author = request.user
            new_event.save()
                
            messages.success(request,'Your Event is created')
        else:
            messages.warning(request, 'Form is not valid, please check the values')

       
        myevents = Event.objects.filter(author=request.user).order_by('-created_on')
        return render(request, 'social/event_list.html', {'event_list':myevents})

class EventListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        events = Event.objects.all().order_by('-created_on')
        form = EventForm()

        context = {
            'event_list': events,
            'form': form,
        }

        return render(request, 'social/event_list.html', context)

    def post(self, request, *args, **kwargs):
        events = Event.objects.all().order_by('-created_on')
        form = EventForm(request.POST)

        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.author = request.user
            new_event.save()

        context = {
            'event_list': events,
            'form': form,
        }

        return render(request, 'social/event_list.html', context)

class EventDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        event = Event.objects.get(pk=pk)
        form = EventApplicationForm()
        eventapplications = EventApplication.objects.filter(applied_event=pk).order_by('-application_date')

        context = {
            'event': event,
            'form': form,
            'eventapplications': eventapplications
        }

        return render(request, 'social/event_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        event = Event.objects.get(pk=pk)
        form = EventApplicationForm(request.POST)
        eventapplications = EventApplication.objects.filter(applied_event=pk).order_by('-application_date')
        profile = UserProfile.objects.get(pk=request.user)
        if len(eventapplications)==0:
            is_applied = False

        for eventapplication in eventapplications:
            if eventapplication.applicant == request.user:
                is_applied = True
                break
            else:
                is_applied = False
        
        if form.is_valid():
            if is_applied == False:
                new_eventapplication = form.save(commit=False)
                new_eventapplication.applicant = request.user
                new_eventapplication.applied_event = event
                new_eventapplication.is_approved = False
                new_eventapplication.save()
    
        eventapplications = EventApplication.objects.filter(applied_event=pk).order_by('-application_date')

        context = {
            'event': event,
            'form': form,
            'eventapplications': eventapplications,
        }

        return render(request, 'social/event_detail.html', context)

class EventEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['picture', 'name', 'description', 'duration', 'category', 'event_date', 'event_time', 'capacity']
    template_name = 'social/event_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('event-detail', kwargs={'pk':pk})

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.author

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'social/event_delete.html'

    success_url = reverse_lazy('event-list')

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.author

class EventApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EventApplication
    template_name = 'social/eventapplication_delete.html'

    def get_success_url(self):
        pk = self.kwargs['event_pk']
        return reverse_lazy('event-detail', kwargs={'pk': pk})
    
    def test_func(self):
        eventapplication = self.get_object()
        return self.request.user == eventapplication.applicant



class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user

        context = {
            'user': user,
            'profile': profile,
        }

        return render(request, 'social/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user