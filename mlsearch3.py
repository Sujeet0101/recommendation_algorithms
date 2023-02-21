from rest_framework import generics
from django.db.models import Q
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from .models import Hostel


class HostelRecommendationView(generics.ListAPIView):
    serializer_class = HostelSerializer

    def get_queryset(self):
        queryset = Hostel.objects.all()
        search_params = self.request.query_params.dict()

        # Filter queryset based on user's search inputs
        if search_params:
            queryset = queryset.filter(Q(hostel_name__icontains=search_params.get('hostel_name', '')) &
                                       Q(district__icontains=search_params.get('district', '')) &
                                       Q(place__icontains=search_params.get('place', '')) &
                                       Q(hostel_type=search_params.get('hostel_type', '')) &
                                       Q(single_seater__lte=search_params.get('single_seater', 10)) &
                                       Q(two_seater__lte=search_params.get('two_seater', 10)) &
                                       Q(three_seater__lte=search_params.get('three_seater', 10)) &
                                       Q(four_seater__lte=search_params.get('four_seater', 10)) &
                                       Q(wifi=search_params.get('wifi', False)) &
                                       Q(closet=search_params.get('closet', False)) &
                                       Q(hot_water=search_params.get('hot_water', False)) &
                                       Q(laundry=search_params.get('laundry', False)) &
                                       Q(parking=search_params.get('parking', False)) &
                                       Q(cctv=search_params.get('cctv', False)) &
                                       Q(fan=search_params.get('fan', False)) &
                                       Q(balcony=search_params.get('balcony', False)))

        # Use cosine similarity to get top 10 recommended hostels
        hostel_descriptions = list(queryset.values_list('description', flat=True))
        vectorizer = CountVectorizer().fit_transform(hostel_descriptions)
        cosine_similarities = cosine_similarity(vectorizer)

        if cosine_similarities.shape[0] > 0:
            similar_indices = cosine_similarities.argsort()[0][-11:-1]
            recommended_hostels = queryset.filter(id__in=similar_indices).order_by('-id')
        else:
            recommended_hostels = queryset.none()

        return recommended_hostels
