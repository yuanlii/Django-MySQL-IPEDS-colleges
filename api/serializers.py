from colleges.models import Institution, AcademicDomain,GraduationRaceType, LibraryCollectionCategory, AcademicProgram
from rest_framework import response, serializers, status


class AcademicDomainSerializer(serializers.ModelSerializer):

	class Meta:
		model = AcademicDomain
		fields = ('academic_domain_id', 'cipcode', 'ciptitle')


class GraduationRaceTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = GraduationRaceType
		fields = ('graduation_race_category_id', 'race_category_name')


class LibraryCollectionCategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = LibraryCollectionCategory
		fields = ('collection_category_id', 'collection_category_name')


class AcademicProgramSerializer(serializers.ModelSerializer):
	institution_id = serializers.ReadOnlyField(source='institution.institution_id')
	academic_domain_id = serializers.ReadOnlyField(source='academic_domain.academic_domain_id')

	class Meta:
		model = AcademicProgram
		fields = ('institution_id', 'academic_domain_id')

#### add LibraryCollection
class LibraryCollectionHoldingSerializer(serializers.ModelSerializer):
	institution_id = serializers.ReadOnlyField(source='institution.institution_id')
	academic_domain_id = serializers.ReadOnlyField(source='academic_domain.academic_domain_id')

	class Meta:
		model = AcademicProgram
		fields = ('institution_id', 'academic_domain_id')


class InstitutionSerializer(serializers.ModelSerializer):
	institution_name = serializers.CharField(
		allow_blank=False,
		max_length=255
	)
	city_id = serializers.CharField(
		allow_blank=False
	)
	state_id = serializers.CharField(
		allow_blank=True
	)
	zip_code = serializers.CharField(
		allow_null=True
	)
	student_faculty_ratio = serializers.DecimalField(
		allow_null=True,
		max_digits=11,
		decimal_places=8)

	percent_admitted = serializers.DecimalField(
		allow_null=True,
		max_digits=10,
		decimal_places=8
	)

	class Meta:
		model = Institution
		fields = (
			'institution_id',
			'institution_name',
			'city_id',
			'state_id',
			'zip_code',
			'student_faculty_ratio',
			'percent_admitted'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		academic_domains = validated_data.pop('academic_program')
		institution = Institution.objects.create(**validated_data)

		if academic_domains is not None:
			for academic_domain in academic_domains:
				AcademicProgram.objects.create(
					institution_id=institution.institution_id,
					academic_domain_id=academic_domain.academic_domain_id
				)
		return academic_domain

	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		institution_id = instance.institution_id
		new_academic_domains = validated_data.pop('acadmic_program')

		instance.institution_name = validated_data.get(
			'institution_name',
			instance.institution_name
		)
		instance.city_id = validated_data.get(
			'city_id',
			instance.city_id
		)
		instance.state_name = validated_data.get(
			'state_id',
			instance.state_id
		)
		instance.zip_code = validated_data.get(
			'zip_code',
			instance.zip_code
		)
		instance.student_faculty_ratio = validated_data.get(
			'student_faculty_ratio',
			instance.student_faculty_ratio
		)
		instance.percent_admitted = validated_data.get(
			'percent_admitted',
			instance.percent_admitted
		)
		instance.save()

		# If any existing AcademicProgram are not in updated list, delete them
		new_ids = []
		old_ids = academic_program.objects \
			.values_list('academic_domain_id', flat=True) \
			.filter(institution_id__exact=institution_id)

		# Insert new unmatched AcademicProgram entries
		for academic_domain in new_academic_domains:
			new_id = academic_domain.academic_domain_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				academic_program.objects \
					.create(institution_id=institution_id, academic_domain_id=new_id)

		# Delete old unmatched AcademicProgram entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				AcademicProgram.objects \
					.filter(institution_id=institution_id, academic_domain_id=old_id) \
					.delete()

		return instance