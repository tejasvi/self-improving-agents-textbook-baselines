"""Inside the sandbox: forward TCP 127.0.0.1:PORT to the host proxy's Unix socket."""
import asyncio, sys
PORT = int(sys.argv[1]); SOCK = sys.argv[2]
async def pipe(r, w):
    try:
        while True:
            b = await r.read(65536)
            if not b: break
            w.write(b); await w.drain()
    except Exception: pass
    finally:
        try: w.close()
        except Exception: pass
async def handle(cr, cw):
    try: ur, uw = await asyncio.open_unix_connection(SOCK)
    except Exception:
        cw.close(); return
    await asyncio.gather(pipe(cr, uw), pipe(ur, cw))
async def main():
    srv = await asyncio.start_server(handle, '127.0.0.1', PORT)
    async with srv: await srv.serve_forever()
asyncio.run(main())
