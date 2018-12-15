

from django.shortcuts import render
from colleges.models import Institution, AcademicProgram
from api.serializers import InstitutionSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class InstitutionViewSet(viewsets.ModelViewSet):
	"""
	This ViewSet provides both 'list' and 'detail' views.
	"""
	queryset = Institution.objects.select_related('academic_domain').order_by('institution_name')
	serializer_class = InstitutionSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def delete(self, request, pk, format=None):
		site = self.get_object(pk)
		self.perform_destroy(self, site)

		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.delete()
