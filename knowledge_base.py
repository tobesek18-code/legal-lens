# knowledge_base.py

NZ_RTA_2026 = {
    "statutes": "Residential Tenancies Act 1986 (updated to 2026), Healthy Homes Standards, Residential Tenancies Amendment reforms.",
    "mandatory_checks": [
        "Healthy Homes Statement",
        "Insurance Statement",
        "Insulation Statement",
        "Smoke Alarm Compliance",
        "Bond Lodgement Requirements",
        "Quiet Enjoyment Rights",
        "Landlord Contact Details",
        "Maintenance Responsibilities",
        "Entry Notice Rules"
    ],
    "red_flags": [
        "Professional carpet cleaning requirements",
        "Illegal pet bans or unreasonable refusal",
        "Pet bond exceeding legal limits",
        "Rent increases more than once every 12 months",
        "Tenant responsible for fair wear and tear",
        "Illegal smoke alarm obligations shifted to tenant",
        "Unlawful inspection frequency",
        "Unfair termination clauses"
    ]
}

AU_RTA_2026 = {
    "statutes": "State-based Residential Tenancies Acts (VIC / NSW / QLD updated 2026 reforms).",
    "mandatory_checks": [
        "Condition Report",
        "Minimum Housing Standards",
        "Bond Compliance",
        "Repair Responsibilities",
        "Valid Notice Periods",
        "Entry Rights Compliance"
    ],
    "red_flags": [
        "No-grounds eviction clauses",
        "Rent bidding language",
        "Professional fumigation clauses",
        "Utility markups",
        "Excessive inspection rights",
        "Excessive bond requirements"
    ]
}

US_LEASE_2026 = {
    "statutes": "Fair Housing Act, CA Civil Code, NY HSTPA, Texas Property Code.",
    "mandatory_checks": [
        "Security Deposit Rules",
        "Lead Paint Disclosure",
        "Habitability Compliance",
        "Entry Notice Rules",
        "Repair Obligations",
        "Bedbug Disclosure where required"
    ],
    "red_flags": [
        "Waiver of habitability",
        "Non-refundable deposits",
        "Automatic yearly renewals",
        "Unreasonable late fees",
        "Unlawful landlord entry",
        "Illegal security deposit caps"
    ]
}

JURISDICTIONS = {
    "New Zealand (RTA 2026)": NZ_RTA_2026,
    "Australia (VIC/NSW/QLD)": AU_RTA_2026,
    "USA (NYC/CA/TX)": US_LEASE_2026
}
