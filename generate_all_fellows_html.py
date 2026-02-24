#!/usr/bin/env python3
import csv

# Read the CSV
fellows_data = {}
all_fellows_list = []
with open('bios/fellow-list copy.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row['Name'].strip()
        track = row['Fellowship Track'].strip()
        if track not in fellows_data:
            fellows_data[track] = []
        fellows_data[track].append(name)
        all_fellows_list.append((name, track))

# Photo mapping - only fellows with these have photos
photo_mapping = {
    'Aaratrica Kashyap': 'Aaratrica Kashyap - Reea Kashyap.jpeg',
    'Anandana Kapur': 'Anandana Kapur.png',
    'Arpit Tripathi': 'arpit_tripathi_photo - Arpit.jpg',
    'Bhargavi PBA': 'Bhargavi PBA_photo - Bhargavi PBA.png',
    'Chetna Anjali': 'chetna.jpeg',
    'Debasri Mukherjee': 'DEBASRI PASSPORT.jpg',
    'Jason Joseph': 'Protrait - Jason Joseph.jpg',
    'Kashish Parpiani': 'Kashish Parpiani - Kashish Parpiani.jpeg',
    'Manav Gudwani': 'IMAGE. - Manav Gudwani.jpg',
    'Neeraj Gudipati': 'Neeraj_Gudipati_NAST - Neeraj Gudipati.jpeg',
    'Nistha Kumari Singh': 'Nistha Photo - Nistha.png',
    'Nrusingha Narayan Dey': 'NRUSINGHA - Nrusingha narayan Dey.jpg',
    'Pranav Satyanath': 'IMG - Pranav Satyanath.jpg',
    'Rajesh Gopal': 'rajesh.jpeg',
    'Shubham Shukla': '20241018_190653(1) - Shubham Shukla.jpg',
    'Siddhant Chandra': 'Siddhant Chandra - Reea Kashyap.jpeg',
    'Soumya Kanti Ghosh': 'Soumya kanti Ghosh - Soumya kanti Ghosh.jpeg',
    'Yash Khandelwal': 'Yash Khandelwal - Yash Khandelwal.jpg'
}

# Map track names to track labels and colors
track_map = {
    'NASC Fellow': {'label': 'NASC - China Track', 'color': '#1d3557'},
    'NASP Fellow': {'label': 'NASP - Pakistan Track', 'color': '#2d6a4f'},
    'NAST Fellow': {'label': 'NAST - Tech Geopolitics', 'color': '#7b2d8b'},
    'LEPF Fellow': {'label': 'LEPF - Law Enforcement', 'color': '#b5451b'}
}

# Generate HTML for fellows section
html_parts = []
html_parts.append('<div class="people-group" id="people-fellows">')

# Group by track in order
track_order = ['NASC Fellow', 'NASP Fellow', 'NAST Fellow', 'LEPF Fellow']
total_fellows = 0

for track_key in track_order:
    if track_key not in fellows_data:
        continue
    
    track_fellows_sorted = sorted(fellows_data[track_key])
    
    if not track_fellows_sorted:
        continue
    
    track_info = track_map[track_key]
    html_parts.append(f'<div class="people-track-section"><div class="people-track-heading" style="background:{track_info["color"]};">{track_info["label"]}</div><div class="people-grid">')
    
    for name in track_fellows_sorted:
        total_fellows += 1
        if name in photo_mapping:
            # Fellow with photo
            photo = photo_mapping[name]
            html_parts.append(f'<div class="person-card"><img src="images/nast-fellows/{photo}" alt="{name}" style="width:100%;height:120px;object-fit:cover;border-radius:4px;" onerror="this.style.display=\'none\'"><div class="person-name" style="margin-top:8px;">{name}</div></div>')
        else:
            # Fellow without photo - just show name
            html_parts.append(f'<div class="person-card"><div class="person-name" style="margin-top:8px;">{name}</div></div>')
    
    html_parts.append('</div></div>')

html_parts.append('</div>')

html_output = ''.join(html_parts)
print(html_output)

# Count fellows
print("\n\n=== COUNT ===", file=__import__('sys').stderr)
print(f"Total fellows: {total_fellows}", file=__import__('sys').stderr)
for track_key in track_order:
    if track_key in fellows_data:
        count = len(fellows_data[track_key])
        print(f"{track_key}: {count}", file=__import__('sys').stderr)
