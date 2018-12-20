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
from django.shortcuts import redirect


def index(request):
   return HttpResponse("Hello, world. You're at the IPEDS colleges index.")

class HomePageView(generic.TemplateView):
	# template_name = 'colleges/index.html'
	template_name = 'colleges/about.html'


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


# fix this ###############
@method_decorator(login_required, name='dispatch')
class GraduationRaceTypeListView(generic.ListView):
	model = 'GraduationRaceType'
	context_object_name = 'race_types'
	template_name = 'colleges/race_type.html'
	paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return GraduationRaceType.objects.all().order_by('race_category_name')


@method_decorator(login_required, name='dispatch')
class AcademicDomainListView(generic.ListView):
	model = 'AcademicDomain'
	context_object_name = 'academic_domains'
	template_name = 'colleges/academic_domain.html'
	paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return AcademicDomain.objects.all().order_by('ciptitle')


@method_decorator(login_required, name='dispatch')
class LibraryCollectionCategoryListView(generic.ListView):
	model = 'LibraryCollectionCategory'
	context_object_name = 'library_collection_categories'
	template_name = 'colleges/library_collection_category.html'
	paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return LibraryCollectionCategory.objects.all().order_by('collection_category_name')
	


@method_decorator(login_required, name='dispatch')
class InstitutionCreateView(generic.View):
	model = Institution
	form_class = InstitutionForm
	success_message = "Institution created successfully"
	template_name = 'colleges/institution_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('colleges/institution_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = InstitutionForm(request.POST)
		print (form.errors)

		if form.is_valid():	
			institution = form.save(commit=False)
			institution.save()
			# return redirect(institution)
			return HttpResponseRedirect(institution.get_absolute_url())
		return render(request, 'colleges/institution_new.html', {'form': form})

	def get(self, request):
		form = InstitutionForm()
		return render(request, 'colleges/institution_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class InstitutionUpdateView(generic.UpdateView):
	model = Institution
	form_class = InstitutionForm
	context_object_name = 'institution'
	success_message = "Institution updated successfully"
	template_name = 'colleges/institution_update.html'
	# success_url = reverse_lazy('institution')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		institution = form.save(commit=False)
		# institution.updated_by = self.request.user
		# institution.date_updated = timezone.now()
		institution.save()

		# academic_domain
		old_ids = AcademicProgram.objects\
			.values_list('academic_domain_id', flat=True)\
			.filter(instituion_id=institution.institution_id)

		new_domains = form.cleaned_data['academic_domains']
		new_ids = []

		for domain in new_domains:
			new_id = academic_domain.academic_domain_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				AcademicProgram.objects \
					.create(institution=institution, academic_domain=domain)

		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				AcademicProgram.objects \
					.filter(institution_id=institution.institution_id, academic_domain_id=old_id) \
					.delete()
		

		# Graduation by race
		new_ids = []

		old_ids = GraduationByRace.objects\
			.values_list('graduation_race_category_id', flat=True)\
			.filter(instituion_id=institution.institution_id)

		new_race_types = form.cleaned_data['graduation_race_type']
		

		for race_type in new_race_types:
			new_id = graduation_race_type.graduation_race_category_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				GraduationByRace.objects \
					.create(institution=institution, graduation_race_type=race_type)

		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				GraduationByRace.objects \
					.filter(institution_id=institution.institution_id, graduation_race_category_id=old_id) \
					.delete()

		
		# LibraryCollectionHolding
		old_ids = LibraryCollectionHolding.objects\
			.values_list('collection_category_id', flat=True)\
			.filter(instituion_id=institution.institution_id)

		new_collection_types = form.cleaned_data['library_collection_category']
		new_ids = []

		for collection_type in new_collection_types:
			new_id = library_collection_category.collection_category_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				LibraryCollectionHolding.objects \
					.create(institution=institution, library_collection_category=collection_type)

		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				LibraryCollectionHolding.objects \
					.filter(institution_id=institution.institution_id, LibraryCollectionHolding_id=old_id) \
					.delete()

		# return HttpResponseRedirect(institution.get_absolute_url())
		return redirect('colleges/institution_detail', pk=institution.pk)


@method_decorator(login_required, name='dispatch')
class InstitutionDeleteView(generic.DeleteView):
	model = Institution
	success_message = "Institution deleted successfully"
	success_url = reverse_lazy('institution')
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


@method_decorator(login_required, name='dispatch')
class InstitutionFilterView(FilterView):
	filterset_class = InstitutionFilter
	context_object_name = 'filters'
	template_name = 'colleges/institution_filter.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

