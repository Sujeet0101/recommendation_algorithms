@api_view(['GET'])
def recommend_by_name(request):
    hostel_name = request.GET.get("hostel_name", None)
    if hostel_name:
        hostel = Hostel.objects.filter(hostel_name = hostel_name)

        #create a user's input_hostel_tags list which contains values of district and location column  
        if hostel.exists():
            hostel = hostel[0]
            input_hostel_tags = hostel.hostel_name + "," + hostel.district + "," + hostel.location
        else:
            input_hostel_tags = ""

       # create hostel_tags list of all hostels
        hostels = Hostel.objects.all()   
        hostels_tags = [hostel.hostel_name + "," + hostel.district + "," + hostel.location for hostel in hostels]

       # Use the TfidfVectorizer from scikit-learn to create a vectorized representation of the input text and hostels list
        vectorizer = TfidfVectorizer()
        input_vec = vectorizer.fit_transform([input_hostel_tags])
        hostels_vec = vectorizer.transform(hostels_tags)

       # Use the cosine similarity metric to calculate the similarity between the input hostel name and the hostels
        similarity = cosine_similarity(input_vec, hostels_vec)

       # Get the top 10 most similar hostels
        top_10 = np.argsort(similarity[0])[::-1][:10].tolist()

       # Get the top 10 hostel objects using the indices
        top_hostels = [hostels[i] for i in top_10]

       # Return the top 5 hostels as a JSON response
        serializer = HostelSerializer(top_hostels, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    else:
        return JsonResponse({"error": "Hostel name not provided."}, status=400)
