import geojson

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from api.models import Stop, Route, Pattern
from api.util import uniqify

class GeoJSONResponseMixin(object):
	def render_to_response(self, content):
		return HttpResponse(geojson.dumps(content),
							content_type='application/json')

class BaseAPIView(GeoJSONResponseMixin, View):
	params = ['lat', 'lng', 'radius_m']
	required_params = params

	def get(self, request, *args, **kwargs):
		# Parse query params.	
		for param in self.params:
			if param in request.GET:
				setattr(self, param, float(request.GET[param]))

		for param in self.required_params:
			if param not in request.GET:
				return HttpResponseBadRequest('Required parameters: ' + ', '.join(self.required_params))

		if hasattr(self, 'lng') and hasattr(self, 'lat'):	
			self.origin = Point(self.lng, self.lat)
	
		# Perform the API call.
		api_result = self.get_api_result(*args, **kwargs)
		
		# Return the result.
		return self.render_to_response(api_result)
	
class NearbyStopsView(BaseAPIView):
	def get_api_result(self, *args, **kwargs):
		stops = Stop.objects.filter(geom__distance_lte=(self.origin, 
													    D(m=self.radius_m)))
		return geojson.FeatureCollection([stop.feature for stop in stops])

class NearbyView(BaseAPIView):
	def get_api_result(self, *args, **kwargs):
		# Find all patterns with a stop close to this points, grouped by route.
		patterns = Pattern.objects.filter(patternstop__stop__geom__distance_lte=(self.origin,
																				 D(m=self.radius_m)))

		# Find the closest stop on each pattern.
		ordered_stops = Stop.objects.distance(self.origin).order_by('distance')
		stops = [ordered_stops.filter(patternstop__pattern=p)[0] for p in patterns]

		features = []
		features.extend([stop.feature for stop in stops])
		features.extend([pattern.feature for pattern in patterns])
		return geojson.FeatureCollection(features)
