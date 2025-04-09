import abc
import asyncio
import httpx


class ResultsObserver(abc.ABC):
    @abc.abstractmethod
    def observe(self, data: bytes) -> None: ...


async def do_reliable_request(url: str, observer: ResultsObserver) -> None:
    """
    Одна из главных проблем распределённых систем - это ненадёжность связи.

    Ваша задача заключается в том, чтобы таким образом исправить этот код, чтобы он
    умел переживать возвраты ошибок и таймауты со стороны сервера, гарантируя
    успешный запрос (в реальной жизни такая гарантия невозможна, но мы чуть упростим себе задачу).

    Все успешно полученные результаты должны регистрироваться с помощью обсёрвера.
    """

    async with httpx.AsyncClient(timeout=10.0) as client:
        # YOUR CODE GOES HERE
        retries = 5
        retries_delay = 2
        exceptions = (httpx.HTTPStatusError, httpx.RequestError, httpx.TimeoutException)

        for attempt in range(retries):
            try:
                response = await client.get(url)
                response.raise_for_status()
                data = response.read()

                observer.observe(data)
                return

            except exceptions as exception:
                if attempt < retries - 1:
                    await asyncio.sleep(retries_delay)
                else:
                    raise Exception(
                        f"Request failed after {retries} attempts: {exception}"
                    )
        #####################
