import csv
from pathlib import Path
from collections import defaultdict

# Define participant sections
bios_dir = Path("bios")
participant_files = {
    "NASC Fellows": "nasc-fellows-bio copy.csv",
    "NASP Fellows": "nasp-bios.csv",
    "NAST Fellows": "nast-fellows-bios copy.csv",
    "LEPF Fellows": "lepf-bios.csv",
    "Invitees": "invitees-all-bio.csv",
    "Takshashila Team": "Takshashila_Team.csv",
}

# Store names by section
names_by_section = defaultdict(set)
all_entries = defaultdict(list)  # Track which sections have each name

def normalize_name(name):
    """Normalize name for comparison"""
    return name.strip().lower()

# Process each file
for section, filename in participant_files.items():
    filepath = bios_dir / filename
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Special handling for NASC file (no headers)
            if "nasc-fellows" in filename.lower():
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    # NASC file format: Name,Bio (no header)
                    parts = line.split(',', 1)
                    if parts:
                        name = parts[0].strip()
                        if name:
                            normalized = normalize_name(name)
                            names_by_section[section].add(normalized)
                            all_entries[normalized].append(section)
            else:
                reader = csv.DictReader(f)
                for row in reader:
                    if row:
                        # Extract name - all use "Name" column
                        name = row.get("Name", "").strip()
                        
                        if name:
                            normalized = normalize_name(name)
                            names_by_section[section].add(normalized)
                            all_entries[normalized].append(section)
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")

# Known distinct individuals with same name
known_distinct = {
    'amit kumar'  # LEPF Fellow vs Takshashila Team member - verified as distinct individuals
}

# Find duplicates
print("=" * 80)
print("DUPLICATE PARTICIPANT ANALYSIS")
print("=" * 80)
print()

duplicates_found = False

for name, sections in sorted(all_entries.items()):
    if len(sections) > 1 and name not in known_distinct:
        duplicates_found = True
        print(f"⚠️  DUPLICATE FOUND: '{name}'")
        print(f"   Appears in: {', '.join(sections)}")
        print()

if not duplicates_found:
    print("✅ No duplicates found across participant sections!")
    print()

# Show verified distinct entries
for name in sorted(known_distinct):
    if name in all_entries and len(all_entries[name]) > 1:
        print(f"ℹ️  VERIFIED DISTINCT: '{name}'")
        print(f"   Appears in: {', '.join(all_entries[name])} (confirmed as different individuals)")
        print()

# Print summary statistics
print("=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)
print()
for section in sorted(participant_files.keys()):
    count = len(names_by_section[section])
    print(f"{section:.<30} {count:>3} participants")

total_unique = len(all_entries)
total_all = sum(len(names_by_section[s]) for s in names_by_section)
# For verified distinct individuals, add back the extra count
truly_unique = total_unique + len([name for name in known_distinct if name in all_entries and len(all_entries[name]) > 1])
print(f"{'TOTAL (all sections):':.<30} {total_all:>3} participants")
print(f"{'UNIQUE (after dedup):':.<30} {total_unique:>3} participants")
print(f"{'TRULY UNIQUE (verified distinct):':.<30} {truly_unique:>3} participants")
print()

# Additional analysis
print("=" * 80)
print("CROSS-SECTION ANALYSIS")
print("=" * 80)
print()

# Check each pair of sections
sections_list = sorted(participant_files.keys())
has_overlap = False
for i, section1 in enumerate(sections_list):
    for section2 in sections_list[i+1:]:
        intersection = names_by_section[section1] & names_by_section[section2]
        if intersection:
            # Filter out known distinct entries
            actual_duplicates = intersection - known_distinct
            if actual_duplicates:
                has_overlap = True
                print(f"{section1} ↔ {section2}: {len(actual_duplicates)} duplicate(s)")
                for name in sorted(actual_duplicates):
                    print(f"  - {name}")
                print()
            # Show verified distinct
            distinct_in_pair = intersection & known_distinct
            if distinct_in_pair:
                print(f"{section1} ↔ {section2}: {len(distinct_in_pair)} verified distinct (same name, different people)")
                for name in sorted(distinct_in_pair):
                    print(f"  - {name}")
                print()

if not has_overlap:
    print("✅ No overlaps between any sections (excluding verified distinct entries)!")
