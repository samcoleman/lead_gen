r = {'business_status': 'OPERATIONAL', 'formatted_address': '509 Abbey Wood Rd, Abbey Wood, London SE2 9HA', 'geometry': {'location': {'lat': 51.48990329999999, 'lng': 0.1217835}, 'viewport': {'northeast': {'lat': 51.49119417989272, 'lng': 0.1231277798927222}, 'southwest': {'lat': 51.48849452010728, 'lng': 0.1204281201072778}}}, 'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png', 'name': 'Glow Beauty', 'opening_hours': {'open_now': False}, 'photos': [{'height': 2448, 'html_attributions': ['<a href=""https://maps.google.com/maps/contrib/107326250885666612670"">Peri Ahmet</a>'], 'photo_reference': 'ATtYBwKbdVZ2CiinA62bi2ItmjeItBfab00Kf1_JtPBApwbv6eBU8kHQTqYUn-eBd4qfXkAIcKvdTvZRjf8qRr1l6F5dabSBUd2LW6lCwJqTh89lKrVdF5osUcvt5T4TUlmY_YZl9sjCiSNWpOLZpEfiFr_BgxY4jL0wD2HeYSgeN9wyoTUo', 'width': 3264}], 'place_id': 'ChIJA-M8FRSv2EcR3sz-AqhrDVI', 'plus_code': {'compound_code': 'F4QC+XP London', 'global_code': '9F32F4QC+XP'}, 'rating': 4.8, 'reference': 'ChIJA-M8FRSv2EcR3sz-AqhrDVI', 'types': ['beauty_salon', 'point_of_interest', 'establishment'], 'user_ratings_total': 24}

#print(r['next_page_token'])
#print(r["status"])

status = r["business_status"]
form_add = r["formatted_address"]
place_id = r["place_id"]
name = r["name"]
plus_code = r["plus_code"]
rating = r["rating"]
user_rating_total = r["user_ratings_total"]
ref = r["reference"]
print(typ)