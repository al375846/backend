from app.db.db import db



async def carga_imagen(img_id:str):
    
    grid_out = await db.fs.open_download_stream(ObjectId(img_id))  
    p = 50 
    r = await grid_out.read(size=-1)
    for i in range(0,len(r),p):
        yield r[i:i+p]

