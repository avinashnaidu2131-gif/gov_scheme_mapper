def find_eligible_schemes(
    age,
    income,
    occupation,
    land,
    category,
    gender,
    district,
    registration_status,
    schemes
):

    eligible = []

    for scheme in schemes:

        # Income check
        if scheme.get("income_limit") is not None:
            if income > scheme["income_limit"]:
                continue

        # Age check
        if scheme.get("min_age"):
            if age < scheme["min_age"]:
                continue

        # Occupation check
        scheme_occ = scheme.get("occupation")

        if scheme_occ != "Any":
            if isinstance(scheme_occ, list):
                if occupation not in scheme_occ:
                    continue
            else:
                if occupation != scheme_occ:
                    continue

        # Gender check
        if scheme.get("gender_required"):
            if gender != scheme["gender_required"]:
                continue

        # Land requirement
        if scheme.get("land_required"):
            if land != "Yes":
                continue

        # Category check
        if category not in scheme.get("priority_category", []):
            continue

        # District check
        districts = scheme.get("districts")
        if districts != "All":
            if district not in districts:
                continue

        # Worker registration check (for special schemes)
        if scheme.get("registration_required"):
            if registration_status != "Yes":
                continue

        eligible.append((scheme["name"], scheme["scheme_category"]))

    return eligible