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
  "republicday": [
    "Good morning {{Name}}! Wishing you a very Happy Republic Day. Here's to celebrating the spirit of our nation, today and always. 🇮🇳",
    "{{Name}}, this Republic Day, we have something special waiting for you. Visit us and discover pieces that celebrate every woman's pride.",
    "Happy Republic Day, {{Name}}! Enjoy [X]% off on select pieces at [Boutique Name], because you deserve to feel special too.",
    "{{Name}}, freedom looks good on you. Explore our new arrivals this Republic Day and pick a look that's truly yours.",
    "This Republic Day, {{Name}}, we're celebrating every woman who stands tall in her own way. Come treat yourself to something beautiful.",
    "{{Name}}, our Republic Day edit is here. Limited pieces, timeless style. Visit us before your favourites are gone.",
    "Happy Republic Day, {{Name}}! May you always wear your confidence as beautifully as you wear our outfits. 🇮🇳",
    "{{Name}}, celebrate the tricolour spirit with us. Special prices, only for a few days.",
    "On this special day, {{Name}}, we're grateful to have you with us. Thank you for your trust and support.",
    "{{Name}}, last day of our Republic Day specials! Don't miss your chance to shop your favourites."
  ],
  "Maha Shivaratri": [
    "{{Name}}, wishing you peace and blessings this Maha Shivaratri. May Lord Shiva bless you with strength and serenity. 🙏",
    "Har Har Mahadev, {{Name}}! Sending you warm wishes on this sacred night.",
    "{{Name}}, for your Maha Shivaratri puja, we have a small collection of simple, elegant pieces. Do take a look.",
    "This Maha Shivaratri, {{Name}}, may all your prayers be answered. Wishing you calm and countless blessings.",
    "{{Name}}, heading to the temple this Maha Shivaratri? Our soft cotton sarees make for a comfortable, graceful choice.",
    "Wishing you a blessed Maha Shivaratri, {{Name}}. May this sacred day bring positivity into your life.",
    "{{Name}}, some occasions call for simplicity. Our understated ethnic pieces are made for days like this.",
    "Om Namah Shivaya, {{Name}}. Sending you warmth and good wishes on this holy night.",
    "{{Name}}, thank you for being part of our family. On this Maha Shivaratri, we wish you peace and wellbeing.",
    "{{Name}}, may Lord Shiva's blessings stay with you always. Happy Maha Shivaratri from [Boutique Name]."
  ],
  "Holi": [
    "Happy Holi, {{Name}}! 🌈 Wishing you a festival full of colour, laughter and beautiful memories.",
    "{{Name}}, Holi calls for colour, and so does your wardrobe. Check out our vibrant new collection made for the season.",
    "{{Name}}, planning a Holi brunch or get-together? Our pastel and white co-ord sets are perfect for looking effortlessly pretty.",
    "This Holi, {{Name}}, add a splash of colour to your closet. New arrivals now in store!",
    "{{Name}}, celebrate Holi in style! Enjoy [X]% off our festive collection, for a few days only.",
    "Holi Hai, {{Name}}! 🎉 May your life always be as colourful and joyful as this beautiful festival.",
    "{{Name}}, once the colours settle, it's time to dress up. Our post-Holi party wear collection is here.",
    "{{Name}}, we handpicked a few pieces just for you this Holi. Come see what caught our eye.",
    "Wishing you and your loved ones a very Happy Holi, {{Name}}. May this festival bring joy that lasts all year.",
    "{{Name}}, our Holi specials end soon. Grab your favourite colourful pieces before they're gone."
  ],
  "Ram Navami": [
    "{{Name}}, wishing you a blessed Ram Navami. May Lord Rama's blessings bring peace to your home. 🙏",
    "Jai Shri Ram, {{Name}}! Sending you warm wishes on this auspicious day.",
    "{{Name}}, celebrating Ram Navami with a puja or temple visit? Our elegant traditional wear is perfect for the occasion.",
    "This Ram Navami, {{Name}}, may your life be filled with truth, courage and devotion.",
    "{{Name}}, a small, thoughtful collection for Ram Navami is now at [Boutique Name]. Simple, graceful pieces for a special day.",
    "Wishing you and your family a peaceful Ram Navami, {{Name}}. 🙏",
    "{{Name}}, some days call for quiet elegance. Explore pieces made for occasions like this.",
    "Happy Ram Navami, {{Name}}! May this day bring you closer to everything good in life.",
    "{{Name}}, thank you for trusting us with your special moments. Wishing you a blessed Ram Navami.",
    "{{Name}}, may Lord Rama's blessings be with you always. Happy Ram Navami from [Boutique Name]."
  ],
  "Buddha Purnima": [
    "{{Name}}, wishing you peace, light and wisdom this Buddha Purnima. 🙏",
    "On this Buddha Purnima, {{Name}}, may you find a moment of calm in your busy life.",
    "{{Name}}, Lord Buddha taught us that true beauty comes from within. Wishing you peace on this sacred day.",
    "May the light of wisdom guide you always, {{Name}}. Happy Buddha Purnima.",
    "{{Name}}, wishing you and your loved ones a peaceful, reflective Buddha Purnima.",
    "This Buddha Purnima, {{Name}}, we simply wish you calm, clarity and quiet joy.",
    "{{Name}}, for the moments that call for simplicity, our softest pieces are here whenever you need them.",
    "Wishing you inner peace this Buddha Purnima, {{Name}}. 🙏",
    "{{Name}}, thank you for being part of our story. Sending you calm and gratitude today.",
    "May you always walk the path of peace, {{Name}}. Happy Buddha Purnima from [Boutique Name]."
  ],
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
    
        promptForListGeneration =  """Generate a JSON array of exactly 10 highly detailed image generation prompts for premium {{OCCASION}} greeting visuals, from the perspective of a high-end, stylish women's boutique.

    Aesthetic & Art Style: Emulate a premium greeting-card / editorial-poster aesthetic — fine-line illustration, a soft watercolour wash, delicate flat vector art, or a smooth minimalist gradient backdrop. DO NOT use photorealism, 3D render, stock-photo style, heavy texture, or cluttered scenes. Every image must feel elegant, breathable, and boutique-grade, built around generous negative space. Let the colour palette reflect the mood of {{OCCASION}} (e.g. warm gold and maroon for Diwali, soft pastels for Holi, deep green and red for Christmas, blush and cream for a birthday) but always refined and tasteful, never garish or novelty-looking.

    Motif & Composition: Choose ONE small, symbolic motif tied to {{OCCASION}} (a single diya, a sprig of marigold, a wisp of colour powder, a snowflake, a lit candle, a curl of ribbon, a lotus, a strand of fairy lights, a few confetti flecks, etc.) and place it with deliberate, elegant asymmetry — never centred, crowded, or busy. CRITICAL — DO NOT include any of the following: clothing, garments, mannequins, models, human faces or bodies, shopping bags, store interiors, logos, price tags, or any literal product. This is about mood and feeling, not merchandise — keep every scene plain, simple, and uncluttered.

    Typography & Text (CRITICAL — MINIMAL, NO NAMES): Most of the 10 images should carry NO text at all. Where text does appear, it must be a single short greeting of no more than 4 words (e.g. "Happy Diwali," "Shubh Holi," "Cheers To You") in elegant serif or fine script typography, tucked into the negative space. NEVER render a personal name, the placeholder {{Name}}, a boutique or brand name, a discount, or an offer — every image must stay generic enough to reuse for any customer.

    Variety (NO REPEATS): To keep the 10 images visually distinct from one another, generate them using this exact sequence of visual treatments:
    1. Macro close-up of the single motif, extreme negative space
    2. Wide, airy scene with the motif small in one corner
    3. Abstract repeating pattern derived from the motif, subtle and soft
    4. Fine-line botanical/linear illustration style
    5. Soft watercolour wash background, no hard edges
    6. Delicate flat-lay arrangement of 2-3 symbolic (non-product) objects
    7. Smooth solid-to-gradient colour field with a single tiny motif
    8. Fine gold or metallic linework on a muted background
    9. Soft pastel, dreamy, out-of-focus mood shot
    10. Bold, graphic, jewel-tone poster composition

    For each of the 10 prompts, briefly specify the exact colour palette, and — only where text is used — the typography style and colour, so it stays crisp and legible against the background.

    Format Rules: Return ONLY a valid JSON array of strings, formatted exactly like this: ["detailed prompt 1", "detailed prompt 2"]. Do NOT wrap the array in objects, do NOT include markdown formatting like ```json, and do NOT include any conversational text.

    Within each string, end with technical tags like: --ar 9:16, premium greeting card design, minimalist boutique campaign, elegant negative space, soft studio lighting, flawless typography, crisp clean linework, 8k resolution, no logos, no clutter."""
        prompt = promptForListGeneration.replace("{{OCCASION}}", occasion)
        promptsList=client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents= prompt
        )
        
        print("Received response for prompt generation")
        
        process_response=promptsList.text
    
        startIndex=process_response.index("[")
        lastIndex=process_response.rindex("]")
        prompts=json.loads(process_response[startIndex:lastIndex+1])



    with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            
            context = browser.new_context(storage_state="oldinstaAuth3.json", color_scheme="dark")
            stealth=Stealth()
            stealth.apply_stealth_sync(context)
            page = context.new_page()
    
            listOfAllBlogs=requests.get("https://techvridha.vercel.app/getlistofallblogs")
            text=listOfAllBlogs.json()
            for i in prompts:
                captionsToFill=f'''New Blog Available At https://techvridha.vercel.app/ {(random.choice(text["listofallBlogs"]))["description"]}'''


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
        
                print(f"✅ Image saved as {filename} for prompt: {i}")
 # 10s rate limit protection

                
                # Pintrest Work 

                # 
                # 
                # 
                # 
                # 
                # 
                # 

                # 
                # 
                # 
                # 

