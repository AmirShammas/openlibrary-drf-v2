import asyncio
import aiohttp
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from asgiref.sync import sync_to_async

from .handler import ScraperHandler
from .models import Book, Author
from .constants import SEARCH_PAGE_COUNT, SEARCH_SUBJECT, SEARCH_URL


class ScraperView(APIView):
    async def fetch_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def scrape_page(self, search_subject, page_number):
        url = SEARCH_URL.format(search_subject=search_subject, page_number=page_number)
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_page(session, url)
            soup = BeautifulSoup(html, "html.parser")
            book_titles, book_urls = ScraperHandler.get_book_title(soup)
            authors_names, authors_urls = ScraperHandler.get_book_author(soup)
            book_covers = ScraperHandler.get_book_cover(soup)

            for title, url, cover, author_name, author_url in zip(book_titles, book_urls, book_covers, authors_names, authors_urls):
                author, _ = await sync_to_async(Author.objects.get_or_create)(name=author_name, url=author_url)
                book = await sync_to_async(Book.objects.create)(title=title, url=url, cover=cover, author=author)

    async def scrape_pages(self, search_subject, search_page_count):
        tasks = []
        print("Scraping... !! Please wait... !!")
        for page_number in range(1, search_page_count + 1):
            task = asyncio.create_task(
                self.scrape_page(search_subject, page_number))
            tasks.append(task)
        await asyncio.gather(*tasks)
        print("Done !!")

    def post(self, request):
        search_subject = request.data.get('search_subject', SEARCH_SUBJECT)
        search_page_count = int(request.data.get(
            'search_page_count', SEARCH_PAGE_COUNT))
        asyncio.run(self.scrape_pages(search_subject, search_page_count))
        return Response({"message": "Scraping completed successfully !!"})
