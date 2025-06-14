from playwright.sync_api import sync_playwright

def test_visit_example():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/docs")  
        assert "FastAPI - " in page.title()
        browser.close()

def test_post_endpoint_visible():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/docs")
        visible_text = page.locator("body").inner_text()
        assert "/items/" in visible_text
        assert "POST" in visible_text
        browser.close()


def test_create_item_through_swagger_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/docs")
        page.get_by_role("button", name="POST /items/").nth(0).click()
        page.get_by_role("button", name="Try it out").nth(0).click()
        json_payload = '''{
        "id": 1,
        "name": "Cup",
        "description": "Hand-painted cup",
        "price": 15.99
        }'''
        page.locator("textarea").fill(json_payload)
        page.get_by_role("button", name="Execute").nth(0).click()
        page.wait_for_selector(".responses-wrapper")
        response_text = page.locator(".responses-wrapper").inner_text()
        assert "200" in response_text
        assert "Cup" in response_text

def test_read_items():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/docs")
        page.get_by_role("button", name="GET /items/").nth(0).click()
        page.get_by_role("button", name="Try it out").nth(0).click()
        page.get_by_role("button", name="Execute").nth(0).click()
        page.wait_for_selector(".responses-wrapper")
        response_text = page.locator(".responses-wrapper").inner_text()
        assert "200" in response_text
        assert "Cup" in response_text 
        browser.close()

def test_update_item():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/docs")
        page.get_by_role("button", name="PUT /items/{item_id}").nth(0).click()
        page.get_by_role("button", name="Try it out").nth(0).click()
        page.locator("input[placeholder='item_id']").fill("1")
        json_payload = '''{
        "id": 1,
        "name": "Cup",
        "description": "Hand-painted ceramic cup",
        "price": 19.99
        }'''
        page.locator("textarea").fill(json_payload)
        page.get_by_role("button", name="Execute").nth(0).click()
        page.wait_for_selector(".responses-wrapper")
        response_text = page.locator(".responses-wrapper").inner_text()
        assert "200" in response_text
        assert "ceramic" in response_text
        browser.close()

def test_delete_item():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/docs")
        page.get_by_role("button", name="DELETE /items/{item_id}").nth(0).click()
        page.get_by_role("button", name="Try it out").nth(0).click()
        page.locator("input[placeholder='item_id']").fill("1")
        page.get_by_role("button", name="Execute").nth(0).click()
        page.wait_for_selector(".responses-wrapper")
        assert "200" in page.locator(".responses-wrapper").inner_text()
        browser.close()

def test_delete_non_existent_item():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/docs")
        page.get_by_role("button", name="DELETE /items/{item_id}").nth(0).click()
        page.get_by_role("button", name="Try it out").nth(0).click()
        page.locator("input[placeholder='item_id']").fill("999") 
        page.get_by_role("button", name="Execute").nth(0).click()
        page.wait_for_selector(".responses-wrapper")
        response_text = page.locator(".responses-wrapper").inner_text()
        assert "404" in response_text
        assert "Item not found" in response_text
        browser.close()