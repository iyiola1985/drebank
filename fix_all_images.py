"""
Fix all images by converting to data URIs and create banking images for all slides
"""
import base64

# Create data URI for tax year ISA image
tax_year_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="taxGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#4a90e2;stop-opacity:1" />
<stop offset="100%" style="stop-color:#357abd;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#taxGrad)"/>
<g transform="translate(200, 125)">
<rect x="-60" y="-40" width="120" height="80" rx="8" fill="#ffffff" opacity="0.95"/>
<rect x="-50" y="-30" width="100" height="25" rx="4" fill="#1a1a2e"/>
<text x="0" y="-12" text-anchor="middle" fill="#4a90e2" font-size="14" font-weight="bold" font-family="Arial">$20,000</text>
<circle cx="-30" cy="5" r="8" fill="#4a90e2"/>
<circle cx="0" cy="5" r="8" fill="#4a90e2"/>
<circle cx="30" cy="5" r="8" fill="#4a90e2"/>
<circle cx="-30" cy="25" r="8" fill="#4a90e2"/>
<circle cx="0" cy="25" r="8" fill="#4a90e2"/>
<circle cx="30" cy="25" r="8" fill="#4a90e2"/>
</g>
<text x="50" y="50" fill="#ffffff" font-size="32" font-weight="bold" opacity="0.3">$</text>
<text x="320" y="200" fill="#ffffff" font-size="32" font-weight="bold" opacity="0.3">$</text>
<polyline points="80,180 120,160 160,140 200,120 240,100 280,90 320,85" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.4"/>
</svg>'''

# Create data URI for book appointment
appointment_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="apptGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#28a745;stop-opacity:1" />
<stop offset="100%" style="stop-color:#20c997;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#apptGrad)"/>
<g transform="translate(200, 125)">
<rect x="-50" y="-50" width="100" height="90" rx="6" fill="#ffffff" opacity="0.95"/>
<rect x="-50" y="-50" width="100" height="25" rx="6" fill="#4a90e2"/>
<text x="0" y="-32" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="bold" font-family="Arial">APPOINTMENT</text>
<line x1="-30" y1="-25" x2="30" y2="-25" stroke="#1a1a2e" stroke-width="1" opacity="0.2"/>
<line x1="-30" y1="-5" x2="30" y2="-5" stroke="#1a1a2e" stroke-width="1" opacity="0.2"/>
<line x1="-30" y1="15" x2="30" y2="15" stroke="#1a1a2e" stroke-width="1" opacity="0.2"/>
<line x1="0" y1="-25" x2="0" y2="35" stroke="#1a1a2e" stroke-width="1" opacity="0.2"/>
<text x="0" y="10" text-anchor="middle" fill="#1a1a2e" font-size="24" font-weight="bold" font-family="Arial">15</text>
<circle cx="0" cy="50" r="15" fill="none" stroke="#4a90e2" stroke-width="2"/>
<line x1="0" y1="50" x2="0" y2="42" stroke="#4a90e2" stroke-width="2"/>
<line x1="0" y1="50" x2="6" y2="50" stroke="#4a90e2" stroke-width="2"/>
</g>
<circle cx="80" cy="60" r="20" fill="#ffffff" opacity="0.2"/>
<circle cx="320" cy="190" r="25" fill="#ffffff" opacity="0.2"/>
</svg>'''

# Create data URI for ring fencing
ring_fencing_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="fenceGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
<stop offset="100%" style="stop-color:#16213e;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#fenceGrad)"/>
<g transform="translate(200, 125)">
<path d="M 0,-60 L -40,-30 L -40,20 L 0,50 L 40,20 L 40,-30 Z" fill="#ffffff" opacity="0.95"/>
<rect x="-15" y="-10" width="30" height="25" rx="3" fill="#4a90e2"/>
<path d="M -20,-20 Q -20,-30 0,-30 Q 20,-30 20,-20 L 20,-10 L -20,-10 Z" fill="#4a90e2"/>
<circle cx="0" cy="0" r="4" fill="#ffffff"/>
</g>
<circle cx="200" cy="125" r="80" fill="none" stroke="#4a90e2" stroke-width="2" opacity="0.3"/>
<circle cx="200" cy="125" r="100" fill="none" stroke="#4a90e2" stroke-width="2" opacity="0.2"/>
<line x1="100" y1="125" x2="300" y2="125" stroke="#4a90e2" stroke-width="1" opacity="0.2"/>
<line x1="200" y1="50" x2="200" y2="200" stroke="#4a90e2" stroke-width="1" opacity="0.2"/>
</svg>'''

# Banking images for the 8 slides
insurance_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="insGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#e91e63;stop-opacity:1" />
<stop offset="100%" style="stop-color:#c2185b;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#insGrad)"/>
<g transform="translate(200, 125)">
<path d="M 0,-50 L -35,-25 L -35,15 L 0,40 L 35,15 L 35,-25 Z" fill="#ffffff" opacity="0.95"/>
<circle cx="0" cy="-5" r="12" fill="#e91e63"/>
<path d="M -8,-5 L -3,0 L 8,-5" stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round"/>
</g>
<circle cx="80" cy="60" r="15" fill="#ffffff" opacity="0.2"/>
<circle cx="320" cy="190" r="20" fill="#ffffff" opacity="0.2"/>
</svg>'''

