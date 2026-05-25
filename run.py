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
SITE_URL = "https://abdbaap.github.io/AutoWallPaper/" 
# The base URL for your raw images on GitHub
RAW_IMG_BASE = "https://abdbaap.github.io/AutoWallPaper/wallpaper/"


# for file in os.listdir("wallsa

client=genai.Client(api_key=os.getenv("GENAI_API_KEY"))
print("Client Initialized")




        

def main():


    global items_xml
    promptForListGeneration = """Generate a JSON array of exactly 10 highly detailed image generation prompts for vertical mobile wallpapers.

Aesthetic & Art Style: Emulate high-end, clean minimalist typography posters. Use flat vector illustrations, smooth cel-shaded anime styles, or stark silhouettes. DO NOT use hyper-realism, 3D, messy textures, or cluttered backgrounds. Focus on massive negative space. The background must be either a bold solid color, a smooth subtle gradient, or a very stripped-down minimalist environment (e.g., a lone mountain, a quiet empty road, or a field of grass).

Character & Composition: Re-imagine iconic characters (Shinchan, Doraemon, Ash Ketchum) or badass archetypes (Samurai, Bikers, Streetwear icons) in a disciplined, streetwear, or stoic aesthetic. The character must be placed in the lower half of the image. CRITICAL: The character's height MUST NOT exceed 40% of the total vertical canvas, leaving the top half completely empty for text. Maintain extremely clean, sharp, professional lines with no glitches.

Typography & Quotes (CRITICAL - NO REPEATS): Each prompt must specifically describe a unique, punchy quote integrated clearly into the upper negative space. To prevent the AI from generating the same generic quotes over and over, you MUST derive the 10 quotes using this exact sequence of themes:
1. Japanese Zen proverb
2. Modern streetwear/hypebeast one-liner
3. Ancient Stoicism (Marcus Aurelius/Seneca vibe)
4. Cyberpunk/Futuristic grit
5. Minimalist focus/mindfulness
6. Hardcore Hustle/Discipline
7. Humorous/Chill vibe (e.g., "Peace Bro")
8. Warrior/Samurai ethos
9. Urban street poetry
10. Abstract one-word motivation

For each quote, describe the exact font style (e.g., bold sans-serif, rough brush script, elegant minimal serif) and text color to ensure it contrasts perfectly with the clean background.

Format Rules: Return ONLY a valid JSON array of strings formatted exactly like this: ["detailed prompt 1", "detailed prompt 2"]. Do NOT wrap the array in objects, do NOT include markdown formatting like ```json, and do NOT include any conversational text. 

Within each string, end with technical tags like: --ar 9:16, masterpiece, 8k resolution, minimalist poster design, crisp typography, clean solid background, flawless text rendering, vector art style, negative space."""
    promptsList=client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents= promptForListGeneration
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
                
                image_url = f"https://gen.pollinations.ai/image/{safe_prompt}?width=1080&height=1920&nologo=true&seed={random_seed}&model=zimage&key={api_key}"
        
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
    '-map_metadata', '-1',
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
except:
    print("Error Occured In Making Images And UploadingTO Instagram")
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