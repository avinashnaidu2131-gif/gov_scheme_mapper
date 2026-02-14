def find_eligible_schemes(
    age,
    income,
    occupation,
    land,
    category,
    gender,
    district,
    schemes,
    registration_status,
    income_verified,
    patta_number,
    caste_certificate,
    family_card_number
):

    eligible = []

    for scheme in schemes:

        # ---- Income verification required ----
        if income_verified != "Yes":
            continue

        # ---- Income limit ----
        if "income_limit" in scheme and scheme["income_limit"] is not None:
            if income > scheme["income_limit"]:
                continue

        # ---- Age ----
        if "min_age" in scheme:
            if age < scheme["min_age"]:
                continue

        # ---- Occupation ----
        if scheme["occupation"] != "Any":
            if isinstance(scheme["occupation"], list):
                if occupation not in scheme["occupation"]:
                    continue
            else:
                if occupation != scheme["occupation"]:
                    continue

        # ---- Land ----
        if scheme.get("land_required", False):
            if land != "Yes" or patta_number == "":
                continue

        # ---- Gender ----
        if "gender_required" in scheme:
            if gender != scheme["gender_required"]:
                continue

        # ---- Category ----
        if category not in scheme["priority_category"]:
            continue

        # ---- District ----
        if scheme["districts"] != "All":
            if district not in scheme["districts"]:
                continue

        # ---- Welfare Registration ----
        if occupation in ["Fisherman", "Salt Pan Worker"]:
            if registration_status != "Yes":
                continue

        # ---- Certificate validation ----
        if caste_certificate == "" or family_card_number == "":
            continue

        eligible.append((scheme["name"], scheme["scheme_category"]))

    return eligible