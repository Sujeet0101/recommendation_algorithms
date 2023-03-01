if district and location:
    # Create input text string
    input_text = f"{district}, {location}"

    # Create hostels text string of all hostels
    hostels = Hostel.objects.filter(district=district, location=location)
    hostels_text = " ".join([f"{hostel.district}, {hostel.location}" for hostel in hostels])

    # Use the TfidfVectorizer from scikit-learn to create a vectorized representation of the input text and hostels text string
    vectorizer = TfidfVectorizer()
    input_vec = vectorizer.fit_transform([input_text])
    hostels_vec = vectorizer.transform([hostels_text])

    # Use the cosine similarity metric to calculate the similarity between the input hostel name and the hostels
    similarity = cosine_similarity(input_vec, hostels_vec)

    # Get the top 40 most similar hostels
    top_40 = np.argsort(similarity[0])[::-1][:40].tolist()

    # Get the top 40 hostel objects using the indices
    top_hostels = [hostels[i] for i in top_40]

    # Return the top 40 hostels as a JSON response
    serializer = HostelSerializer(top_hostels, many=True)
    return JsonResponse(serializer.data, safe=False)

else:
    return JsonResponse({"error": "Hostel district and location not provided."}, status=404)
