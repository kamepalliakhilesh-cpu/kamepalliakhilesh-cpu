import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import datetime

def fetch_codechef_data(username):
    """Fetch CodeChef profile data including rating and heatmap info."""
    url = f"https://www.codechef.com/users/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None, None
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Extract rating
    rating = "N/A"
    rating_el = soup.select_one(".rating-number")
    if rating_el:
        rating = rating_el.text.strip()
    
    # Extract stars
    stars = ""
    star_el = soup.select_one(".rating-star span")
    if star_el:
        stars = star_el.text.strip()
    
    # Extract rank
    global_rank = "N/A"
    rank_els = soup.select(".rating-ranks .inline-list li a")
    if rank_els:
        global_rank = rank_els[0].text.strip() if rank_els else "N/A"

    return rating, stars


def generate_rating_svg(username, rating, stars):
    """Generate a clean, attractive CodeChef rating badge SVG."""
    
    # Determine color based on rating
    try:
        r = int(rating)
        if r >= 2500:
            color = "#FF0000"      # Red - 7★
            tier = "7★"
        elif r >= 2200:
            color = "#FF7F00"      # Orange - 6★
            tier = "6★"
        elif r >= 2000:
            color = "#FFBF00"      # Yellow - 5★
            tier = "5★"
        elif r >= 1800:
            color = "#684273"      # Purple - 4★
            tier = "4★"
        elif r >= 1600:
            color = "#3366CC"      # Blue - 3★
            tier = "3★"
        elif r >= 1400:
            color = "#1E7D22"      # Green - 2★
            tier = "2★"
        else:
            color = "#666666"      # Grey - 1★
            tier = "1★"
    except (ValueError, TypeError):
        color = "#666666"
        tier = ""

    star_display = stars if stars else tier
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="120" viewBox="0 0 400 120">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e"/>
      <stop offset="100%" style="stop-color:#16213e"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:{color}"/>
      <stop offset="100%" style="stop-color:{color}88"/>
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
  </defs>
  
  <rect width="400" height="120" rx="12" fill="url(#bg)" filter="url(#shadow)"/>
  <rect x="0" y="0" width="6" height="120" rx="3" fill="url(#accent)"/>
  
  <!-- CodeChef Logo Text -->
  <text x="30" y="35" font-family="'Segoe UI', Arial, sans-serif" font-size="14" font-weight="600" fill="#8892b0">CODECHEF</text>
  
  <!-- Username -->
  <text x="30" y="62" font-family="'Segoe UI', Arial, sans-serif" font-size="20" font-weight="700" fill="#e6f1ff">{username}</text>
  
  <!-- Rating -->
  <text x="30" y="95" font-family="'Segoe UI', Arial, sans-serif" font-size="16" fill="#8892b0">Rating: </text>
  <text x="100" y="95" font-family="'Segoe UI', Arial, sans-serif" font-size="18" font-weight="700" fill="{color}">{rating}</text>
  
  <!-- Stars -->
  <text x="200" y="95" font-family="'Segoe UI', Arial, sans-serif" font-size="18" fill="{color}">{star_display}</text>
  
  <!-- Badge -->
  <rect x="300" y="20" width="80" height="30" rx="15" fill="{color}22" stroke="{color}" stroke-width="1.5"/>
  <text x="340" y="40" font-family="'Segoe UI', Arial, sans-serif" font-size="12" font-weight="600" fill="{color}" text-anchor="middle">{tier if tier else "Rated"}</text>
</svg>'''
    
    return svg


if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "k_v_akhilesh"
    
    print(f"Fetching CodeChef data for {username}...")
    rating, stars = fetch_codechef_data(username)
    
    if rating is None:
        print("Failed to fetch data, generating fallback SVG...")
        rating = "N/A"
        stars = ""
    
    print(f"Rating: {rating}, Stars: {stars}")
    
    svg = generate_rating_svg(username, rating, stars)
    
    output_path = "dist/codechef-stats.svg"
    import os
    os.makedirs("dist", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    
    print(f"SVG saved to {output_path}")
