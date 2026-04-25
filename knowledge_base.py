# knowledge_base.py

# New Zealand Framework
NZ_RTA_2026 = {
    "statutes": "Residential Tenancies Act 1986 (Updated 2026), Healthy Homes Standards.",
    "red_flags": [
        "Professional carpet cleaning: Landlords cannot require this unless there is actual damage.",
        "Short notice periods: Periodic tenants only need to give 21 days (unless updated to 28).",
        "Illegal Pet Bans: Landlords cannot unreasonably refuse pets (2025/26 law change).",
        "Illegal Pet Bonds: Pet bonds are capped at 2 weeks extra rent (total max 6 weeks bond).",
        "Rent increase frequency: Must not be more than once every 12 months.",
        "Maintenance: Tenants are NOT responsible for fair wear and tear.",
        "Smoke alarms: Landlords must provide/maintain; shifting this to tenants is void."
    ],
    "mandatory_checks": ["Healthy Homes Statement", "Insurance Statement", "Insulation Statement"]
}

# Australia Framework (Consolidated VIC/NSW/QLD 2026 Standards)
AU_RTA_2026 = {
    "statutes": "State-specific Residential Tenancies Acts (2026 reform versions).",
    "red_flags": [
        "No-grounds evictions: Generally unlawful; landlords must provide a specific valid reason.",
        "Rent Bidding: Any clause suggesting the tenant 'bid' higher than advertised is illegal.",
        "Professional fumigation: Cannot be mandated unless the tenant kept a pet.",
        "Utility markups: Landlords cannot charge more for water/electricity than the utility provider charges.",
        "Entry rights: Landlords must give 48-hour notice for inspections (State dependent, usually max 4 per year).",
        "Bond limits: Generally capped at 4 weeks rent if rent is under a certain threshold."
    ],
    "mandatory_checks": ["Minimum Standards Compliance (locks, bins, weatherproofing)", "Condition Report Signature"]
}

# USA Framework (Federal + Key State Protections CA/NY/TX)
US_LEASE_2026 = {
    "statutes": "Fair Housing Act, State Civil Codes (CA AB-1482, NY HSTPA).",
    "red_flags": [
        "Waiver of Habitability: Clauses forcing tenants to accept a 'as-is' unit with defects are void.",
        "Non-refundable deposits: Illegal in many states (e.g., California).",
        "Security Deposit Caps: Often limited to 1 month's rent (recent 2024/25 laws in CA).",
        "Automatic Renewal: Clauses that auto-renew for a full year without a reminder notice.",
        "Late fees: Must be 'reasonable' (typically capped at 5-10% of monthly rent).",
        "Unlawful Entry: Landlords must typically give 24-hour notice for non-emergencies."
    ],
    "mandatory_checks": ["Lead-Based Paint Disclosure (if pre-1978)", "Security Deposit Receipt", "Bedbug Disclosure (NY/CA)"]
}

# Mapping for app.py
JURISDICTIONS = {
    "New Zealand (RTA 2026)": NZ_RTA_2026,
    "Australia (VIC/NSW/QLD)": AU_RTA_2026,
    "USA (NYC/CA/TX)": US_LEASE_2026
}