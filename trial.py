from google import genai
import os
import urllib.parse
import requests
from playwright.sync_api import sync_playwright
import time
from concurrent.futures import ThreadPoolExecutor
# import asyncio
import base64
import re
# from moviepy import VideoFileClip, concatenate_videoclips
# import shutil
from datetime import datetime 
from datetime import timezone,timedelta
import random
# import yt_dlp
import subprocess
from dotenv import load_dotenv # Add this

# Load the .env file BEFORE you try to access the keys
load_dotenv()
# import threading
import os 
import json
from playwright_stealth import Stealth




items_xml=""
SITE_URL = "https://abdworkspace.github.io/autoWallpaperReels/" 
# The base URL for your raw images on GitHub
RAW_IMG_BASE = "https://abdworkspace.github.io/autoWallpaperReels/wallpaper/"


# for file in os.listdir("wallsa

client=genai.Client(api_key=os.getenv("GENAI_API_KEY"))
print("Client Initialized")
festival_messages={
#   "republicday": [
#     "Good morning {{Name}}! Wishing you a very Happy Republic Day. Here's to celebrating the spirit of our nation, today and always. 🇮🇳",
#     "{{Name}}, this Republic Day, we have something special waiting for you. Visit us and discover pieces that celebrate every woman's pride.",
#     "Happy Republic Day, {{Name}}! Enjoy [X]% off on select pieces at [Boutique Name], because you deserve to feel special too.",
#     "{{Name}}, freedom looks good on you. Explore our new arrivals this Republic Day and pick a look that's truly yours.",
#     "This Republic Day, {{Name}}, we're celebrating every woman who stands tall in her own way. Come treat yourself to something beautiful.",
#     "{{Name}}, our Republic Day edit is here. Limited pieces, timeless style. Visit us before your favourites are gone.",
#     "Happy Republic Day, {{Name}}! May you always wear your confidence as beautifully as you wear our outfits. 🇮🇳",
#     "{{Name}}, celebrate the tricolour spirit with us. Special prices, only for a few days.",
#     "On this special day, {{Name}}, we're grateful to have you with us. Thank you for your trust and support.",
#     "{{Name}}, last day of our Republic Day specials! Don't miss your chance to shop your favourites."
#   ],
#   "Maha Shivaratri": [
#     "{{Name}}, wishing you peace and blessings this Maha Shivaratri. May Lord Shiva bless you with strength and serenity. 🙏",
#     "Har Har Mahadev, {{Name}}! Sending you warm wishes on this sacred night.",
#     "{{Name}}, for your Maha Shivaratri puja, we have a small collection of simple, elegant pieces. Do take a look.",
#     "This Maha Shivaratri, {{Name}}, may all your prayers be answered. Wishing you calm and countless blessings.",
#     "{{Name}}, heading to the temple this Maha Shivaratri? Our soft cotton sarees make for a comfortable, graceful choice.",
#     "Wishing you a blessed Maha Shivaratri, {{Name}}. May this sacred day bring positivity into your life.",
#     "{{Name}}, some occasions call for simplicity. Our understated ethnic pieces are made for days like this.",
#     "Om Namah Shivaya, {{Name}}. Sending you warmth and good wishes on this holy night.",
#     "{{Name}}, thank you for being part of our family. On this Maha Shivaratri, we wish you peace and wellbeing.",
#     "{{Name}}, may Lord Shiva's blessings stay with you always. Happy Maha Shivaratri from [Boutique Name]."
#   ],
#   "Holi": [
#     "Happy Holi, {{Name}}! 🌈 Wishing you a festival full of colour, laughter and beautiful memories.",
#     "{{Name}}, Holi calls for colour, and so does your wardrobe. Check out our vibrant new collection made for the season.",
#     "{{Name}}, planning a Holi brunch or get-together? Our pastel and white co-ord sets are perfect for looking effortlessly pretty.",
#     "This Holi, {{Name}}, add a splash of colour to your closet. New arrivals now in store!",
#     "{{Name}}, celebrate Holi in style! Enjoy [X]% off our festive collection, for a few days only.",
#     "Holi Hai, {{Name}}! 🎉 May your life always be as colourful and joyful as this beautiful festival.",
#     "{{Name}}, once the colours settle, it's time to dress up. Our post-Holi party wear collection is here.",
#     "{{Name}}, we handpicked a few pieces just for you this Holi. Come see what caught our eye.",
#     "Wishing you and your loved ones a very Happy Holi, {{Name}}. May this festival bring joy that lasts all year.",
#     "{{Name}}, our Holi specials end soon. Grab your favourite colourful pieces before they're gone."
#   ],
#   "Ram Navami": [
#     "{{Name}}, wishing you a blessed Ram Navami. May Lord Rama's blessings bring peace to your home. 🙏",
#     "Jai Shri Ram, {{Name}}! Sending you warm wishes on this auspicious day.",
#     "{{Name}}, celebrating Ram Navami with a puja or temple visit? Our elegant traditional wear is perfect for the occasion.",
#     "This Ram Navami, {{Name}}, may your life be filled with truth, courage and devotion.",
#     "{{Name}}, a small, thoughtful collection for Ram Navami is now at [Boutique Name]. Simple, graceful pieces for a special day.",
#     "Wishing you and your family a peaceful Ram Navami, {{Name}}. 🙏",
#     "{{Name}}, some days call for quiet elegance. Explore pieces made for occasions like this.",
#     "Happy Ram Navami, {{Name}}! May this day bring you closer to everything good in life.",
#     "{{Name}}, thank you for trusting us with your special moments. Wishing you a blessed Ram Navami.",
#     "{{Name}}, may Lord Rama's blessings be with you always. Happy Ram Navami from [Boutique Name]."
#   ],
#   "Buddha Purnima": [
#     "{{Name}}, wishing you peace, light and wisdom this Buddha Purnima. 🙏",
#     "On this Buddha Purnima, {{Name}}, may you find a moment of calm in your busy life.",
#     "{{Name}}, Lord Buddha taught us that true beauty comes from within. Wishing you peace on this sacred day.",
#     "May the light of wisdom guide you always, {{Name}}. Happy Buddha Purnima.",
#     "{{Name}}, wishing you and your loved ones a peaceful, reflective Buddha Purnima.",
#     "This Buddha Purnima, {{Name}}, we simply wish you calm, clarity and quiet joy.",
#     "{{Name}}, for the moments that call for simplicity, our softest pieces are here whenever you need them.",
#     "Wishing you inner peace this Buddha Purnima, {{Name}}. 🙏",
#     "{{Name}}, thank you for being part of our story. Sending you calm and gratitude today.",
#     "May you always walk the path of peace, {{Name}}. Happy Buddha Purnima from [Boutique Name]."
#   ],
  "Independence Day": [
    "Happy Independence Day, {{Name}}! 🇮🇳 Wishing you pride, joy and freedom in everything you do.",
    "{{Name}}, freedom never goes out of style. Celebrate with our new collection, made for the woman who knows her mind.",
    "This Independence Day, {{Name}}, enjoy [X]% off on select styles. Our little way of celebrating you.",
    "{{Name}}, here's to the freedom to choose your own style, always. Happy Independence Day!",
    "Jai Hind, {{Name}}! Wishing you and your family a very Happy Independence Day.",
    "{{Name}}, our Independence Day edit is live: fresh styles, festive spirit. Come take a look.",
    "{{Name}}, celebrate the 15th of August in style. Limited-time offers, only this week.",
    "This Independence Day, {{Name}}, we're celebrating every woman who wears her confidence proudly. That includes you.",
    "{{Name}}, thank you for choosing us on this journey. Happy Independence Day from all of us.",
    "{{Name}}, our Independence Day specials end soon. Don't miss your favourite picks!"
  ],
  "Janmashtami (Vaishnava)": [
    "{{Name}}, wishing you a joyful Janmashtami. May Lord Krishna's blessings fill your home with love. 🦚",
    "Radhe Radhe, {{Name}}! Sending you warm wishes on this beautiful day.",
    "{{Name}}, celebrating Janmashtami with a midnight puja? Our elegant ethnic pieces are perfect for the occasion.",
    "This Janmashtami, {{Name}}, may your life be as colourful and joyful as Krishna's own stories.",
    "{{Name}}, a special Janmashtami collection awaits you at [Boutique Name]. Graceful pieces for a devotional day.",
    "Happy Janmashtami, {{Name}}! Wishing you and your family peace, love and prosperity.",
    "{{Name}}, dress up for the celebrations. New arrivals, made for the occasion.",
    "Jai Shri Krishna, {{Name}}! May this festival bring you closer to all that you love.",
    "{{Name}}, thank you for being part of our journey. Wishing you a beautiful Janmashtami.",
    "{{Name}}, may Krishna's flute bring melody to your life. Happy Janmashtami from [Boutique Name]."
  ],
  "Dussehra": [
    "Happy Dussehra, {{Name}}! 🏹 Wishing you victory over every challenge, today and always.",
    "{{Name}}, Dussehra marks new beginnings. What better way to start than with a new outfit? Explore our collection today.",
    "This Vijayadashami, {{Name}}, they say it's auspicious to buy something new. We have just the pieces for you.",
    "{{Name}}, celebrate the win of good over evil with a look that makes you feel unstoppable. Happy Dussehra!",
    "{{Name}}, our Dussehra collection is here: bold colours, graceful silhouettes, made to celebrate you.",
    "Wishing you strength, courage and joy this Dussehra, {{Name}}. 🙏",
    "{{Name}}, enjoy [X]% off this Dussehra season, because new beginnings deserve a beautiful start.",
    "{{Name}}, may this Dussehra burn away every worry and bring you closer to your dreams.",
    "{{Name}}, only a few days left of our Dussehra specials. Come pick your favourites before they're gone!",
    "Happy Vijayadashami, {{Name}}! Thank you for letting us be part of your celebrations, year after year."
  ],
  "Diwali (Deepavali)": [
    "Dear {{Name}}, wishing you a Diwali as bright and beautiful as you are. May this festival of lights bring joy and new beginnings. ✨",
    "{{Name}}, our new Diwali collection has arrived! Rich colours, fine fabrics and pieces made to make you shine this season. 🪔",
    "{{Name}}, you're invited first! Our Diwali edit opens for our valued customers before anyone else. Come pick your favourites.",
    "{{Name}}, celebrate Diwali in style. Enjoy [X]% off our festive collection, only until [date].",
    "{{Name}}, not sure what to wear this Diwali? Visit us and we'll help you find the perfect look, handpicked for you.",
    "{{Name}}, Diwali is also about gifting the people you love. Looking for something special for your mom, sister or best friend? We have you covered.",
    "{{Name}}, thank you for being part of our journey. This Diwali, we have something special just for you.",
    "{{Name}}, only a few days left for Diwali! If you haven't picked your outfit yet, now's the time.",
    "{{Name}}, Diwali is almost here. Have you found your outfit yet? Let's find the one that makes you feel your best.",
    "{{Name}}, may this Diwali bring you and your family happiness, good health and prosperity. Happy Diwali from [Boutique Name]! 🪔✨"
  ],
  "Guru Nanak's Birthday": [
    "{{Name}}, wishing you a blessed Gurpurab. May Guru Nanak Dev Ji's teachings of love and equality guide us all. 🙏",
    "Happy Guru Nanak Jayanti, {{Name}}! Wishing you and your family peace and happiness.",
    "{{Name}}, visiting the Gurdwara this Gurpurab? Our simple, elegant pieces are perfect for the day.",
    "This Prakash Purab, {{Name}}, may your life be filled with light, humility and kindness.",
    "{{Name}}, wishing you a peaceful and joyful Gurpurab, surrounded by loved ones.",
    "Sat Sri Akal, {{Name}}! Sending you warm wishes on this holy day.",
    "{{Name}}, a small collection of graceful pieces awaits you at [Boutique Name], perfect for the celebrations ahead.",
    "Happy Gurpurab, {{Name}}! May Guru Nanak's blessings stay with you always.",
    "{{Name}}, thank you for being part of our journey. Wishing you a beautiful Gurpurab.",
    "{{Name}}, may this Gurpurab bring you peace, light and togetherness. Warm wishes from [Boutique Name]."
  ],
  "Christmas": [
    "Merry Christmas, {{Name}}! 🎄 Wishing you a season full of warmth, love and sparkle.",
    "{{Name}}, our Christmas collection is here: sequins, velvet and all things festive. Perfect for your celebrations!",
    "{{Name}}, planning your Christmas party look? We've handpicked pieces that will make you shine this season.",
    "This Christmas, {{Name}}, gift yourself something beautiful. You deserve it.",
    "{{Name}}, enjoy [X]% off our festive edit this Christmas. Limited time only!",
    "{{Name}}, looking for the perfect Christmas gift for someone special? Our collection has something for everyone.",
    "Ho Ho Ho, {{Name}}! Wishing you a Merry Christmas filled with joy and beautiful moments.",
    "{{Name}}, our Christmas specials are almost gone. Grab your favourites before they're sold out!",
    "{{Name}}, thank you for making this year special for us. Wishing you a very Merry Christmas.",
    "{{Name}}, may your Christmas be as bright and beautiful as you are. Warm wishes from all of us at [Boutique Name]. 🎄✨"
  ]
}




        

