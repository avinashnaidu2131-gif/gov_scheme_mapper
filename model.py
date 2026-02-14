def find_eligible_schemes(age, income, occupation, land, category, gender, district, schemes):

    eligible_schemes = []

    for scheme in schemes:

        # -------- OCCUPATION CHECK --------
        scheme_occ = scheme.get("occupation")

        if scheme_occ:
            if scheme_occ != "Any":
                if isinstance(scheme_occ, list):
                    if occupation not in scheme_occ:
                        continue
                else:
                    if scheme_occ != occupation:
                        continue

        # -------- GENDER CHECK --------
        required_gender = scheme.get("gender_required")
        if required_gender:
            if required_gender != gender:
                continue

        # -------- INCOME CHECK --------
        if income > scheme.get("income_limit", 999999999):
            continue

        # -------- LAND CHECK --------
        if scheme.get("land_required") and land != "Yes":
            continue

        # -------- CATEGORY CHECK --------
        if category not in scheme.get("priority_category", []):
            continue

        # -------- DISTRICT CHECK (SAFE) --------
        scheme_districts = scheme.get("districts")
        if scheme_districts and scheme_districts != "All":
            if isinstance(scheme_districts, list):
                if district not in scheme_districts:
                    continue

        eligible_schemes.append(
            (scheme["name"], scheme.get("scheme_category", "General"))
        )

    return eligible_schemes