# Save images with the date in the filename
                # FIX 1: Correct the datetime call based on your imports
                today = datetime.now().strftime("%Y-%m-%d")
                
                # FIX 2: Create a unique ID for this specific image
                unique_id = f"wallpaper_{today}_{prompts.index(i)}"
                filenameforpintrest = f"{unique_id}.jpg"
                filenameForPintrestFeed = os.path.join("wallpaper", filenameforpintrest)

                # FIX 3: Update the URL to point to today's uniquely named file, not the old static ones
                img_url = f"{RAW_IMG_BASE}{filenameforpintrest}"
                
                # FIX 4: Add the GUID, unique link anchor, and image/jpeg type
                items_xml += f"""<item>
      <title>{captionsToFill}</title>
      <link>{SITE_URL}#{unique_id}</link>
      <guid isPermaLink="false">techvridha_{unique_id}</guid>
      <description>High quality wallpaper: {i.replace("--ar 9:16","").replace("dalle","")}</description>
      <pubDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</pubDate>
      <media:content url="{img_url}" medium="image" type="image/jpeg" />
    </item>"""

                
                with open(filename,"wb") as file:
                    file.write(response.content)
                with open(filenameForPintrestFeed,"wb") as file:
                    file.write(response.content)
                

                
                video_filename=f"wallpaper_{random_seed}.mp4"
                
                audio_path="wallpaper.mp3"

                intro_file="intro.png"
                phone_profiles = [
        {"make": "Apple", "model": "iPhone 15 Pro", "software": "17.4.1"},
        {"make": "Apple", "model": "iPhone 14 Pro Max", "software": "17.3"},
        {"make": "Apple", "model": "iPhone 13", "software": "16.6"},
        {"make": "Samsung", "model": "SM-S918B", "software": "Android 14"}, # S23 Ultra
        {"make": "Google", "model": "Pixel 8 Pro", "software": "Android 14"}
    ]
    
                device = random.choice(phone_profiles)

    # 2. Generate a fake recording time (e.g., recorded somewhere between 5 to 120 minutes ago)
                minutes_ago = random.randint(5, 120)
                fake_time = (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).strftime('%Y-%m-%dT%H:%M:%S.000000Z')

                a=str({random.randint(1, 3)}) 
                ffmpeg_cmd = [
    'ffmpeg',
    '-y',
    '-loop', '1',
    '-t', '3',
    '-i', filename,
    '-i', audio_path,
    '-filter_complex', '[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v]',
    '-map', '[v]',
    '-map', '1:a',
    '-metadata', f'creation_time={fake_time}',
        '-metadata', f'make={device["make"]}',
        '-metadata', f'model={device["model"]}',
        '-metadata', f'software={device["software"]}',
        '-metadata', 'encoder=Lavf59.27.100',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-r', '30',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    video_filename
]
                try:
                    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                    print(f"✅ Video created successfully: {video_filename}")
                    # Update upload_file to the video
                    upload_file = os.path.abspath(filename)
                except subprocess.CalledProcessError as e:
                    print(f"❌ FFmpeg failed: {e}")
                    upload_file = os.path.abspath(filename) # Fallback to image if video fails
            
                page.goto("https://www.instagram.com/",timeout=400000)
                # time.sleep(20)
                print("Waiting For Some Time")
        


                try:
                    page.get_by_role("button", name="close").click()
                except:
                    print("There Was No Notification Related To Notification")
                try:
                    page.get_by_role("button", name="Turn On").click()
        
                except:
                    print("There Was No Notification Related To Notification")
                
            

                try:
                
                    page.get_by_role("button", name="close").hover()
                    time.sleep(random.uniform(0,5.9))
                    page.get_by_role("button", name="close").click()
                except:
                    print("There Was No Notification Related To Notification")
                try:
                    
                    page.get_by_role("button", name="Turn On").hover()
                    time.sleep(random.uniform(0,5.9))
                    page.get_by_role("button", name="Turn On").click()
                
                except:
                    print("There Was No Notification Related To Notification")


                    
             
                try:
                    page.get_by_role("link", name="New post").hover()
                    time.sleep(random.uniform(3.5, 7.2)) # For standard button clicks

                    print("Clicked On New Post")
                except Exception as e:
                    print(f"Error clicking New post: {e}")
        
                try:
                    
                    clickonCreate = page.get_by_role("link", name="New post Create").hover()
                    time.sleep(random.uniform(0,5.9))
                    clickonCreate = page.get_by_role("link", name="New post Create").click()
                    time.sleep(random.uniform(5.5, 12.0))
                    print("Clicked New post Create")
                except Exception as e:
                    print(f"Error clicking New post Create: {e}")
                    

                try:
                    
                    clickOnCreatePost = page.get_by_role("link", name="Post Post").hover()
                    time.sleep(random.uniform(0,5.9))
                    clickOnCreatePost = page.get_by_role("link", name="Post Post").click()
                    time.sleep(random.uniform(3.5, 7.2)) # For standard button clicks

                    print("Clicked Post Post")
                except Exception as e:
                    print(f"Error clicking Post Post: {e}")
                    

                try:
                    with page.expect_file_chooser() as fc_info:
                        
                        page.get_by_role("button", name="Select from computer").hover()
                        time.sleep(random.uniform(0,5.9))
                        page.get_by_role("button", name="Select from computer").click()
                        time.sleep(random.uniform(5.5, 12.0))
                    file_chooser = fc_info.value
                    file_chooser.set_files(video_filename)
                    print(f"Selected file {video_filename}")
                except Exception as e:
                    print(f"Error selecting file: {e}")
                    

                try:
                    if prompts.index(i)==0:
                        
                        clickingOnOk = page.get_by_role("button", name="OK").hover()
                        time.sleep(random.uniform(0,5.9))
                        clickingOnOk = page.get_by_role("button", name="OK").click()
                        time.sleep(random.uniform(3.5, 7.2)) # For standard button clicks

                        print("Clicked OK")
                except Exception as e:
                    print(f"Error clicking OK: {e}")
                    

                try:
                    
                    clickingOnCrop = page.locator("button").filter(has_text="Select crop").hover()
                    time.sleep(random.uniform(0,5.9))
                    clickingOnCrop = page.locator("button").filter(has_text="Select crop").click()
        
                    time.sleep(random.uniform(5.5, 12.0))
                    print("Clicked Select crop")
                except Exception as e:
                    print(f"Error clicking Select crop: {e}")
                    

                try:
                    
                    clickingonOriginalSize =  page.get_by_role("button", name="Original Photo outline icon").hover()
                    time.sleep(random.uniform(0,5.9))
                    clickingonOriginalSize =  page.get_by_role("button", name="Original Photo outline icon").click()
                    time.sleep(random.uniform(3.5, 7.2)) # For standard button clicks

                    print("Clicked Original size")
                except Exception as e:
                    print(f"Error clicking Original size: {e}")
                    

                try:
                    
                    clickingonNext = page.locator("div").filter(has_text=re.compile(r"^Next$")).nth(1).hover()
                    time.sleep(random.uniform(0,5.9))
                    clickingonNext = page.locator("div").filter(has_text=re.compile(r"^Next$")).nth(1).click()
                    time.sleep(random.uniform(5.5, 12.0))
                    print("Clicked Next (first)")
                except Exception as e:
                    print(f"Error clicking Next (first): {e}")
                    

                try:
                    
                    clickingOnAnotherNext = page.locator("div").filter(has_text=re.compile(r"^Next$")).nth(1).hover()
                    time.sleep(random.uniform(0,5.9))
                    clickingOnAnotherNext = page.locator("div").filter(has_text=re.compile(r"^Next$")).nth(1).click()
                    time.sleep(random.uniform(3.5, 7.2)) # For standard button clicks

                    print("Clicked Next (second)")
                except Exception as e:
                    print(f"Error clicking Next (second): {e}")
                    

                try:
                    captions = page.get_by_role("textbox", name="Write a caption...")
                    time.sleep(random.uniform(5.5, 12.0))
                    
                    captions.hover()
                    time.sleep(random.uniform(0,5.9))
                    captions.click()
                    captions.type(captionsToFill, delay=random.randint(50, 150))
                    print("Inserted caption")
                except Exception as e:
                    print(f"Error writing caption: {e}")
                    

                try:
                    
                    clickingOnShareButton = page.get_by_role("button", name="Share", exact=True).hover()
                    time.sleep(random.uniform(0,5.9))
                    clickingOnShareButton = page.get_by_role("button", name="Share", exact=True).click()
                    
                    time.sleep(random.uniform(5.5, 12.0))
                    print("Clicked Share")
                except Exception as e:
                    print(f"Error clicking Share: {e}")
                                

                # 2. Wait dynamically for the upload to finish (up to 4 minutes)
                try:
                    # Instagram shows this exact text when the upload is truly finished.
                    # We give it 240,000 milliseconds (4 minutes) to appear.
                    page.locator("text=Your reel has been shared.").wait_for(timeout=300000)
                    print("✅ Upload confirmed by Instagram!")
                    os.remove(video_filename)
                    try:
                        reelClose=page.get_by_role("button", name="Close")
                        
                        reelClose.hover()
                        time.sleep(random.uniform(0,5.9))
                        reelClose.click()
                        time.sleep(random.uniform(3.5, 7.2)) # For standard button clicks

                        page.goto("https://instagram.com")
                        print("Went TO Instagram")
                        print("Reel Uploaded SuccessFully")
                        time.sleep(random.uniform(3.5, 7.2)) # For standard button clicks

                    except:
                    
                        print("Unable To Find CLose Button")
                except Exception as e:
                    print("❌ Timeout waiting for success message. It took too long or failed.")
                    page.reload() # Refresh to clear the stuck upload screen
                     #
                time.sleep(random.randint(9,30))
                
                time.sleep(5)
                print("Navigating Back To Instgarm")
              
                time.sleep(random.randint(1,5))
                 #
        


 # Run the whole process 3 times