def main():

    global items_xml
    occasions = list(festival_messages.keys()) + ["Birthday"]
    for occasion in occasions:
    
        promptForListGeneration =  """You are an expert AI image-prompt engineer working for a premium, stylish women's fashion boutique.Generate a JSON array of exactly 10 highly detailed image generation prompts for premium {{OCCASION}} greeting visuals, from the perspective of a high-end, stylish women's boutique. Write AI image-generation prompts for festive/occasion greeting posters the boutique sends to customers on WhatsApp and Instagram. These are NOT product ads — they are pure celebratory visuals.

OCCASION: {{OCCASION}}

Write 10 distinct, ready-to-paste AI image-generation prompts for this occasion, following every rule below:

1. AUDIENCE & MOOD: the audience is entirely women. Aim for refined, soft, aspirational "quiet luxury" — like a high-end fashion magazine's festival cover — never festival clip art or a sales flyer.
2. PALETTE & MOTIFS: draw from {{OCCASION}}'s traditional colors and symbols (or, for a Birthday, universal symbols like balloons, ribbon, candles, confetti, cake) — elevated into muted jewel tones, soft pastels and gold/brass accents rather than bright, saturated colors.
3. SUBJECT: object-led and symbolic only — flowers, light, fabric, traditional props, abstract pattern. No boutique products, clothing, mannequins, shopping bags, price tags, logos, or human figures/faces/hands.
4. TEXT: the only text is a short greeting — "Happy {{OCCASION}}," or a natural short equivalent for solemn occasions (e.g. "Om Namah Shivaya" for Maha Shivaratri) — in elegant fine serif or script type, placed with generous negative space. No names, no discounts, no CTAs, no boutique name.
5. COMPOSITION: one complete, full-bleed poster — background, subject, light and text considered together, nothing cropped or unfinished. Square 1:1 unless told otherwise.
6. VARIETY: across the 10, vary composition (flat lay, macro, wide scene, illustration, abstract pattern), palette direction and central motif, while keeping one cohesive visual identity. Mix photographic (soft cinematic light, shallow depth of field) and fine illustration styles.
7. FORMAT: each prompt is ONE flowing paragraph (not bullets), detailed enough to paste straight into an AI image tool — include lighting, mood, palette, composition, and the exact greeting text to render.

Before writing, briefly consider {{OCCASION}}'s traditional palette, symbols and mood — but don't show this thinking.

OUTPUT: only a numbered list, 1–10. No preamble, no explanation."""
        prompt = promptForListGeneration.replace("{{OCCASION}}", occasion)
        promptsList=client.models.generate_content(
            model="gemini-2.5-flash",
            contents= prompt
        )
        
        print("Received response for prompt generation")
        process_response=promptsList.text
    
        startIndex=process_response.index("[")
        lastIndex=process_response.rindex("]")
        prompts=json.loads(process_response[startIndex:lastIndex+1])
        for i in prompts:
            

            api_key="sk_aHtpw0Iv5BvrwjEN9A2BANRXGDzbV47x"
            # This removes all hidden newlines (\n) and tabs that trigger Cloudflare
            clean_prompt = re.sub(r'\s+', ' ', i).strip()
            finalPromptInText=clean_prompt.replace("'", "").replace("-", "").replace(",", "").replace("--ar","").replace("--ar 9:16","").replace("%","percent").replace(".","")

            print(finalPromptInText)
# Now encode it safely
            safe_prompt = urllib.parse.quote(finalPromptInText)
            print(len(safe_prompt))
            random_seed = random.randint(0, 1000000)
            
            image_url = f"https://gen.pollinations.ai/image/{safe_prompt}?width=1080&height=1920&nologo=true&seed={random_seed}&model=flux&key={api_key}"
    
            headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

# Pass the disguise into the request
            response = requests.get(image_url, headers=headers)
            if response.status_code != 200:
                        error_details = "Unknown Error"
                        try:
                            error_details = json.dumps(response.json())
                        except Exception:
                            error_details = response.text
                    
                        print(f"❌ API error: {response.status_code} | {error_details}")
                        continue
                # FIX 2: Use , not return, so it doesn't stop the whole job

                        
    
            filename=f"wallpaper_{random_seed}.jpg"
            with open(filename,"wb") as file:
                    file.write(response.content)
    
            print(f"✅ Image saved as {filename} for prompt: {i}")
            
            
            
            
            
            
main()