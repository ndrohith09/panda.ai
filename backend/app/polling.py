import asyncio
from httpx import AsyncClient 

# TODO: check func
async def poll_endpoint(url: str, interval: int):
    async with AsyncClient() as client:
        while True:
            try:
                response = await client.get(url)
                # Process the response as needed
                print(f"Status: {response.status_code}, Response: {response.json()}")
                
                create_logs = await client.post('http://localhost:8000/logs/create' , {
                    "pipeline_id" : response.pipeline_id,
                    "log_id" : response.log_id,
                    "error_log" : response.error_log,
                })               
                print("create_logs",create_logs)  
            except Exception as e:
                print(f"Error polling {url}: {e}")
            await asyncio.sleep(interval)  # Wait before the next poll
