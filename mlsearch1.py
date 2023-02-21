from django.db import models
from django.contrib.postgres.search import SearchVector
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MinMaxScaler
from rest_framework import generics, filters
from django_filters import rest_framework as django_filters

class Hostel(models.Model):
    manager_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hostel')
    hostel_id = models.BigAutoField(primary_key=True)
    hostel_name = models.CharField(max_length=200, null=True, blank=True)
    type=(
        ('Boys', "Boys"),
        ('Girls', "Girls")
    )
    hostel_type = models.CharField(max_length=10, choices=type, null=True)
    pan_no = models.CharField(max_length=200, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    manager_name = models.CharField(max_length=100, null=True, blank=True)
    manager_contact = models.CharField(max_length=100, null=True, blank=True)
    # price
    single_seater = models.IntegerField(null=True, blank=True)
    two_seater = models.IntegerField(null=True, blank=True)
    three_seater = models.IntegerField(null=True, blank=True)
    four_seater = models.IntegerField(null=True, blank=True)
    admission_fee = models.IntegerField(null=True, blank=True)
    # ----
    description = models.TextField(max_length=1000, blank=True, null=True)
    # images
    image_1 = models.URLField(null=True, blank=True)
    image_2 = models.URLField(null=True, blank=True)
    image_3 = models.URLField(null=True, blank=True)
    # Facilities
    wifi = models.BooleanField(default=False)
    closet = models.BooleanField(default=False)
    hot_water = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    cctv = models.BooleanField(default=False)
    fan = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    # ----------------------------
    map_link = models.URLField(null=True, blank=True)

    # Define the vector field for cosine similarity
    vector = SearchVector('hostel_name') + SearchVector('district') + SearchVector('place') + \
        SearchVector('hostel_type') + SearchVector('description') + \
        SearchVector('manager_name') + SearchVector('manager_contact') + \
        SearchVector('wifi') + SearchVector('closet') + \
        SearchVector('hot_water') + SearchVector('laundry') + \
        SearchVector('parking') + SearchVector('cctv') + \
        SearchVector('fan') + SearchVector('balcony')

    def save(self, *args, **kwargs):
        # Convert the hostel attributes to a vector
        attributes = [
            self.hostel_name, self.district, self.place, self.hostel_type,
            self.description, self.manager_name, self.manager_contact,
            self.wifi, self.closet, self.hot_water, self.laundry,
            self.parking, self.cctv, self.fan, self.balcony
        ]
        vectorizer = CountVectorizer()
        scaler = MinMaxScaler()
        vector = vectorizer.fit_transform(attributes).toarray()
        vector = scaler.fit_transform(vector)
        self.vector = vector.tolist()[0]

        super().save(*args, **kwargs)

class HostelSearchAPIView(generics.ListAPIView):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    filter_backends = [filters.SearchFilter, django_filters
