from playwright.sync_api import Page

class HighlightManager:
    def __init__(self , page:Page):
        self.page = page;

    def highlight_element(self , element):
        """Highlight the element by adding a border"""

        element.evaluate("""
        el => {
        const box = el.getBoundingClientRect();
        el.style.outline = '3px solid ' + (box.width > 200 ? 'red' : 'green');
        el.style.outlineOffset = '2px';
        el.style.transition = 'outline 0.3s ease';
        }
        """)

    def enhanced_query_selector(self , selector: str):
        print(f"Using query selector")
        element = self.page.query_selector(selector);
        if element:
            self.highlight_element(element)
        return element

    def enhanced_locator(self , selector: str):
        print(f"using locator")
        element = self.page.locator(selector)
        if element:
            self.highlight_element(element)
        return element   

    def enhanced_text(self , text: str , exact = False):

        element = self.page.get_by_text(text , exact=exact)
        if element:
            self.highlight_element(element)
        return element 

