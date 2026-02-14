def find_eligible_schemes(age, income, occupation, land, category, gender, district, schemes):

    eligible_schemes = []

    for scheme in schemes:

        score = 0

        # Income check
        if income <= scheme.get("income_limit", 0):
            score += 1

        # Occupation check
        if scheme.get("occupation") == occupation:
            score += 1

        # Land requirement check
        if scheme.get("land_required") and land == "Yes":
            score += 1

        # Category check
        if category in scheme.get("priority_category", []):
            score += 1

        # District check (SAFE VERSION)
        scheme_districts = scheme.get("districts", "All")

        if scheme_districts != "All":
            if isinstance(scheme_districts, list):
                if district not in scheme_districts:
                    continue

        # Add if eligible
        if score >= 2:
            eligible_schemes.append(
                (scheme["name"], scheme.get("scheme_category", "General"))
            )

    return eligible_schemes