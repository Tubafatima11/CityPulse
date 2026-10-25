"""
Generates clean Hyderabad civic demo visual cards for CityPulse testing.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLES = [
    {
        "filename": "sample_drain.jpg",
        "title": "Gachibowli Bio-Diversity Junction (Inflow Drain)",
        "color": (26, 54, 93),
        "accent": (59, 130, 246),
        "details": ["Grate Blockage: ~85% with monsoon silt", "Waterlogging: 5-inch pool into IT corridor", "GHMC Zone: Serilingampally (West)", "Coordinates: 17.4401° N, 78.3489° E"]
    },
    {
        "filename": "sample_sidewalk.jpg",
        "title": "Charminar Pedestrian Promenade (Lad Bazaar)",
        "color": (120, 53, 15),
        "accent": (245, 158, 11),
        "details": ["Cobblestone slab upheaval (>2 inches)", "Direct hazard for elderly pedestrians & tourists", "GHMC Zone: Charminar (South)", "Coordinates: 17.3616° N, 78.4747° E"]
    },
    {
        "filename": "sample_pothole.jpg",
        "title": "Road No. 36 Jubilee Hills (Near Metro Pillar 1650)",
        "color": (127, 29, 29),
        "accent": (239, 68, 68),
        "details": ["Crater with exposed aggregate in fast lane", "Severe hazard for two-wheelers & RTC buses", "GHMC Zone: Khairatabad (Central)", "Coordinates: 17.4319° N, 78.4073° E"]
    },
    {
        "filename": "sample_rubbish.jpg",
        "title": "Kukatpally Y-Junction (Near Metro Station)",
        "color": (76, 29, 149),
        "accent": (168, 85, 247),
        "details": ["GHMC Community Dumper Bin Overflow (+2ft)", "Commercial boxes spilling onto service road", "GHMC Zone: Kukatpally (North)", "Coordinates: 17.4938° N, 78.3995° E"]
    }
]

def generate():
    for item in SAMPLES:
        img = Image.new("RGB", (800, 600), color=item["color"])
        draw = ImageDraw.Draw(img)
        
        # Outer border
        draw.rectangle([20, 20, 780, 580], outline=item["accent"], width=4)
        
        # Header bar
        draw.rectangle([40, 40, 760, 110], fill=item["accent"])
        draw.text((60, 55), "GHMC CIVIC INCIDENT SURVEILLANCE — HYDERABAD", fill=(255, 255, 255))
        draw.text((60, 80), item["title"], fill=(230, 240, 255))
        
        # Grid lines representing road inspection
        for y in range(140, 360, 40):
            draw.line([(60, y), (740, y)], fill=(80, 80, 90), width=1)
            
        # Target defect marker
        draw.rectangle([250, 160, 550, 340], outline=(255, 255, 255), width=3)
        draw.text((260, 170), "[TARGET CIVIC HAZARD ZONE]", fill=(255, 255, 255))
        
        # Evidence details
        y_text = 390
        draw.text((60, y_text), "AUTOMATED MULTIMODAL EVIDENCE TAGS:", fill=(255, 255, 255))
        for line in item["details"]:
            y_text += 32
            draw.text((80, y_text), f"• {line}", fill=(220, 225, 230))
            
        filepath = os.path.join(OUTPUT_DIR, item["filename"])
        img.save(filepath, quality=90)
        print(f"Generated: {filepath}")

if __name__ == "__main__":
    generate()