try:
    main()
except Exception as e:
    print(f"Error Occured In Making Images And UploadingTO Instagram: {e}")
# --- NEW: ROLLING FEED LOGIC ---
existing_items = ""
try:
    # Read the current feed to grab old items
    with open("feed.xml", "r", encoding="utf-8") as f:
        content = f.read()
        # Find all existing <item> blocks using regex
        matches = re.findall(r'<item>.*?</item>', content, re.DOTALL)
        # Keep only the newest 40 old items (so with today's 10, we have 50 total)
        existing_items = "\n".join(matches[:40])
except FileNotFoundError:
    # If feed.xml doesn't exist yet, just 
    pass

# Combine today's items (items_xml) with the old items (existing_items)
full_rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:content="http://purl.org/rss/1.0/modules/content/">
    <channel>
    <title>TechVridha.vercel.app Wallpapers</title>
    <link>{SITE_URL}</link>
    <description>Latest high-quality wallpapers batch.</description>
    {items_xml}
    {existing_items}
    </channel>
</rss>"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(full_rss)

try:
    commit_msg = f"Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git","add","."],check=True)
    subprocess.run(["git","commit","-m",commit_msg],check=True)
    subprocess.run(["git","push","origin","main"],check=True)
    print("Successfully pushed to GitHub!")

except Exception as e:
    print(e)