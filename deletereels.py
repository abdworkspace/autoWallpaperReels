from playwright.sync_api import sync_playwright
import time
import random

USERNAME = "motivationquoteswale"
TARGET_VIEWS = 200 # Your threshold
reelsToDelete=[]




def deletereels():
    with sync_playwright() as p:
        # Using a headed browser makes debugging easier
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(storage_state="instaAuth3.json")
        page = context.new_page()
        time.sleep(10)
        print("In Delete Functuib")
        page.goto("https://instagram.com",timeout=300000)
        try:
            page.get_by_role("button", name="close").click()
        except:
            print("There Was No Notification Related To Notification")
        try:
            page.get_by_role("button", name="Turn On").click()
        
        except:
            print("There Was No Notification Related To Notification")
        for reelDelete in reelsToDelete:
            print("Deleting reel no 1")
            page.goto(reelDelete,timeout=4000000)
            try:
                page.get_by_role("button", name="More options").click()
            except:
                continue
            time.sleep(random.randint(1,50))
            try:
                page.get_by_role("button", name="Delete").click()
            except:
                continue
            try:
                 page.get_by_role("button", name="Delete").click()
            except:
                continue
            reelsToDelete.remove(reelDelete)
            time.sleep(random.randint(1,50))

def formatingViews(views):
    if "K" in views:
        return int(float(views.replace("K",""))*1000)
    elif "M" in views:
        return int(float(views.replace("M",""))*1000000)
    else:
        return int(views)


def find_low_performing_reels():
    with sync_playwright() as p:
        # Using a headed browser makes debugging easier
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(storage_state="instaAuth3.json")
        page = context.new_page()

        # 1. Navigate to the Reels tab
        print(f"Navigating to {USERNAME}'s reels...")
        page.goto(f"https://www.instagram.com/{USERNAME}/reels/", timeout=6000000)
        try:
            page.get_by_role("button", name="close").click()
        except:
            print("There Was No Notification Related To Notification")
        try:
            page.get_by_role("button", name="Turn On").click()
        
        except:
            print("There Was No Notification Related To Notification")
        time.sleep(10)
        reels= page.locator('a[href*="/reel/"]').all()
        for times in range(20):
            
            for i in reels:    
                href=i.get_attribute("href")
                text=i.inner_text().replace(",","")
                fullUrl=f"https://instagram.com{href}"
                if formatingViews(text)<TARGET_VIEWS and fullUrl not in reelsToDelete:
                    reelsToDelete.append(fullUrl)
                    print(fullUrl)
            for scrollCount in range(3):
                page.keyboard.press("PageDown")
                time.sleep(random.randint(1,10))
        print("running the delete function scrolled")
        print(reelsToDelete)
    deletereels()
    print("deleted all the reels")
    time.sleep(20)

            
    
    
find_low_performing_reels()