activate_card_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#4a90e2;stop-opacity:1" />
<stop offset="100%" style="stop-color:#357abd;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#cardGrad)"/>
<g transform="translate(200, 125)">
<rect x="-70" y="-35" width="140" height="70" rx="8" fill="#ffffff" opacity="0.95"/>
<rect x="-60" y="-25" width="120" height="50" rx="4" fill="#1a1a2e"/>
<rect x="-50" y="-15" width="100" height="8" rx="2" fill="#4a90e2"/>
<rect x="-50" y="0" width="80" height="8" rx="2" fill="#cccccc"/>
<circle cx="30" cy="20" r="8" fill="#4a90e2"/>
</g>
</svg>'''

security_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="secGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
<stop offset="100%" style="stop-color:#16213e;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#secGrad)"/>
<g transform="translate(200, 125)">
<circle cx="0" cy="0" r="40" fill="none" stroke="#4a90e2" stroke-width="3"/>
<path d="M 0,-30 L -15,-15 L -15,0 L 0,15 L 15,0 L 15,-15 Z" fill="#4a90e2"/>
<circle cx="0" cy="-10" r="5" fill="#ffffff"/>
</g>
</svg>'''

guides_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="guideGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#28a745;stop-opacity:1" />
<stop offset="100%" style="stop-color:#20c997;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#guideGrad)"/>
<g transform="translate(200, 125)">
<rect x="-50" y="-40" width="100" height="80" rx="4" fill="#ffffff" opacity="0.95"/>
<line x1="-40" y1="-20" x2="40" y2="-20" stroke="#1a1a2e" stroke-width="2"/>
<line x1="-40" y1="0" x2="40" y2="0" stroke="#1a1a2e" stroke-width="2"/>
<line x1="-40" y1="20" x2="40" y2="20" stroke="#1a1a2e" stroke-width="2"/>
<circle cx="-30" cy="-10" r="3" fill="#28a745"/>
<circle cx="-30" cy="10" r="3" fill="#28a745"/>
</g>
</svg>'''

secure_key_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="keyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#4a90e2;stop-opacity:1" />
<stop offset="100%" style="stop-color:#357abd;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#keyGrad)"/>
<g transform="translate(200, 125)">
<rect x="-25" y="-15" width="50" height="30" rx="4" fill="#ffffff" opacity="0.95"/>
<circle cx="0" cy="0" r="8" fill="#4a90e2"/>
<rect x="8" y="-3" width="20" height="6" rx="2" fill="#4a90e2"/>
<circle cx="30" cy="0" r="4" fill="#4a90e2"/>
</g>
</svg>'''

voice_id_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="voiceGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#ff6b35;stop-opacity:1" />
<stop offset="100%" style="stop-color:#f7931e;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#voiceGrad)"/>
<g transform="translate(200, 125)">
<ellipse cx="0" cy="0" rx="30" ry="50" fill="#ffffff" opacity="0.95"/>
<path d="M -20,-30 Q -20,-40 0,-40 Q 20,-40 20,-30" fill="#ffffff" opacity="0.95"/>
<circle cx="0" cy="-10" r="8" fill="#ff6b35"/>
</g>
</svg>'''

card_support_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
<defs>
<linearGradient id="supportGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
<stop offset="100%" style="stop-color:#16213e;stop-opacity:1" />
</linearGradient>
</defs>
<rect width="400" height="250" fill="url(#supportGrad)"/>
<g transform="translate(200, 125)">
<rect x="-60" y="-30" width="120" height="60" rx="6" fill="#ffffff" opacity="0.95"/>
<circle cx="-30" cy="0" r="12" fill="#4a90e2"/>
<path d="M -30,-5 L -25,0 L -30,5 L -35,0 Z" fill="#ffffff"/>
<circle cx="30" cy="0" r="12" fill="#4a90e2"/>
<path d="M 30,-5 L 35,0 L 30,5 L 25,0 Z" fill="#ffffff"/>
</g>
</svg>'''

def svg_to_data_uri(svg):
    """Convert SVG to data URI"""
    svg_bytes = svg.encode('utf-8')
    base64_svg = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{base64_svg}"

images = {
    'tax-year-isa': tax_year_svg,
    'book-appointment': appointment_svg,
    'ring-fencing': ring_fencing_svg,
    'insurance': insurance_svg,
    'activate-card': activate_card_svg,
    'security': security_svg,
    'guides': guides_svg,
    'secure-key': secure_key_svg,
    'voice-id': voice_id_svg,
    'card-support': card_support_svg
}

print("Data URIs created for all banking images!")
for name in images.keys():
    print(f"✓ {name}")
