import re
import json
from socket import timeout
from playwright.sync_api import Page, expect

payload = '{"title": "Lorem Ipsum", "completed": false}'
data = json.loads(payload)


def test_hit_post_request(page: Page):
    page.goto("https://reqres.in/")

    # Expect a title "to contain" a substring.
    expect(page.get_by_text(re.compile("A real backend you"))).to_be_visible()

    # Expect a reqres-terminal to be visible
    expect(page.get_by_text(re.compile("reqres-terminal"))).to_be_visible()

    # Ensure the Boot is done
    expect(page.get_by_test_id("bootSequence")).not_to_be_visible()

    # Click POST request button
    page.get_by_role("button", name="POST").click()

    # Ensure the button is active
    expect(page.get_by_role("button", name="POST")).to_have_class(re.compile("active"))

    # Innput the payload
    page.locator(".code-editor-textarea").fill(payload)

    # Click The Send Button
    page.get_by_role("button", name="Send").click()

    # Check the response status code
    expect(page.locator("#responseStatus")).to_contain_text("201 Created")

    # Check the response Body
    parentLocator = page.locator("#responseBody")
    idProperty = parentLocator.locator('.json-string:right-of(:text("id"))').first
    titleProperty = parentLocator.locator('.json-string:right-of(:text("title"))').first
    completedProperty = parentLocator.locator(
        '.json-boolean:right-of(:text("completed"))'
    ).first
    # Assert the Response
    print(f"HAHAHA >>> {data['title']}")
    expect(idProperty).to_be_visible()
    expect(titleProperty).to_contain_text(str(data["title"]))
    expect(completedProperty).to_contain_text(str(data["completed"]), ignore_case=True)

