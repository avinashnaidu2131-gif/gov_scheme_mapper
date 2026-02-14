def find_eligible_schemes(
    age, income, occupation, land, category, gender, district,
    schemes, registration_status,
    income_verified, patta_number,
    caste_certificate, family_card_number
):

    eligible_schemes = []

    # -------- Revenue Mandatory Checks --------
    if income_verified != "Yes":
        return []

    if not family_card_number:
        return []

    if not caste_certificate:
        return []

    if land == "Yes" and not patta_number:
        return []

    for scheme in schemes:

        if scheme.get("min_age") and age < scheme["min_age"]:
            continue

        if scheme.get("income_limit") is not None:
            if income > scheme["income_limit"]:
                continue

        scheme_occ = scheme.get("occupation")
        if scheme_occ and scheme_occ != "Any":
            if isinstance(scheme_occ, list):
                if occupation not in scheme_occ:
                    continue
            else:
                if occupation != scheme_occ:
                    continue

        if scheme.get("gender_required"):
            if gender != scheme["gender_required"]:
                continue

        if scheme.get("land_required") and land != "Yes":
            continue

        if scheme.get("priority_category"):
            if category not in scheme["priority_category"]:
                continue

        scheme_districts = scheme.get("districts")
        if scheme_districts != "All":
            if isinstance(scheme_districts, list):
                if district not in scheme_districts:
                    continue
            else:
                if district != scheme_districts:
                    continue

        if scheme.get("eligibility_conditions"):
            if scheme["eligibility_conditions"].get("registration_required"):
                if registration_status != "Yes":
                    continue

        eligible_schemes.append(
            (scheme["name"], scheme.get("scheme_category","General"))
        )

    return eligible_schemes