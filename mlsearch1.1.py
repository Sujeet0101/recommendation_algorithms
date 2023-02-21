```py
class HostelRecommendationView(generics.ListAPIView):
  serializer_class = HostelSerializer
  def get_queryset(self):
    queryset = Hostel.objects.all()

    #get search inputs
    hostel_name = self.request.query_params.get('hostel_name')
    district = self.request.query_params.get('district')
    place = self.request.query_params.get('place')
    hostel_type = self.request.query_params.get('hostel_type')
    single_seater = self.request.query_params.get('single_seater')
    two_seater = self.request.query_params.get('two_seater')
    three_seater = self.request.query_params.get('three_seater')
    four_seater = self.request.query_params.get('four_seater')
    wifi = self.request.query_params.get('wifi')
    closet = self.request.query_params.get('closet')
    hot_water = self.request.query_params.get('hot_water')
    laundry = self.request.query_params.get('laundry')
    parking = self.request.query_params.get('parking')
    cctv = self.request.query_params.get('cctv')
    fan = self.request.query_params.get('fan')
    balcony = self.request.query_params.get('balcony')

    #filter hostels based on search inputs
    if hostel_name:
        queryset = queryset.filter(hostel_name__icontains=hostel_name)
    if district:
        queryset = queryset.filter(district__icontains=district)
    if place:
        queryset = queryset.filter(place__icontains=place)
    if hostel_type:
        queryset = queryset.filter(hostel_type=hostel_type)
    if single_seater:
        queryset = queryset.filter(single_seater__lte=single_seater)
    if two_seater:
        queryset = queryset.filter(two_seater__lte=two_seater)
    if three_seater:
        queryset = queryset.filter(three_seater__lte=three_seater)
    if four_seater:
        queryset = queryset.filter(four_seater__lte=four_seater)
    if wifi:
        queryset = queryset.filter(wifi=True)
    if closet:
        queryset = queryset.filter(closet=True)
    if hot_water:
        queryset = queryset.filter(hot_water=True)
    if laundry:
        queryset = queryset.filter(laundry=True)
    if parking:
        queryset = queryset.filter(parking=True)
    if cctv:
        queryset = queryset.filter(cctv=True)
    if fan:
        queryset = queryset.filter(fan=True)
    if balcony:
        queryset = queryset.filter(balcony=True)

    #calculate cosine similarity between search inputs and hostel features
    input_vector = np.zeros((1, 14))
    input_vector[0][0] = 1 if wifi else 0
    input_vector[0][1] = 1 if closet else 0
    input_vector[0][2] = 1 if hot_water else 0
    input_vector[0][3] = 1 if laundry else 0
    input_vector[0][4] = 1 if parking else 0
    input_vector[0][5] = 1 if cctv else 0
    input_vector[0][6] = 1 if fan else 0
    input_vector[0][7] = 1 if balcony else 0
    input_vector[0][8] = single_seater if single_seater else 0
    input_vector[0][9] = two_seater if two_seater else 0
    input_vector[0][10] = three_seater if three_seater else 0
    input_vector[0][11] = four_seater if four_seater else

