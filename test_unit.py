from data.backend import ModelRecommendation

mr = ModelRecommendation(model_type="MLOVIE", film_list_titles=["The Matrix", "Total Recall", "Bangkok Breaking", "Squid Game"])
titles = mr.get_title()
years = mr.get_year()
print("Suggested Titles:")
for title in titles:
    print(f"- {title}, {years[titles.index(title)]}")