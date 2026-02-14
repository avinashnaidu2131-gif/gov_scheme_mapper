def find_eligible_schemes(age, income, occupation, land, category, gender, district, schemes):

    eligible_schemes = []

    for scheme in schemes:

        score = 0

        if income <= scheme["income_limit"]:
            score += 1

        if scheme["occupation"] == occupation:
            score += 1

        if scheme["land_required"] and land == "Yes":
            score += 1

        if category in scheme["priority_category"]:
            score += 1

        # District filter
        if scheme["districts"] != "All" and district not in scheme["districts"]:
            continue

        if score >= 2:
            eligible_schemes.append((scheme["name"], scheme["scheme_category"]))

    return eligible_schemes