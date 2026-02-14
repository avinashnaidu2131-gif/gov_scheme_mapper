def find_eligible_schemes(age, income, occupation, land, category, gender, district, schemes):

    eligible_schemes = []

    for scheme in schemes:

        # -------- AGE CHECK --------
        if "min_age" in scheme:
            if age < scheme["min_age"]:
                continue

        if "max_age" in scheme:
            if age > scheme["max_age"]:
                continue

        # -------- INCOME CHECK --------
        if "income_limit" in scheme:
            if income > scheme["income_limit"]:
                continue

        # -------- OCCUPATION CHECK --------
        if "occupation" in scheme:
            scheme_occ = scheme["occupation"]

            if scheme_occ != "Any":
                if isinstance(scheme_occ, list):
                    if occupation not in scheme_occ:
                        continue
                else:
                    if occupation != scheme_occ:
                        continue

        # -------- GENDER CHECK --------
        if "gender_required" in scheme:
            if gender != scheme["gender_required"]:
                continue

        # -------- LAND CHECK --------
        if "land_required" in scheme:
            if scheme["land_required"] is True and land != "Yes":
                continue

        # -------- CATEGORY CHECK --------
        if "priority_category" in scheme:
            if category not in scheme["priority_category"]:
                continue

        # -------- DISTRICT CHECK --------
        if "districts" in scheme:
            scheme_districts = scheme["districts"]

            if scheme_districts != "All":
                if isinstance(scheme_districts, list):
                    if district not in scheme_districts:
                        continue
                else:
                    if district != scheme_districts:
                        continue

        # If ALL checks passed
        eligible_schemes.append(
            (scheme["name"], scheme.get("scheme_category", "General"))
        )

    return eligible_schemes