import pytest
from src.scraping.selenium_config import SeleniumBrowser

@pytest.fixture
def browser():
    b = SeleniumBrowser(headless=True)
    driver = b.create_browser()
    yield driver  # passa o driver para o teste
    b.close_browser(driver)  # fecha no final do teste

def test_initialization(browser):
    assert browser is not None # Valida inicialização do browser

def test_navigation(browser):
    browser.get("https://www.google.com") # Valida se navegação é funcional
    assert "Google" in browser.title
