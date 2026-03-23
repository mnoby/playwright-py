import json
from socket import timeout
from turtle import home
from playwright.sync_api import Page, expect
from pages.reqres_home_page import HomePage

payload = '{"title": "Lorem Ipsum", "completed": false}'
data = json.loads(payload)


def test_hit_post_request(page: Page):
    home_page = HomePage(page)
    page.goto("https://reqres.in/")

    # Verify the Application is ready.
    home_page.is_page_and_API_ready()
    
    # Click POST request button
    home_page.click_post_button("active")

    # Input the payload
    home_page.send_post_request(payload) 
    page.wait_for_timeout(20000)

    # Assert the Response
    home_page.is_response_ok("201 Created", payload)

