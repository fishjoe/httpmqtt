import uasyncio

class l:
    lst=[]

def queue(d):
    async def sendIt():
        #This will not run until a sleep period occurs
        print(l.lst)
        l.lst=[]

	l.lst.append(d)
	if len(l.lst) > 1:
		return

	uasyncio.create_task(sendIt())

async def main():
	queue("hello")
	queue("world")
	await uasyncio.sleep(0)

	queue("this")
	queue("is")
	queue("neet")
	await uasyncio.sleep(0)

	queue("farewell")
	queue("my")
	queue("world")
	await uasyncio.sleep(0)

uasyncio.run(main())