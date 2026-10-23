# This code practices async and executors both at the same time
# Note: both executors and asyncio is not working parallely to make it smiple
# but the contnent inside them is running parallely
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import asyncio
import time
def download(item):
    time.sleep(item)
    return f"Job Downloading: Success"
async def file(item):
    await asyncio.sleep(item)
    return f"Job File: Success"
def calculation(item):
    time.sleep(item)
    return f"Job Calculation: Success"
async def slow_request(item):
    try:
        await asyncio.sleep(item)
        return f"Job Slow_request: Success"
    except:
        return f"Job Slow_request: TIMEOUT"
 
class Main:
    def __init__(self):
        self.All_jobs = []
        self.results = []
    def add_job(self):
        job_name = input("Enter Job name: ")
        duration = int(input("Enter Duration: "))
        self.All_jobs.append((job_name,duration))
    def View_queue(self):
        for item in self.All_jobs:
            print(f"Job Name: {item[0]}\nJob Duration: {item[1]}")
    async def Run_all(self):
        asyn_jobs = []
        thread_job = []
        proces_job = []
        for item in self.All_jobs:
            if "file" in item[0].lower():
                t1 = asyncio.create_task(file(item[1]))
                asyn_jobs.append(t1)
            elif "slow" in item[0].lower():
                t2 = asyncio.wait_for(slow_request(item[1]),timeout=2) #or asyncio.creat_task(asyncio.waitfor(...  
                asyn_jobs.append(asyncio.create_task(t2))
            elif "down" in item[0].lower():
                thread_job.append(item[1])
            elif "calc" in item[0].lower():
                proces_job.append(item[1])
        for item in asyncio.as_completed(asyn_jobs):
            resp = await item
            self.results.append(resp)
        with ThreadPoolExecutor(max_workers=4) as ex:
            res2 = ex.map(download,thread_job)
        self.results.extend(res2)
        with ProcessPoolExecutor(max_workers=4) as ex:
            res3 = ex.map(calculation,proces_job)
        self.results.extend(res3)
        self.All_jobs.clear()
        print("Done")
    def View_result(self):
        for item in self.results:
            print(item)
    def Export_report(self):
        with open("Job_Results.txt","a") as file:
            for item in self.results:
                file.write(f"{item}\n")
        self.results.clear()
        print("Finished")

async def mainn(cls):
    while True:
        choice = int(input("\nEnter Your Choice: "))
        match choice:
            case 1:
                cls.add_job()
            case 2:
                cls.View_queue()
            case 3:
                await cls.Run_all()
            case 4:
                cls.View_result()
            case 5:
                cls.Export_report()
            case 6:
                print("Thank you")
                break
            case _:
                print("Please N. within 1-6\n")

print("\n======= Welcome ========\n")
print("1. Add Job")
print("2. View Queue")
print("3. Run all job")
print("4. View Result")
print("5. Export Report")
print("6. Exist\n")

if __name__=="__main__":
    clas_ob = Main()
    asyncio.run(mainn(clas_ob))
