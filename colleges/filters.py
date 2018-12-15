import django_filters
from colleges.models import Institution, City, State

class InstitutionFilter(django_filters.FilterSet):
	institution_name = django_filters.CharFilter(
		field_name='institution_name',
		label='Institution Name',
		lookup_expr='icontains'
	)

	# city = django_filters.ModelChoiceFilter(
	# 	field_name = 'city',
    #     label = 'City',
    #     queryset = City.objects.all().order_by('city_name').distinct(),
	# 	lookup_expr='exact')
	
	# state = django_filters.ModelChoiceFilter(
	# 	field_name = 'state',
    #     label = 'State',
    #     queryset = State.objects.all().order_by('state_name').distinct(),
	# 	lookup_expr='exact')


	class Meta:
		model = Institution
		fields = ['institution_name','city','state']