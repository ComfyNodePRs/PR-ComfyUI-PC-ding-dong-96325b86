import os
import execution
import asyncio
from typing import List, Literal, NamedTuple, Optional
from server import PromptServer
from aiohttp import web
routes = PromptServer.instance.routes


old_task_done = execution.PromptQueue.task_done

play_type = 'all'
video_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "video")

def new_task_done(self, item_id, history_result,
                  status: Optional['PromptQueue.ExecutionStatus']):
    ret = old_task_done(self, item_id, history_result, status)
    print(f"play_type: {play_type}, queue length: {len(self.queue)}")
    if play_type == 'all' and len(self.queue) >0:
        return ret
        
    PromptServer.instance.send_sync("pc.play_ding_dong_audio", {})

    return ret


execution.PromptQueue.task_done= new_task_done


files_end_with = ('.mp4', '.avi', '.mov', '.mkv', '.webm','.mp3')

def load_video():
    if not os.path.exists(video_dir):
        return []
        
    video_files = []
    for file in os.listdir(video_dir):
        if file.lower().endswith(files_end_with):
            video_files.append(file)
            
    return video_files


@routes.post('/pc_get_video_files')
async def get_video_files(request):
    video_files = load_video()
    return web.json_response({"video_files": video_files})

@routes.get('/pc_get_audio')
async def get_audio(request):
    # Get audio file path from query parameters
    filename = request.query.get('filename')
    if not filename:
        return web.Response(text="No filename provided", status=400)
        
    # Build full path to audio file in video directory
    audio_path = os.path.join(video_dir, filename)

    # Validate file exists and has audio extension
    if not os.path.exists(audio_path):
        return web.Response(text="Audio file not found", status=404)
        
    if not filename.lower().endswith(files_end_with):
        return web.Response(text="Invalid audio file format", status=400)

    # Return the audio file
    return web.FileResponse(audio_path)


@routes.post('/pc_set_play_type')
async def set_play_type(request):
    global play_type
    the_data = await request.post()
    play_type = the_data.get('play_type', 'all')
    return web.json_response({})


# Handle file upload via aiohttp
@routes.post('/pc_upload_video')
async def upload_video(request):
    reader = await request.multipart()
    field = await reader.next()
    
    if not field or field.name != 'file':
        return web.json_response({'error': 'No file uploaded'}, status=400)
        
    filename = field.filename
    if not filename.lower().endswith(files_end_with):
        return web.json_response({'error': 'Invalid file format'}, status=400)

    # Save uploaded file
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
        
    file_path = os.path.join(video_dir, filename)
    
    try:
        with open(file_path, 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

    return web.json_response({'success': True, 'filename': filename})


WEB_DIRECTORY = "./web"