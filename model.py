def find_eligible_schemes(age, income, occupation, land, category, gender, district, schemes):

    eligible_schemes = []

    for scheme in schemes:

        # Occupation check (allow "Any")
        scheme_occ = scheme.get("occupation")
        if scheme_occ != "Any" and scheme_occ != occupation:
            continue

        # Gender check
        required_gender = scheme.get("gender_required")
        if required_gender and required_gender != gender:
            continue

        # Income check
        if income > scheme.get("income_limit", 0):
            continue

        # Land check
        if scheme.get("land_required") and land != "Yes":
            continue

        # Category check
        if category not in scheme.get("priority_category", []):
            continue

        # District check
        scheme_districts = scheme.get("districts", "All")
        if scheme_districts != "All":
            if isinstance(scheme_districts, list):
                if district not in scheme_districts:
                    continue

        # Age-based logic
        min_age = scheme.get("min_age")
        if min_age and age < min_age:
            continue

        max_age = scheme.get("max_age")
        if max_age and age > max_age:
            continue

        eligible_schemes.append(
            (scheme["name"], scheme.get("scheme_category", "General"))
        )

    return eligible_schemes