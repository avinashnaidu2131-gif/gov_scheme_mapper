def find_eligible_schemes(age, income, occupation, land, category, gender, district, schemes):

    eligible_schemes = []

    for scheme in schemes:

        # STRICT occupation match
        if scheme.get("occupation") != occupation:
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

        # If all conditions passed → eligible
        eligible_schemes.append(
            (scheme["name"], scheme.get("scheme_category", "General"))
        )

    return eligible_schemes