"""
Generates clean synthetic demo visual cards for CityPulse testing.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SAMPLES = [
    {
        "filename": "sample_drain.jpg",
        "title": "7th & Market: Storm Drain Inflow",
        "color": (26, 54, 93),
        "accent": (59, 130, 246),
        "details": ["Grate Obstruction: ~80%", "Leaf Mulch & Litter", "Standing Runoff: 4-inch Pool", "Location: BLOCK-A"]
    },
    {
        "filename": "sample_sidewalk.jpg",
        "title": "Elmwood Pedestrian Walkway",
        "color": (120, 53, 15),
        "accent": (245, 158, 11),
        "details": ["2.5-Inch Vertical Upheaval", "Concrete Fracture Line", "Wheelchair Corridor Blocked", "Location: BLOCK-B"]
    },
    {
        "filename": "sample_pothole.jpg",
        "title": "4th Ave Transit Corridor",
        "color": (127, 29, 29),
        "accent": (239, 68, 68),
        "details": ["18-inch Rim Depression", "Exposed Subbase Gravel", "Bus Wheel Impact Path", "Location: BLOCK-C"]
    },
    {
        "filename": "sample_rubbish.jpg",
        "title": "Pine St Commercial Alleyway",
        "color": (76, 29, 149),
        "accent": (168, 85, 247),
        "details": ["Receptacle Overflow (+18in)", "Cardboard & Refuse Spill", "Sidewalk Clearance Obstructed", "Location: BLOCK-D"]
    }
]

def generate():
    for item in SAMPLES:
        img = Image.new("RGB", (800, 600), color=item["color"])
        draw = ImageDraw.Draw(img)
        
        # Border
        draw.rectangle([20, 20, 780, 580], outline=item["accent"], width=4)
        
        # Title bar
        draw.rectangle([40, 40, 760, 110], fill=item["accent"])
        draw.text((60, 60), f"CITYPULSE CAMERA OBSERVATION: {item['title']}", fill=(255, 255, 255))
        
        # Simulated street grid
        for y in range(140, 360, 40):
            draw.line([(60, y), (740, y)], fill=(80, 80, 90), width=1)
            
        # Draw mock target defect boundary
        draw.rectangle([250, 160, 550, 340], outline=(255, 255, 255), width=3)
        draw.text((260, 170), "[TARGET DEFECT ZONE]", fill=(255, 255, 255))
        
        # Evidence details
        y_text = 400
        draw.text((60, y_text), "AUTOMATED MULTIMODAL EVIDENCE TAGS:", fill=(255, 255, 255))
        for line in item["details"]:
            y_text += 35
            draw.text((80, y_text), f"• {line}", fill=(220, 225, 230))
            
        filepath = os.path.join(OUTPUT_DIR, item["filename"])
        img.save(filepath, quality=90)
        print(f"Generated: {filepath}")

if __name__ == "__main__":
    generate()
