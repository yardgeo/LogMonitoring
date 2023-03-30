import asyncio


async def test(i):
    for j in range(2, 5):
        print(i ** j)


async def main():
    for i in range(2, 6):
        print(i)
        test(i)


loop = asyncio.get_event_loop()

# run all services in parallel
loop.run_until_complete(
    main()
)
