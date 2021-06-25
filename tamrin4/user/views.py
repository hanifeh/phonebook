from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework import generics, viewsets
from rest_framework.response import Response

from user import forms, models
from django.views.decorators.csrf import csrf_exempt
from . import serializers
# Create your views here.
from user.forms import UserForm, EditForm


@method_decorator(csrf_exempt, name='dispatch')
class CreateUser(LoginRequiredMixin, CreateView):
    model = models.MyUser
    form_class = UserForm

    def get_form_kwargs(self):
        kw = super(CreateUser, self).get_form_kwargs()
        kw.update({'user': self.request.user})
        return kw

    def form_invalid(self, form):
        return JsonResponse({'status': "error"})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        if 'action' not in self.request.session.keys():
            self.request.session['action'] = []

        self.request.session['action'] += [f'add contact : {self.object.phone_number} .']
        return JsonResponse({'status': "ok"})


# @csrf_exempt
# @login_required
# def search(request):
#     if request.method == 'POST':
#         searched = request.POST.get('searched', None)
#         mode = request.POST.get('mode', None)
#         if mode == '1':
#             obj = models.MyUser.objects.filter(phone_number__contains=searched, user=request.user)
#         elif mode == '2':
#             obj = models.MyUser.objects.filter(phone_number=searched, user=request.user)
#         elif mode == '3':
#             obj = models.MyUser.objects.filter(phone_number__startswith=searched, user=request.user)
#         elif mode == '4':
#             obj = models.MyUser.objects.filter(phone_number__endswith=searched, user=request.user)
#         else:
#             return JsonResponse({'result': "error"})
#         if obj:
#             return JsonResponse({
#                 'results': list(obj.values())
#             })
#         else:
#             return JsonResponse({'result': "phone number not found !"})
#     else:
#         return render(request, 'search.html', {})


@method_decorator(csrf_exempt, name='dispatch')
class Search(LoginRequiredMixin, ListView):
    model = models.MyUser
    template_name = 'search.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        searched = request.POST.get('searched', None)
        mode = request.POST.get('mode', None)
        if mode == '1':
            obj = models.MyUser.objects.filter(phone_number__contains=searched, user=request.user)
        elif mode == '2':
            obj = models.MyUser.objects.filter(phone_number=searched, user=request.user)
        elif mode == '3':
            obj = models.MyUser.objects.filter(phone_number__startswith=searched, user=request.user)
        elif mode == '4':
            obj = models.MyUser.objects.filter(phone_number__endswith=searched, user=request.user)
        else:
            return JsonResponse({'result': "error"})
        if obj:
            return JsonResponse({
                'results': list(obj.values()),
                'count': obj.count(),
            })
        else:
            return JsonResponse({'result': "phone number not found !"})


@method_decorator(csrf_exempt, name='dispatch')
class NewSearch(LoginRequiredMixin, ListView):
    model = models.MyUser
    template_name = 'newsearch.html'
    paginate_by = 5

    def get_queryset(self):
        searched = self.request.GET.get('searched', None)
        mode = self.request.GET.get('mode', None)
        if mode == '1':
            obj = models.MyUser.objects.filter(phone_number__contains=searched, user=self.request.user)
        elif mode == '2':
            obj = models.MyUser.objects.filter(phone_number=searched, user=self.request.user)
        elif mode == '3':
            obj = models.MyUser.objects.filter(phone_number__startswith=searched, user=self.request.user)
        elif mode == '4':
            obj = models.MyUser.objects.filter(phone_number__endswith=searched, user=self.request.user)
        else:
            obj = models.MyUser.objects.filter(user=self.request.user)
        if mode:
            if 'action' not in self.request.session.keys():
                self.request.session['action'] = []

            self.request.session['action'] += [f'search : {searched} .']
        return obj


@method_decorator(csrf_exempt, name='dispatch')
class PhoneBook(LoginRequiredMixin, ListView):
    model = models.MyUser
    template_name = 'phonebook.html'
    paginate_by = 5

    def get_queryset(self):
        qs = models.MyUser.objects.filter(user=self.request.user)
        return qs

class EditNumber(LoginRequiredMixin, UpdateView):
    model = models.MyUser
    template_name = 'editnumber.html'
    form_class = EditForm

    success_url = '/newsearch/'

    def get_form_kwargs(self):
        kw = super(EditNumber, self).get_form_kwargs()
        kw.update({'user': self.request.user})
        return kw

    def get_queryset(self):
        number = models.MyUser.objects.filter(pk=self.kwargs['pk'], user=self.request.user)
        if number:
            return number
        else:
            raise Http404("No MyModel matches the given query.")

    def form_valid(self, form):
        if 'action' not in self.request.session.keys():
            self.request.session['action'] = []
        self.request.session['action'] += [f'edit contact : {self.object.phone_number} .']
        super(EditNumber, self).form_valid(form)
        return redirect('/newsearch')


@method_decorator(csrf_exempt, name='dispatch')
class ActionView(LoginRequiredMixin, ListView):
    template_name = 'action.html'

    def get_queryset(self):
        if 'action' in self.request.session.keys():
            qs = self.request.session['action']
            if len(qs) > 5:
                qs = qs[-5:]
            return qs
        else:
            return []


class PhoneListAPI(viewsets.ModelViewSet):
    serializer_class = serializers.PhoneNumberSerializer
    queryset = models.MyUser.objects.all()
    filter_fields = (
        'first_name',
        'last_name',
        'phone_number',
    )

    def get_queryset(self):
        number = models.MyUser.objects.filter(user=self.request.user)
        return number

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
