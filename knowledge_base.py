# knowledge_base.py

NZ_RTA_2026 = {
    "statutes": "Residential Tenancies Act 1986 (updated 2026), Healthy Homes Standards, Privacy Act 2020, Asbestos Regulations.",
    "mandatory_checks": [
        "Maintenance Responsibilities",
        "Healthy Homes Compliance Statement",
        "Insurance Statement (disclosing excess amounts)",
        "Insulation Statement (location and R-value)",
        "Smoke Alarm Compliance (must be working/photoelectric)[cite: 4]",
        "Bond Lodgement (must be lodged with Tenancy Services within 23 working days)[cite: 4]",
        "Landlord/Agent Contact Details & Address for Service[cite: 4]",
        "Asbestos Disclosure (for pre-2000 builds)",
        "Maximum Rent in Advance (2 weeks limit)[cite: 4]"
    ],
    "red_flags": [
        "Professional carpet cleaning requirements (illegal unless damage-based)[cite: 4]",
        "Total pet bans (Unreasonable under 2026 reforms)[cite: 4]",
        "Pet bonds exceeding 1 week's rent[cite: 4]",
        "Rent increases occurring more than once every 12 months[cite: 4]",
        "Tenant responsible for 'fair wear and tear'[cite: 4]",
        "Fixed-term-only clauses (attempting to block automatic periodic conversion)",
        "Unlawful letting fees (abolished)[cite: 4]"
    ],
    "remedy_suggestions": {
        "Carpet Cleaning": "Request removal of the clause or amendment to 'Tenant must leave the property in a reasonably clean and tidy condition'.[cite: 4]",
        "Pet Ban": "Cite RTA 2026 reforms; suggest a 'Pet Agreement' instead of a flat ban.[cite: 4]",
        "Insurance": "Ensure the landlord's insurance excess is disclosed to avoid tenant liability for accidental damage.[cite: 4]"
    }
}

AU_RTA_2026 = {
    "statutes": "Residential Tenancies Acts (VIC 1997 / NSW 2010 / QLD 2008) including 2026 Minimum Standards reforms.",
    "mandatory_checks": [
        "Repair Responsibilities",
        "Valid Notice Periods",
        "Incoming Condition Report (signed by both parties)[cite: 4]",
        "Minimum Housing Standards (electrical safety, heating, locks)[cite: 4]",
        "External Combustible Cladding Disclosure (apartments)",
        "Gas and Electrical Safety Check dates (required every 2 years in VIC)",
        "Bond capped at 4 weeks rent (unless high-rent threshold applies)[cite: 4]",
        "Utility metering (individual meter requirement for charging)[cite: 4]"
    ],
    "red_flags": [
        "Rent bidding (soliciting offers above advertised price)[cite: 4]",
        "Professional fumigation (illegal unless pets kept or damage proved)[cite: 4]",
        "No-grounds evictions during fixed-term[cite: 4]",
        "Mandatory Direct Debit payment (must offer at least one fee-free method)",
        "Utility markups or administrative fees[cite: 4]",
        "Break-lease fee caps (must be actual loss, not arbitrary penalty)"
    ],
    "remedy_suggestions": {
        "Rent Bidding": "Report to state consumer affairs; offer remains at the advertised price.[cite: 4]",
        "Minimum Standards": "Request proof of electrical and gas safety checks before signing.[cite: 4]",
        "Minor Mods": "Request the standard 'Small modifications' form to be attached to the lease.[cite: 4]"
    }
}

US_LEASE_2026 = {
    "statutes": "Fair Housing Act, CA Civil Code, NY HSTPA, Texas Property Code, Federal Lead-Based Paint Disclosure.",
    "mandatory_checks": [
        "Security Deposit Caps (e.g., 1 month in NY/CA)[cite: 4]",
        "Lead Paint Disclosure (for pre-1978 buildings)[cite: 4]",
        "Flood Zone and Radon Gas Disclosures",
        "Notice of Entry (standard 24-48 hours)[cite: 4]",
        "Bedbug History Disclosure (NYC and others)[cite: 4]",
        "Habitability Compliance[cite: 4]"
    ],
    "red_flags": [
        "Waiver of right to sue or trial by jury[cite: 4]",
        "Self-help eviction waivers (landlord changing locks without court order)",
        "Non-refundable 'administrative' or 'move-in' fees[cite: 4]",
        "Overly restrictive guest clauses (violating right to privacy)",
        "Automatic renewal without 30-day notice[cite: 4]",
        "Illegal attorney fee-shifting (non-reciprocal fees)[cite: 4]"
    ],
    "remedy_suggestions": {
        "Late Fees": "Ask for alignment with state caps (e.g., 5% of monthly rent).[cite: 4]",
        "Habitability": "Remove clauses stating the unit is 'as-is' if it waives the landlord's duty to repair.[cite: 4]",
        "Security Deposit": "Ensure the bank name and address where the deposit is held are listed.[cite: 4]"
    }
}

JURISDICTIONS = {
    "New Zealand (Auckland/National)": NZ_RTA_2026,
    "Australia (VIC/NSW/QLD)": AU_RTA_2026,
    "USA (NYC/CA/TX/National)": US_LEASE_2026
}