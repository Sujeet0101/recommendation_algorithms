from django.db.models import Q
from rest_framework import generics
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from .models import Hostel


class HostelRecommendationView(generics.ListAPIView):
    serializer_class = HostelSerializer

    def get_queryset(self):
        hostel_name = self.request.GET.get('hostel_name', '')
        district = self.request.GET.get('district', '')
        place = self.request.GET.get('place', '')
        hostel_type = self.request.GET.get('hostel_type', '')
        single_seater = self.request.GET.get('single_seater', '')
        two_seater = self.request.GET.get('two_seater', '')
        three_seater = self.request.GET.get('three_seater', '')
        four_seater = self.request.GET.get('four_seater', '')
        wifi = self.request.GET.get('wifi', '')
        closet = self.request.GET.get('closet', '')
        hot_water = self.request.GET.get('hot_water', '')
        laundry = self.request.GET.get('laundry', '')
        parking = self.request.GET.get('parking', '')
        cctv = self.request.GET.get('cctv', '')
        fan = self.request.GET.get('fan', '')
        balcony = self.request.GET.get('balcony', '')

        # Filter hostels by search parameters
        qs = Hostel.objects.all()
        if hostel_name:
            qs = qs.filter(hostel_name__icontains=hostel_name)
        if district:
            qs = qs.filter(district__icontains=district)
        if place:
            qs = qs.filter(place__icontains=place)
        if hostel_type:
            qs = qs.filter(hostel_type=hostel_type)
        if single_seater:
            qs = qs.filter(single_seater__lte=single_seater)
        if two_seater:
            qs = qs.filter(two_seater__lte=two_seater)
        if three_seater:
            qs = qs.filter(three_seater__lte=three_seater)
        if four_seater:
            qs = qs.filter(four_seater__lte=four_seater)
        if wifi:
            qs = qs.filter(wifi=True)
        if closet:
            qs = qs.filter(closet=True)
        if hot_water:
            qs = qs.filter(hot_water=True)
        if laundry:
            qs = qs.filter(laundry=True)
        if parking:
            qs = qs.filter(parking=True)
        if cctv:
            qs = qs.filter(cctv=True)
        if fan:
            qs = qs.filter(fan=True)
        if balcony:
            qs = qs.filter(balcony=True)

        # Get hostel descriptions
        descriptions = qs.values_list('description', flat=True)
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions)
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Get top 10 recommended hostels
        hostel_indices = pd.Series(qs.index, index=qs['hostel_name'])
        recommended_hostels = []
        if len(descriptions) > 1:
            idx = hostel_indices[hostel_name]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]
            hostel_indices = [i[0] for i in sim_scores]
            recommended_hostels = qs.filter(id__in=hostel_indices)

        return recommended_hostels
