# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.urls import reverse

class AcademicDomain(models.Model):
    academic_domain_id = models.AutoField(primary_key=True)
    cipcode = models.IntegerField()
    ciptitle = models.CharField(db_column='CipTitle', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'academic_domain'
        ordering = ['cipcode']
        verbose_name = 'IPEDS Academic Program Domain'
        verbose_name_plural = 'IPEDS Academic Program Domains'

    def __str__(self):
        return str(self.cipcode)


class GraduationRaceType(models.Model):
    graduation_race_category_id = models.AutoField(primary_key=True)
    race_category_name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'graduation_race_type'
        ordering = ['race_category_name']
        verbose_name = 'IPEDS Institution Graduation Race Type'
        verbose_name_plural = 'IPEDS Institution Graduation Race Types'

    def __str__(self):
        return self.race_category_name


class LibraryCollectionCategory(models.Model):
    collection_category_id = models.AutoField(primary_key=True)
    collection_category_name = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'library_collection_category'
        ordering = ['collection_category_name']
        verbose_name = 'IPEDS Institution Library Collection Category'
        verbose_name_plural = 'IPEDS Institution Library Collection Categories'
    
    def __str__(self):
        return self.collection_category_name


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'city'
        ordering = ['city_name']
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.city_name


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'state'
        ordering = ['state_name']
        verbose_name = 'state'
        verbose_name_plural = 'states'

    def __str__(self):
        return self.state_name


# add many-to-many relationship inside
class Institution(models.Model):
    institution_id = models.AutoField(primary_key=True)
    unitid = models.IntegerField(unique=True, null=True)
    institution_name = models.CharField(max_length=255)
    survey_year = models.CharField(max_length=4)
    zip_code = models.CharField(max_length=255, blank=True, null=True)

    student_faculty_ratio = models.IntegerField()
    # student_faculty_ratio = models.DecimalField(max_digits=10, decimal_places=0)
    percent_admitted = models.IntegerField()
    # percent_admitted = models.DecimalField(max_digits=10, decimal_places=0)

    city = models.ForeignKey(City, on_delete=models.PROTECT)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    academic_domain = models.ManyToManyField(
        AcademicDomain,
        through='AcademicProgram',
        blank=True,
        related_name='institution_domains'
    )
    graduation_race_type = models.ManyToManyField(
        GraduationRaceType,
        through='GraduationByRace',
        blank=True,
        related_name='institution_races'
    )
    library_collection_category = models.ManyToManyField(
        LibraryCollectionCategory,
        through='LibraryCollectionHolding',
        blank=True,
        related_name='institution_libraries'
    )

    class Meta:
        managed = False
        db_table = 'institution'
        ordering = ['institution_name']
        verbose_name = 'IPEDS Institution'
        verbose_name_plural = 'IPEDS Institutions'

    def __str__(self):
        return self.institution_name

    def get_absolute_url(self):
        return reverse('institution_detail', kwargs={'pk': self.pk})
    

    # add new method
    @property
    def academic_domain_names(self):
        academic_domains = self.academic_domain.objects.all().order_by('ciptitle')

        names = []
        for academic_domain in academic_domains:
            name = academic_domain.ciptitle
            if name is None:
                continue
            cipcode = academic_domain.cipcode

            name_and_code = ''.join([academic_domain, ' (', cipcode, ')'])
            if name_and_code not in names:
                names.append(name_and_code)

        return ', '.join(names)
    

    @property
    def graduation_race_type_names(self): 
        graduation_race_types = self.graduation_race_type.objects.all().order_by('race_category_name')

        names = []
        for graduation_race_type in graduation_race_types:
            name = graduation_race_type.graduation_race_type_name
            if name is None:
                continue

            if name not in names:
                names.append(name)

        return ', '.join(names)

    
    @property
    def library_collection_category_names(self):  
        library_collection_categories = self.library_collection_category.objects.all().order_by('collection_category_name')

        names = []
        for library_collection_category in library_collection_categories:
            name = library_collection_category.collection_category_name
            if name is None:
                continue

            if name not in names:
                names.append(name)

        return ', '.join(names)


class AcademicProgram(models.Model):
    academic_program_id = models.AutoField(primary_key=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    academic_domain = models.ForeignKey(AcademicDomain, on_delete=models.CASCADE)
    number_of_program_offered = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'academic_program'
        ordering = ['institution_id','academic_domain_id']
        verbose_name = 'IPEDS Academic Program Offered by Domains'
        verbose_name_plural = 'IPEDS Academic Programs Offered by Domains'


class GraduationByRace(models.Model):
    graduation_by_race_id = models.AutoField(primary_key=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    graduation_race_category = models.ForeignKey(GraduationRaceType, on_delete=models.CASCADE)
    number_of_graduation = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'graduation_by_race'
        ordering = ['institution_id','graduation_race_category_id']
        # ordering = ['institution_id','graduation_race_type__graduation_race_category_id']
        verbose_name = 'IPEDS Institution Graduation by Race'
        verbose_name_plural = 'IPEDS Institution Graduations by Race'


class LibraryCollectionHolding(models.Model):
    library_collection_holding_id = models.AutoField(primary_key=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    collection_category = models.ForeignKey(LibraryCollectionCategory, on_delete=models.CASCADE)
    number_of_total_collection = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'library_collection_holding'
        verbose_name = 'IPEDS Institution Library Collection Holding'
        verbose_name_plural = 'IPEDS Institution Library Collection Holdings'


class PeerComparison(models.Model):
    peer_comparison_id = models.AutoField(primary_key=True)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, related_name='institution_set')
    comparison_institution = models.ForeignKey(Institution, on_delete=models.PROTECT, related_name='comparison_institution_set')

    class Meta:
        managed = False
        db_table = 'peer_comparison'
        verbose_name = 'IPEDS Institution Peer Comparison'
        verbose_name_plural = 'IPEDS Institution Peer Comparisons'
