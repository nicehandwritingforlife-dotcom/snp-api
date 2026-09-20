from fastapi import FastAPI, HTTPException, Query
import yt_dlp

app = FastAPI(title="Snapchat Downloader API")

@app.get("/get-snapchat")
def get_snapchat_media(url: str = Query(..., description="Snapchat URL")):
    # بررسی لینک اسنپ‌چت
    if "snapchat.com" not in url.lower():
        raise HTTPException(
            status_code=400, 
            detail="لینک وارد شده مربوط به اسنپ‌چت نیست."
        )

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            direct_url = info.get('url')
            if not direct_url and 'entries' in info and len(info['entries']) > 0:
                direct_url = info['entries'][0].get('url')

            if not direct_url:
                raise HTTPException(
                    status_code=404, 
                    detail="لینک مستقیم ویدیو یافت نشد."
                )

            return {
                "status": "success",
                "title": info.get('title', 'Snapchat Video'),
                "thumbnail": info.get('thumbnail'),
                "direct_url": direct_url
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"خطا در پردازش لینک: {str(e)}"
        )
