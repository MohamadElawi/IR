import pycountry

names_dic = []

for country in pycountry.countries:
    names_dic.append([country.name, country.alpha_2])

# Example usage:
for country in names_dic:
    country_name, abbreviation = country
    print(f'"{country_name}" :"{abbreviation}" ,')