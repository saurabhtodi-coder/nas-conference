import csv
from pathlib import Path
from collections import defaultdict

bios_dir = Path("bios")

# Define all files including mentors
takshashila_file = "Takshashila_Team.csv"
other_sections = {
    "Invitees": "invitees-all-bio.csv",
    "LEPF Fellows": "lepf-bios.csv",
    "NASC Fellows": "nasc-fellows-bio copy.csv",
    "NASP Fellows": "nasp-bios.csv",
    "NAST Fellows": "nast-fellows-bios copy.csv",
    "NAST Mentors": "mentor-list copy.csv",
    "NASP Mentors": "fellow-list copy.csv",  # Using fellow-list for NASP mentors
}

def normalize_name(name):
    """Normalize name for comparison"""
    return name.strip().lower()

# Extract Takshashila staff names
takshashila_names = {}
takshashila_roles = {}

filepath = bios_dir / takshashila_file
if filepath.exists():
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row:
                name = row.get("Name", "").strip()
                category = row.get("Category", "").strip()
                designation = row.get("Designation", "").strip()
                if name:
                    normalized = normalize_name(name)
                    takshashila_names[normalized] = name
                    takshashila_roles[normalized] = {
                        "original_name": name,
                        "category": category,
                        "designation": designation
                    }

# Extract names from other sections
other_names = defaultdict(lambda: {"normalized": set(), "originals": {}})

for section, filename in other_sections.items():
    filepath = bios_dir / filename
    if not filepath.exists():
        print(f"⚠️  File not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        # Special handling for mentor-list file (no headers)
        if "mentor-list" in filename.lower():
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # mentor-list format: Name,Track (no header)
                parts = line.split(',', 1)
                if parts:
                    name = parts[0].strip()
                    if name:
                        normalized = normalize_name(name)
                        other_names[section]["normalized"].add(normalized)
                        other_names[section]["originals"][normalized] = name
        # Special handling for NASC file (no headers)
        elif "nasc-fellows" in filename.lower():
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split(',', 1)
                if parts:
                    name = parts[0].strip()
                    if name:
                        normalized = normalize_name(name)
                        other_names[section]["normalized"].add(normalized)
                        other_names[section]["originals"][normalized] = name
        # Special handling for fellow-list file (no headers)
        elif "fellow-list" in filename.lower():
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split(',', 1)
                if parts:
                    name = parts[0].strip()
                    if name:
                        normalized = normalize_name(name)
                        other_names[section]["normalized"].add(normalized)
                        other_names[section]["originals"][normalized] = name
        else:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    name = row.get("Name", "").strip()
                    if name:
                        normalized = normalize_name(name)
                        other_names[section]["normalized"].add(normalized)
                        other_names[section]["originals"][normalized] = name

# Compare Takshashila staff with other sections
print("=" * 100)
print("TAKSHASHILA STAFF vs OTHER PARTICIPANT SECTIONS")
print("=" * 100)
print()

overlaps_found = False

for section in sorted(other_sections.keys()):
    intersection = set(takshashila_names.keys()) & other_names[section]["normalized"]
    
    if intersection:
        overlaps_found = True
        print(f"\n{'=' * 100}")
        print(f"TAKSHASHILA TEAM ↔ {section.upper()}: {len(intersection)} overlap(s)")
        print(f"{'=' * 100}")
        
        for normalized_name in sorted(intersection):
            ts_role = takshashila_roles[normalized_name]
            other_name = other_names[section]["originals"][normalized_name]
            
            print(f"\n  👤 {ts_role['original_name']}")
            print(f"     Takshashila Role:")
            print(f"       - Category: {ts_role['category']}")
            print(f"       - Designation: {ts_role['designation']}")
            print(f"     Also listed in: {section}")
            print(f"       - Name: {other_name}")

if not overlaps_found:
    print("\n✅ No overlaps between Takshashila Staff and other participant sections!")

# Summary statistics
print(f"\n\n{'=' * 100}")
print("SUMMARY STATISTICS")
print(f"{'=' * 100}\n")

print(f"Takshashila Team members: {len(takshashila_names)}")
for section in sorted(other_sections.keys()):
    count = len(other_names[section]["normalized"])
    print(f"{section}.....................: {count}")

print(f"\n{'=' * 100}")
print("BREAKDOWN BY TAKSHASHILA CATEGORY")
print(f"{'=' * 100}\n")

categories = defaultdict(list)
for normalized, role_info in takshashila_roles.items():
    category = role_info['category']
    categories[category].append(role_info)

for category in sorted(categories.keys()):
    members = categories[category]
    print(f"{category}: {len(members)} members")
    for member in sorted(members, key=lambda x: x['original_name']):
        # Check if this member appears in other sections
        member_norm = normalize_name(member['original_name'])
        appears_in = [sec for sec, data in other_names.items() if member_norm in data["normalized"]]
        
        if appears_in:
            print(f"  ⚠️  {member['original_name']} - {member['designation']} [ALSO IN: {', '.join(appears_in)}]")
        else:
            print(f"  • {member['original_name']} - {member['designation']}")
    print()
