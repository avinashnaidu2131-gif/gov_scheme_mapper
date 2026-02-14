def find_eligible_schemes(age, income, occupation, land, category, gender, district, schemes, registration_status):

    eligible_schemes = []

    for scheme in schemes:

        # ---- AGE CHECK ----
        if "min_age" in scheme:
            if age < scheme["min_age"]:
                continue

        if "max_age" in scheme:
            if age > scheme["max_age"]:
                continue

        # ---- INCOME CHECK ----
        if "income_limit" in scheme:
            if scheme["income_limit"] is not None:
                if income > scheme["income_limit"]:
                    continue

        # ---- OCCUPATION CHECK ----
        if "occupation" in scheme:
            scheme_occ = scheme["occupation"]

            if scheme_occ != "Any":
                if isinstance(scheme_occ, list):
                    if occupation not in scheme_occ:
                        continue
                else:
                    if occupation != scheme_occ:
                        continue

        # ---- GENDER CHECK ----
        if "gender_required" in scheme:
            if gender != scheme["gender_required"]:
                continue

        # ---- LAND CHECK ----
        if "land_required" in scheme:
            if scheme["land_required"] and land != "Yes":
                continue

        # ---- CATEGORY CHECK ----
        if "priority_category" in scheme:
            if category not in scheme["priority_category"]:
                continue

        # ---- DISTRICT CHECK ----
        if "districts" in scheme:
            scheme_districts = scheme["districts"]

            if scheme_districts != "All":
                if isinstance(scheme_districts, list):
                    if district not in scheme_districts:
                        continue
                else:
                    if district != scheme_districts:
                        continue

        # ---- WORKER REGISTRATION CHECK ----
        if "eligibility_conditions" in scheme:
            conditions = scheme["eligibility_conditions"]

            if conditions.get("registration_required", False):
                if registration_status != "Yes":
                    continue

        eligible_schemes.append(
            (scheme["name"], scheme.get("scheme_category", "General"))
        )

    return eligible_schemes