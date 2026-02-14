def find_eligible_schemes(age, income, occupation, land, category, schemes):

    results = []

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

        # Decide eligibility
        if score >= 2:
            status = "Eligible"
        else:
            status = "Not Eligible"

        results.append((scheme["name"], status))

    return results
