from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Institution

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse,reverse_lazy
from colleges.forms import InstitutionForm
from django.http import HttpResponseRedirect
from .filters import InstitutionFilter
from django_filters.views import FilterView


# Create your views here.
def index(request):
   return HttpResponse("Hello, world. You're at the IPEDS colleges index.")

class HomePageView(generic.TemplateView):
	template_name = 'colleges/index.html'


class AboutPageView(generic.TemplateView):
	template_name = 'colleges/about.html'


class InstitutionListView(generic.ListView):
	model = Institution
	context_object_name = 'institutions'
	template_name = 'colleges/institution.html'
	paginate_by = 50

	def get_queryset(self):
		return Institution.objects.all().order_by('institution_name')
		

class InstitutionDetailView(generic.DetailView):
	model = Institution
	context_object_name = 'institution'
	template_name = 'colleges/institution_detail.html'


# @method_decorator(login_required, name='dispatch')
class InstitutionCreateView(generic.View):
	model = Institution
	form_class = InstitutionForm
	success_message = "Institution created successfully"
	template_name = 'colleges/institution_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = InstitutionForm(request.POST)
		if form.is_valid():
			institution = form.save(commit=False)
			institution.save()
			# for city in form.cleaned_data['city']:
			# 	HeritageSiteJurisdiction.objects.create(heritage_site=site, country_area=country)
			# return redirect(site) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'colleges/institution_new.html', {'form': form})

	def get(self, request):
		form = InstitutionForm()
		return render(request, 'colleges/institution_new.html', {'form': form})


# @method_decorator(login_required, name='dispatch')
class InstitutionUpdateView(generic.UpdateView):
	model = Institution
	form_class = InstitutionForm
	context_object_name = 'institution'
	success_message = "Institution updated successfully"
	template_name = 'colleges/institution_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		institution = form.save(commit=False)
		institution.updated_by = self.request.user
		institution.date_updated = timezone.now()
		institution.save()

		# Current country_area_id values linked to site
		# old_ids = HeritageSiteJurisdiction.objects\
		# 	.values_list('country_area_id', flat=True)\
		# 	.filter(heritage_site_id=site.heritage_site_id)

		# New countries list
		# new_countries = form.cleaned_data['country_area']

		# TODO can these loops be refactored?

		# New ids
		# new_ids = []

		# Insert new unmatched country entries
		# for country in new_countries:
		# 	new_id = country.country_area_id
		# 	new_ids.append(new_id)
		# 	if new_id in old_ids:
		# 		continue
		# 	else:
		# 		HeritageSiteJurisdiction.objects \
		# 			.create(heritage_site=site, country_area=country)

		# Delete old unmatched country entries
		# for old_id in old_ids:
		# 	if old_id in new_ids:
		# 		continue
		# 	else:
		# 		HeritageSiteJurisdiction.objects \
		# 			.filter(heritage_site_id=site.heritage_site_id, country_area_id=old_id) \
		# 			.delete()

		# return HttpResponseRedirect(site.get_absolute_url())
		# return redirect('heritagesites/site_detail', pk=site.pk)


# @method_decorator(login_required, name='dispatch')
class InstitutionDeleteView(generic.DeleteView):
	model = Institution
	success_message = "Institution deleted successfully"
	success_url = reverse_lazy('institutions')
	context_object_name = 'institution'
	template_name = 'colleges/institution_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete HeritageSiteJurisdiction entries
		# HeritageSiteJurisdiction.objects \
		# 	.filter(heritage_site_id=self.object.institution_id) \
		# 	.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())


# @method_decorator(login_required, name='dispatch')
class InstitutionFilterView(FilterView):
	filterset_class = InstitutionFilter
	context_object_name = 'filters'
	template_name = 'colleges/institution_filter.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

