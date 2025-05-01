from playwright.sync_api import sync_playwright
from highlight import HighlightManager
import time

# def highlight_element(page, selector):
#     page.eval_on_selector(selector , '''
#     el => {
#     const box = el.getBoundingClientRect();

#     const outline = document.createElement('div');
#     outline.style.position = 'absolute';
#     outline.style.top = box.top + window.scrollY + 'px';
#     outline.style.left = box.left + window.scrollX + 'px';
#     outline.style.width = box.width + 'px';
#     outline.style.height = box.height + 'px';
#     outline.style.border = '2px solid ' + (box.width > 100 ? 'red' : 'green');
#     outline.style.zIndex = 9999;
#     outline.style.pointerEvents = 'none';
#     document.body.appendChild(outline);
#     }
#     ''')

def highlight_element(page, selector):
    page.eval_on_selector(selector , """
    
    el => {
    const box = el.getBoundingClientRect();
    const width = box.width;

    el.style.outline = '3px solid ' + (width > 200 ? 'red' : 'green');
    el.style.outlineOffset = '2px';
    el.style.transition = 'outline 0.3s ease'; 
    }
    
    """)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
        context = browser.new_context()
        page = context.new_page()


        page.goto("https://example.com")

        # using highlight manager 
        highlight_manager = HighlightManager(page)

        more = highlight_manager.enhanced_text("More Information...")

        time.sleep(3)

        more.click()

        time.sleep(2)

        element = highlight_manager.enhanced_query_selector("//div[@id='logo']")

        highlight_manager.enhanced_locator("//div[@class='help-article']")

        # highlight_element(page , "h1")


        page.wait_for_timeout(10000)

        browser.close()

if __name__ == "__main__":
    main()        


