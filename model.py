def find_eligible_schemes(age, income, occupation, land, category, schemes):

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

        if score >= 2:
            eligible_schemes.append(scheme["name"])

    return eligible_schemes